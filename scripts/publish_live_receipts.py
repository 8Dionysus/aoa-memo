#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG_PATH = REPO_ROOT / ".aoa" / "live_receipts" / "memo-writeback-receipts.jsonl"
MEMORY_OBJECT_CATALOG_PATH = REPO_ROOT / "generated" / "memory_object_catalog.min.json"
RUNTIME_WRITEBACK_TARGETS_PATH = REPO_ROOT / "generated" / "runtime_writeback_targets.min.json"
GROWTH_REFINERY_LANES_PATH = REPO_ROOT / "generated" / "growth_refinery_writeback_lanes.min.json"
RECALL_SURFACE_PREFIX = "repo:aoa-memo/generated/memory_object_catalog.min.json#"
GROWTH_LANE_REF_PREFIX = "repo:aoa-memo/generated/growth_refinery_writeback_lanes.min.json#"
ALLOWED_EVENT_KINDS = {"memo_writeback_receipt", "memo_growth_writeback_receipt"}


class ReceiptPublishError(ValueError):
    pass


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append bounded memo-layer receipts to the owner-local live JSONL log."
    )
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        help="Path to a JSON or JSONL file containing one receipt, an array of receipts, or one receipt per line.",
    )
    parser.add_argument(
        "--log-path",
        default=str(DEFAULT_LOG_PATH),
        help="Owner-local JSONL log that should receive newly published memo receipts.",
    )
    parser.add_argument(
        "--catalog-path",
        default=str(MEMORY_OBJECT_CATALOG_PATH),
        help="Generated memory-object recall catalog used to verify receipt adoption.",
    )
    parser.add_argument(
        "--growth-lanes-path",
        default=str(GROWTH_REFINERY_LANES_PATH),
        help="Generated growth-refinery writeback lanes used to verify support-memory receipts.",
    )
    return parser.parse_args(argv)


def load_memory_object_catalog(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{path}: memory-object catalog must be an object")
    items = payload.get("memory_objects")
    if not isinstance(items, list):
        raise ReceiptPublishError(f"{path}: memory-object catalog must expose memory_objects")
    by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ReceiptPublishError(f"{path}.memory_objects[{index}]: must be an object")
        object_id = item.get("id")
        if not isinstance(object_id, str) or not object_id:
            raise ReceiptPublishError(f"{path}.memory_objects[{index}].id: must be a non-empty string")
        by_id[object_id] = item
    return by_id


def load_runtime_writeback_targets(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{path}: runtime writeback targets must be an object")
    items = payload.get("targets")
    if not isinstance(items, list):
        raise ReceiptPublishError(f"{path}: runtime writeback targets must expose targets")
    by_surface: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ReceiptPublishError(f"{path}.targets[{index}]: must be an object")
        runtime_surface = item.get("runtime_surface")
        if not isinstance(runtime_surface, str) or not runtime_surface:
            raise ReceiptPublishError(
                f"{path}.targets[{index}].runtime_surface: must be a non-empty string"
            )
        by_surface[runtime_surface] = item
    return by_surface


def load_growth_refinery_writeback_lanes(path: Path) -> dict[str, dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{path}: growth refinery writeback lanes must be an object")
    items = payload.get("lanes")
    if not isinstance(items, list):
        raise ReceiptPublishError(f"{path}: growth refinery writeback lanes must expose lanes")
    by_ref: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ReceiptPublishError(f"{path}.lanes[{index}]: must be an object")
        lane_ref = item.get("lane_ref")
        if not isinstance(lane_ref, str) or not lane_ref:
            raise ReceiptPublishError(f"{path}.lanes[{index}].lane_ref: must be a non-empty string")
        by_ref[lane_ref] = item
    return by_ref


def validate_memo_writeback_receipt(
    *,
    receipt: dict[str, Any],
    location: str,
    object_id: str,
    payload: dict[str, Any],
    evidence_ref_values: list[str],
    memory_objects_by_id: dict[str, dict[str, Any]],
    runtime_targets_by_surface: dict[str, dict[str, Any]],
) -> None:
    catalog_entry = memory_objects_by_id.get(object_id)
    if catalog_entry is None:
        raise ReceiptPublishError(
            f"{location}.object_ref.id: {object_id!r} does not resolve in generated memory-object recall catalog"
        )

    recall_ref = f"{RECALL_SURFACE_PREFIX}{object_id}"
    if recall_ref not in evidence_ref_values:
        raise ReceiptPublishError(
            f"{location}.evidence_refs: must include adopted recall surface ref {recall_ref!r}"
        )

    for field in ("target_kind", "writeback_class", "review_state"):
        if not isinstance(payload.get(field), str) or not payload[field]:
            raise ReceiptPublishError(f"{location}.payload.{field}: must be a non-empty string")

    memory_object_ref = payload.get("memory_object_ref")
    if memory_object_ref is not None:
        if not isinstance(memory_object_ref, str) or not memory_object_ref:
            raise ReceiptPublishError(f"{location}.payload.memory_object_ref: must be a non-empty string")
        if memory_object_ref != catalog_entry.get("source_path"):
            raise ReceiptPublishError(
                f"{location}.payload.memory_object_ref: must match adopted memory object source_path "
                f"{catalog_entry.get('source_path')!r}"
            )
    if payload["target_kind"] != catalog_entry.get("kind"):
        raise ReceiptPublishError(
            f"{location}.payload.target_kind: must match adopted memory object kind "
            f"{catalog_entry.get('kind')!r}"
        )
    if payload["review_state"] != catalog_entry.get("review_state"):
        raise ReceiptPublishError(
            f"{location}.payload.review_state: must match adopted memory object review_state "
            f"{catalog_entry.get('review_state')!r}"
        )

    if payload["writeback_class"] != "reviewed_candidate":
        return

    runtime_surface = payload.get("runtime_surface")
    if not isinstance(runtime_surface, str) or not runtime_surface:
        raise ReceiptPublishError(
            f"{location}.payload.runtime_surface: reviewed_candidate receipts must include a non-empty runtime_surface"
        )
    runtime_target = runtime_targets_by_surface.get(runtime_surface)
    if runtime_target is None:
        raise ReceiptPublishError(
            f"{location}.payload.runtime_surface: unknown runtime writeback surface {runtime_surface!r}"
        )
    if runtime_target.get("writeback_class") != "reviewed_candidate":
        raise ReceiptPublishError(
            f"{location}.payload.runtime_surface: {runtime_surface!r} must resolve to a reviewed_candidate mapping"
        )
    if runtime_target.get("target_kind") != payload["target_kind"]:
        raise ReceiptPublishError(
            f"{location}.payload.runtime_surface: {runtime_surface!r} must resolve to target_kind "
            f"{payload['target_kind']!r}"
        )
    writeback_anchor_ref = payload.get("writeback_anchor_ref")
    if not isinstance(writeback_anchor_ref, str) or not writeback_anchor_ref:
        raise ReceiptPublishError(
            f"{location}.payload.writeback_anchor_ref: reviewed_candidate receipts must include a non-empty writeback_anchor_ref"
        )
    if writeback_anchor_ref not in evidence_ref_values:
        raise ReceiptPublishError(
            f"{location}.evidence_refs: reviewed_candidate receipts must include writeback anchor ref {writeback_anchor_ref!r}"
        )
    if memory_object_ref is None:
        raise ReceiptPublishError(
            f"{location}.payload.memory_object_ref: reviewed_candidate receipts must include adopted memory object source_path"
        )


def validate_growth_writeback_receipt(
    *,
    location: str,
    object_id: str,
    payload: dict[str, Any],
    evidence_ref_values: list[str],
    growth_lanes_by_ref: dict[str, dict[str, Any]],
) -> None:
    for field in ("growth_lane_ref", "target_kind", "writeback_class", "review_status", "source_example_ref"):
        if not isinstance(payload.get(field), str) or not payload[field]:
            raise ReceiptPublishError(f"{location}.payload.{field}: must be a non-empty string")

    lane_ref = payload["growth_lane_ref"]
    lane = growth_lanes_by_ref.get(lane_ref)
    if lane is None:
        raise ReceiptPublishError(
            f"{location}.payload.growth_lane_ref: unknown growth refinery writeback lane {lane_ref!r}"
        )
    if object_id != lane.get("memory_id"):
        raise ReceiptPublishError(
            f"{location}.object_ref.id: must match lane memory_id {lane.get('memory_id')!r}"
        )
    if payload["target_kind"] != lane.get("target_kind"):
        raise ReceiptPublishError(
            f"{location}.payload.target_kind: must match lane target_kind {lane.get('target_kind')!r}"
        )
    if payload["writeback_class"] != lane.get("writeback_class"):
        raise ReceiptPublishError(
            f"{location}.payload.writeback_class: must match lane writeback_class {lane.get('writeback_class')!r}"
        )
    if payload["review_status"] != lane.get("review_status"):
        raise ReceiptPublishError(
            f"{location}.payload.review_status: must match lane review_status {lane.get('review_status')!r}"
        )
    if payload["source_example_ref"] != lane.get("source_path"):
        raise ReceiptPublishError(
            f"{location}.payload.source_example_ref: must match lane source_path {lane.get('source_path')!r}"
        )

    primary_ref = lane.get("primary_ref")
    if not isinstance(primary_ref, str) or primary_ref not in evidence_ref_values:
        raise ReceiptPublishError(
            f"{location}.evidence_refs: must include primary support ref {primary_ref!r}"
        )
    expected_lane_ref = f"{GROWTH_LANE_REF_PREFIX}{lane_ref}"
    if expected_lane_ref not in evidence_ref_values:
        raise ReceiptPublishError(
            f"{location}.evidence_refs: must include growth lane ref {expected_lane_ref!r}"
        )

    required_evidence_refs = lane.get("required_evidence_refs")
    if not isinstance(required_evidence_refs, list):
        raise ReceiptPublishError(
            f"{location}.payload.growth_lane_ref: lane {lane_ref!r} must expose required_evidence_refs"
        )
    for required_ref in required_evidence_refs:
        if required_ref not in evidence_ref_values:
            raise ReceiptPublishError(
                f"{location}.evidence_refs: must include required growth-refinery evidence ref {required_ref!r}"
            )


def validate_receipt(
    receipt: dict[str, Any],
    *,
    location: str,
    memory_objects_by_id: dict[str, dict[str, Any]],
    runtime_targets_by_surface: dict[str, dict[str, Any]],
    growth_lanes_by_ref: dict[str, dict[str, Any]],
) -> None:
    required_fields = (
        "event_kind",
        "event_id",
        "observed_at",
        "run_ref",
        "session_ref",
        "actor_ref",
        "object_ref",
        "evidence_refs",
        "payload",
    )
    for field in required_fields:
        if field not in receipt:
            raise ReceiptPublishError(f"{location}: missing field {field!r}")

    event_kind = receipt["event_kind"]
    if event_kind not in ALLOWED_EVENT_KINDS:
        raise ReceiptPublishError(
            f"{location}.event_kind: unsupported memo receipt kind {event_kind!r}"
        )
    if not isinstance(receipt["event_id"], str) or not receipt["event_id"]:
        raise ReceiptPublishError(f"{location}.event_id: must be a non-empty string")

    object_ref = receipt["object_ref"]
    if not isinstance(object_ref, dict):
        raise ReceiptPublishError(f"{location}.object_ref: must be an object")
    object_id = object_ref.get("id")
    if not isinstance(object_id, str) or not object_id:
        raise ReceiptPublishError(f"{location}.object_ref.id: must be a non-empty string")

    evidence_refs = receipt["evidence_refs"]
    if not isinstance(evidence_refs, list) or not evidence_refs:
        raise ReceiptPublishError(f"{location}.evidence_refs: must be a list")
    evidence_ref_values: list[str] = []
    for index, evidence_ref in enumerate(evidence_refs):
        if not isinstance(evidence_ref, dict):
            raise ReceiptPublishError(f"{location}.evidence_refs[{index}]: must be an object")
        ref = evidence_ref.get("ref")
        if not isinstance(ref, str) or not ref:
            raise ReceiptPublishError(f"{location}.evidence_refs[{index}].ref: must be a non-empty string")
        evidence_ref_values.append(ref)

    payload = receipt["payload"]
    if not isinstance(payload, dict):
        raise ReceiptPublishError(f"{location}.payload: must be an object")

    object_kind = object_ref.get("kind")
    if event_kind == "memo_writeback_receipt":
        if object_kind != "memory_object":
            raise ReceiptPublishError(f"{location}.object_ref.kind: must equal 'memory_object'")
        validate_memo_writeback_receipt(
            receipt=receipt,
            location=location,
            object_id=object_id,
            payload=payload,
            evidence_ref_values=evidence_ref_values,
            memory_objects_by_id=memory_objects_by_id,
            runtime_targets_by_surface=runtime_targets_by_surface,
        )
        return

    if object_kind != "support_memory":
        raise ReceiptPublishError(f"{location}.object_ref.kind: must equal 'support_memory'")
    validate_growth_writeback_receipt(
        location=location,
        object_id=object_id,
        payload=payload,
        evidence_ref_values=evidence_ref_values,
        growth_lanes_by_ref=growth_lanes_by_ref,
    )


def load_receipts(
    paths: list[Path],
    *,
    memory_objects_by_id: dict[str, dict[str, Any]] | None = None,
    runtime_targets_by_surface: dict[str, dict[str, Any]] | None = None,
    growth_lanes_by_ref: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if memory_objects_by_id is None:
        memory_objects_by_id = load_memory_object_catalog(MEMORY_OBJECT_CATALOG_PATH)
    if runtime_targets_by_surface is None:
        runtime_targets_by_surface = load_runtime_writeback_targets(RUNTIME_WRITEBACK_TARGETS_PATH)
    if growth_lanes_by_ref is None:
        growth_lanes_by_ref = load_growth_refinery_writeback_lanes(GROWTH_REFINERY_LANES_PATH)
    receipts: list[dict[str, Any]] = []
    for path in paths:
        if path.suffix == ".jsonl":
            for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                line = raw_line.strip()
                if not line:
                    continue
                item = json.loads(line)
                if not isinstance(item, dict):
                    raise ReceiptPublishError(f"{path}:{line_number}: receipt must be an object")
                validate_receipt(
                    item,
                    location=f"{path}:{line_number}",
                    memory_objects_by_id=memory_objects_by_id,
                    runtime_targets_by_surface=runtime_targets_by_surface,
                    growth_lanes_by_ref=growth_lanes_by_ref,
                )
                receipts.append(item)
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            validate_receipt(
                payload,
                location=str(path),
                memory_objects_by_id=memory_objects_by_id,
                runtime_targets_by_surface=runtime_targets_by_surface,
                growth_lanes_by_ref=growth_lanes_by_ref,
            )
            receipts.append(payload)
            continue
        if not isinstance(payload, list):
            raise ReceiptPublishError(f"{path}: receipt payload must be an object or list")
        for index, item in enumerate(payload):
            if not isinstance(item, dict):
                raise ReceiptPublishError(f"{path}[{index}]: receipt must be an object")
            validate_receipt(
                item,
                location=f"{path}[{index}]",
                memory_objects_by_id=memory_objects_by_id,
                runtime_targets_by_surface=runtime_targets_by_surface,
                growth_lanes_by_ref=growth_lanes_by_ref,
            )
            receipts.append(item)
    return receipts


def load_existing_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    event_ids: set[str] = set()
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        item = json.loads(line)
        if not isinstance(item, dict):
            raise ReceiptPublishError(f"{path}:{line_number}: existing log line must be an object")
        event_id = item.get("event_id")
        if isinstance(event_id, str) and event_id:
            event_ids.add(event_id)
    return event_ids


def append_new_receipts(*, log_path: Path, receipts: list[dict[str, Any]]) -> tuple[int, int]:
    existing_ids = load_existing_ids(log_path)
    appended = 0
    skipped = 0
    needs_line_boundary = False
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if log_path.exists() and log_path.stat().st_size > 0:
        with log_path.open("rb") as existing_handle:
            existing_handle.seek(-1, 2)
            needs_line_boundary = existing_handle.read(1) != b"\n"
    with log_path.open("a", encoding="utf-8") as handle:
        for receipt in receipts:
            event_id = receipt["event_id"]
            if event_id in existing_ids:
                skipped += 1
                continue
            if needs_line_boundary:
                handle.write("\n")
                needs_line_boundary = False
            handle.write(json.dumps(receipt, sort_keys=True, ensure_ascii=False) + "\n")
            existing_ids.add(event_id)
            appended += 1
    return appended, skipped


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    input_paths = [Path(path).expanduser().resolve() for path in args.input]
    if not input_paths:
        raise SystemExit("no receipt input files were provided")
    log_path = Path(args.log_path).expanduser().resolve()
    catalog_path = Path(args.catalog_path).expanduser().resolve()
    growth_lanes_path = Path(args.growth_lanes_path).expanduser().resolve()
    memory_objects_by_id = load_memory_object_catalog(catalog_path)
    runtime_targets_by_surface = load_runtime_writeback_targets(RUNTIME_WRITEBACK_TARGETS_PATH)
    growth_lanes_by_ref = load_growth_refinery_writeback_lanes(growth_lanes_path)
    receipts = load_receipts(
        input_paths,
        memory_objects_by_id=memory_objects_by_id,
        runtime_targets_by_surface=runtime_targets_by_surface,
        growth_lanes_by_ref=growth_lanes_by_ref,
    )
    appended, skipped = append_new_receipts(log_path=log_path, receipts=receipts)
    print(f"[ok] appended {appended} memo receipts to {log_path}")
    print(f"[skip] duplicate event ids skipped: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
