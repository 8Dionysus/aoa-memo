"""Live receipt log degradation and provenance checks."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def validate_live_receipt_log() -> None:
    if not LIVE_RECEIPT_LOG_PATH.exists():
        print("[OK]   live receipt log absent")
        return

    catalog = load_json(GENERATED / "memory-objects" / "memory_object_catalog.min.json")
    capsules = load_json(GENERATED / "memory-objects" / "memory_object_capsules.json")
    sections = load_json(GENERATED / "memory-objects" / "memory_object_sections.full.json")
    runtime_targets = load_json(RUNTIME_WRITEBACK_TARGETS_PATH)
    growth_lanes = load_json(GROWTH_REFINERY_WRITEBACK_LANES_PATH)
    catalog_entries_by_id = {
        item["id"]: item
        for item in catalog.get("memory_objects", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    capsule_entries_by_id = {
        item["id"]: item
        for item in capsules.get("memory_objects", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    section_entries_by_id = {
        item["id"]: item
        for item in sections.get("memory_objects", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    runtime_targets_by_surface = {
        item["runtime_surface"]: item
        for item in runtime_targets.get("targets", [])
        if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
    }
    growth_lanes_by_ref = {
        item["lane_ref"]: item
        for item in growth_lanes.get("lanes", [])
        if isinstance(item, dict) and isinstance(item.get("lane_ref"), str)
    }
    catalog_ids = set(catalog_entries_by_id)
    errors: list[str] = []
    seen_event_ids: set[str] = set()
    reviewed_object_cache: dict[str, dict] = {}

    def reviewed_corpus_object(catalog_entry: dict) -> dict | None:
        source_path = catalog_entry.get("source_path")
        if catalog_entry.get("source_kind") != "reviewed_corpus" or not isinstance(source_path, str):
            return None
        if source_path in reviewed_object_cache:
            return reviewed_object_cache[source_path]
        object_path = ROOT / source_path
        if not object_path.exists():
            return None
        data = load_json(object_path)
        if not isinstance(data, dict):
            return None
        reviewed_object_cache[source_path] = data
        return data

    def source_ref_payload(ref: str) -> dict | None:
        ref_path = ref.removeprefix("repo:aoa-memo/") if ref.startswith("repo:aoa-memo/") else ref
        ref_path, _, _ = ref_path.partition("#")
        target = ROOT / ref_path
        if not target.exists() or target.suffix.lower() != ".json":
            return None
        data = load_json(target)
        return data if isinstance(data, dict) else None

    def is_reviewed_corpus_source_ref(catalog_entry: dict, ref: object) -> bool:
        if not isinstance(ref, str) or not ref:
            return False
        reviewed_object = reviewed_corpus_object(catalog_entry)
        if reviewed_object is None:
            return False
        source_refs = reviewed_object.get("provenance", {}).get("source_refs", [])
        return isinstance(source_refs, list) and ref in source_refs

    for line_number, raw_line in enumerate(
        LIVE_RECEIPT_LOG_PATH.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = raw_line.strip()
        if not line:
            continue
        try:
            receipt = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: invalid JSONL receipt: {exc}")
            continue
        if not isinstance(receipt, dict):
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: receipt must be an object")
            continue

        event_id = receipt.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: event_id must be a non-empty string")
        elif event_id in seen_event_ids:
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: duplicate event_id {event_id!r}")
        else:
            seen_event_ids.add(event_id)

        event_kind = receipt.get("event_kind")
        if event_kind not in {"memo_writeback_receipt", "memo_growth_writeback_receipt"}:
            errors.append(
                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: event_kind must be a supported memo live receipt kind"
            )
        else:
            actor_ref = receipt.get("actor_ref")
            expected_actor_ref = LIVE_RECEIPT_ACTOR_BY_KIND[event_kind]
            if not isinstance(actor_ref, str) or not actor_ref:
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: actor_ref must be a non-empty string"
                )
            elif actor_ref != expected_actor_ref:
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: actor_ref {actor_ref!r} "
                    f"must equal {expected_actor_ref!r} for {event_kind} receipts"
                )

        object_ref = receipt.get("object_ref")
        object_id = object_ref.get("id") if isinstance(object_ref, dict) else None
        if not isinstance(object_ref, dict):
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref must be an object")
        else:
            if object_ref.get("repo") != "aoa-memo":
                errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.repo must equal 'aoa-memo'")
            if not isinstance(object_id, str) or not object_id:
                errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.id must be a non-empty string")
            elif event_kind == "memo_writeback_receipt":
                if object_ref.get("kind") != "memory_object":
                    errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.kind must equal 'memory_object'")
                elif object_id not in catalog_ids:
                    errors.append(
                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.id {object_id!r} "
                        "is absent from generated/memory-objects/memory_object_catalog.min.json"
                    )
                else:
                    catalog_entry = catalog_entries_by_id[object_id]
                    capsule_entry = capsule_entries_by_id.get(object_id)
                    if capsule_entry is None:
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.id {object_id!r} "
                            "is absent from generated/memory-objects/memory_object_capsules.json"
                        )
                    else:
                        if capsule_entry.get("kind") != catalog_entry.get("kind"):
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: capsule kind "
                                f"{capsule_entry.get('kind')!r} must match catalog kind "
                                f"{catalog_entry.get('kind')!r}"
                            )
                        if capsule_entry.get("source_path") != catalog_entry.get("source_path"):
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: capsule source_path "
                                f"{capsule_entry.get('source_path')!r} must match catalog source_path "
                                f"{catalog_entry.get('source_path')!r}"
                            )
                    section_entry = section_entries_by_id.get(object_id)
                    if section_entry is None:
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.id {object_id!r} "
                            "is absent from generated/memory-objects/memory_object_sections.full.json"
                        )
                    else:
                        if section_entry.get("kind") != catalog_entry.get("kind"):
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: section kind "
                                f"{section_entry.get('kind')!r} must match catalog kind "
                                f"{catalog_entry.get('kind')!r}"
                            )
                        if section_entry.get("source_path") != catalog_entry.get("source_path"):
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: section source_path "
                                f"{section_entry.get('source_path')!r} must match catalog source_path "
                                f"{catalog_entry.get('source_path')!r}"
                            )
                        section_items = section_entry.get("sections")
                        if not isinstance(section_items, list) or not section_items:
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: section entry for {object_id!r} "
                                "must expose non-empty sections"
                            )
            elif event_kind == "memo_growth_writeback_receipt":
                if object_ref.get("kind") != "support_memory":
                    errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.kind must equal 'support_memory'")

        payload = receipt.get("payload")
        growth_lane_ref: str | None = None
        growth_lane: dict | None = None
        if not isinstance(payload, dict):
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload must be an object")
        else:
            if event_kind == "memo_writeback_receipt":
                for field in ("target_kind", "writeback_class", "review_state"):
                    if not isinstance(payload.get(field), str) or not payload[field]:
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.{field} must be a non-empty string"
                        )
                if isinstance(object_id, str) and object_id in catalog_entries_by_id:
                    catalog_entry = catalog_entries_by_id[object_id]
                    if payload.get("target_kind") != catalog_entry.get("kind"):
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.target_kind "
                            f"{payload.get('target_kind')!r} must match catalog kind "
                            f"{catalog_entry.get('kind')!r}"
                        )
                    if payload.get("review_state") != catalog_entry.get("review_state"):
                        memory_object_ref = payload.get("memory_object_ref")
                        ref_payload = source_ref_payload(memory_object_ref) if isinstance(memory_object_ref, str) else None
                        ref_review_state = (
                            ref_payload.get("lifecycle", {}).get("review_state")
                            if isinstance(ref_payload, dict)
                            else None
                        )
                        if not (
                            is_reviewed_corpus_source_ref(catalog_entry, memory_object_ref)
                            and payload.get("review_state") == ref_review_state
                        ):
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.review_state "
                                f"{payload.get('review_state')!r} must match catalog review_state "
                                f"{catalog_entry.get('review_state')!r}"
                            )
                    memory_object_ref = payload.get("memory_object_ref")
                    if memory_object_ref is not None:
                        if not isinstance(memory_object_ref, str) or not memory_object_ref:
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.memory_object_ref must be a non-empty string"
                            )
                        elif (
                            memory_object_ref != catalog_entry.get("source_path")
                            and not is_reviewed_corpus_source_ref(catalog_entry, memory_object_ref)
                        ):
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.memory_object_ref "
                                f"{memory_object_ref!r} must match catalog source_path "
                                f"{catalog_entry.get('source_path')!r}"
                            )
                    if payload.get("writeback_class") == "reviewed_candidate":
                        runtime_surface = payload.get("runtime_surface")
                        if not isinstance(runtime_surface, str) or not runtime_surface:
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: reviewed_candidate receipts must include payload.runtime_surface"
                            )
                        else:
                            runtime_target = runtime_targets_by_surface.get(runtime_surface)
                            if runtime_target is None:
                                errors.append(
                                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.runtime_surface "
                                    f"{runtime_surface!r} is absent from mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json"
                                )
                            else:
                                if runtime_target.get("writeback_class") != "reviewed_candidate":
                                    errors.append(
                                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.runtime_surface "
                                        f"{runtime_surface!r} must resolve to a reviewed_candidate mapping"
                                    )
                                if runtime_target.get("target_kind") != catalog_entry.get("kind"):
                                    errors.append(
                                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.runtime_surface "
                                        f"{runtime_surface!r} must resolve to catalog kind {catalog_entry.get('kind')!r}"
                                    )
                        writeback_anchor_ref = payload.get("writeback_anchor_ref")
                        if not isinstance(writeback_anchor_ref, str) or not writeback_anchor_ref:
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: reviewed_candidate receipts must include payload.writeback_anchor_ref"
                            )
                        if memory_object_ref is None:
                            errors.append(
                                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: reviewed_candidate receipts must include payload.memory_object_ref"
                            )
            elif event_kind == "memo_growth_writeback_receipt":
                for field in ("growth_lane_ref", "target_kind", "writeback_class", "review_status", "source_example_ref"):
                    if not isinstance(payload.get(field), str) or not payload[field]:
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.{field} must be a non-empty string"
                        )
                growth_lane_ref = payload.get("growth_lane_ref") if isinstance(payload.get("growth_lane_ref"), str) else None
                growth_lane = growth_lanes_by_ref.get(growth_lane_ref) if growth_lane_ref else None
                if growth_lane_ref and growth_lane is None:
                    errors.append(
                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.growth_lane_ref "
                        f"{growth_lane_ref!r} is absent from mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json"
                    )
                if isinstance(growth_lane, dict):
                    if payload.get("target_kind") != growth_lane.get("target_kind"):
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.target_kind "
                            f"{payload.get('target_kind')!r} must match lane target_kind "
                            f"{growth_lane.get('target_kind')!r}"
                        )
                    if payload.get("writeback_class") != growth_lane.get("writeback_class"):
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.writeback_class "
                            f"{payload.get('writeback_class')!r} must match lane writeback_class "
                            f"{growth_lane.get('writeback_class')!r}"
                        )
                    if payload.get("review_status") != growth_lane.get("review_status"):
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.review_status "
                            f"{payload.get('review_status')!r} must match lane review_status "
                            f"{growth_lane.get('review_status')!r}"
                        )
                    if payload.get("source_example_ref") != growth_lane.get("source_path"):
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.source_example_ref "
                            f"{payload.get('source_example_ref')!r} must match lane source_path "
                            f"{growth_lane.get('source_path')!r}"
                        )
                    if isinstance(object_id, str) and object_id != growth_lane.get("memory_id"):
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.id {object_id!r} "
                            f"must match lane memory_id {growth_lane.get('memory_id')!r}"
                        )

        evidence_refs = receipt.get("evidence_refs")
        if not isinstance(evidence_refs, list):
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs must be a list")
            continue
        evidence_ref_values: list[str] = []
        for evidence_index, evidence in enumerate(evidence_refs):
            if not isinstance(evidence, dict):
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}] must be an object"
                )
                continue
            ref = evidence.get("ref")
            if not isinstance(ref, str) or not ref:
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}].ref must be a non-empty string"
                )
                continue
            evidence_ref_values.append(ref)
            if not ref.startswith("repo:aoa-memo/"):
                continue
            path_text, _, anchor = ref.removeprefix("repo:aoa-memo/").partition("#")
            if any(part in {"", ".", ".."} for part in path_text.split("/")):
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}].ref "
                    f"must use a normalized repo-relative path: {path_text!r}"
                )
                continue
            local_path = (ROOT / path_text).resolve()
            try:
                local_path.relative_to(ROOT_RESOLVED)
            except ValueError:
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}].ref "
                    f"escapes the repository root: {path_text!r}"
                )
                continue
            if not local_path.exists():
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}].ref "
                    f"points to missing local path {path_text!r}"
                )
                continue
            if path_text == "generated/memory-objects/memory_object_catalog.min.json":
                if not anchor:
                    errors.append(
                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: catalog evidence ref must include a memory object id anchor"
                    )
                elif anchor not in catalog_ids:
                    errors.append(
                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: catalog evidence ref points to uncataloged id {anchor!r}"
                    )
                elif isinstance(object_id, str) and anchor != object_id:
                    errors.append(
                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: catalog evidence id {anchor!r} "
                        f"must match object_ref.id {object_id!r}"
                    )
            if path_text == "mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json":
                if not anchor:
                    errors.append(
                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth lane evidence ref must include a lane anchor"
                    )
                elif anchor not in growth_lanes_by_ref:
                    errors.append(
                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth lane evidence ref points to unknown lane {anchor!r}"
                    )
                elif growth_lane_ref is not None and anchor != growth_lane_ref:
                    errors.append(
                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth lane evidence ref {anchor!r} "
                        f"must match payload.growth_lane_ref {growth_lane_ref!r}"
                    )
        if event_kind == "memo_writeback_receipt" and isinstance(object_id, str) and object_id in catalog_ids:
            expected_recall_ref = f"{RECALL_SURFACE_PREFIX}{object_id}"
            if expected_recall_ref not in evidence_ref_values:
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs must include adopted recall surface ref "
                    f"{expected_recall_ref!r}"
                )
            if (
                isinstance(payload, dict)
                and payload.get("writeback_class") == "reviewed_candidate"
                and isinstance(payload.get("writeback_anchor_ref"), str)
                and payload["writeback_anchor_ref"] not in evidence_ref_values
            ):
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: reviewed_candidate receipts must include writeback anchor ref "
                    f"{payload['writeback_anchor_ref']!r} in evidence_refs"
                )
        if event_kind == "memo_growth_writeback_receipt" and isinstance(growth_lane, dict) and growth_lane_ref is not None:
            primary_ref = growth_lane.get("primary_ref")
            if isinstance(primary_ref, str) and primary_ref not in evidence_ref_values:
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth receipts must include primary support ref "
                    f"{primary_ref!r}"
                )
            expected_lane_ref = f"{GROWTH_LANE_REF_PREFIX}{growth_lane_ref}"
            if expected_lane_ref not in evidence_ref_values:
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth receipts must include lane ref "
                    f"{expected_lane_ref!r}"
                )
            required_refs = growth_lane.get("required_evidence_refs")
            if isinstance(required_refs, list):
                for required_ref in required_refs:
                    if required_ref not in evidence_ref_values:
                        errors.append(
                            f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: growth receipts must include required evidence ref "
                            f"{required_ref!r}"
                        )

    if errors:
        print("[FAIL] live receipt log")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   live receipt log")
