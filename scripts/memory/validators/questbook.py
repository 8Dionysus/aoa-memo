"""Quest source and projection checks for the memory-context profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def quest_sort_key(quest_id: str) -> tuple[int, str]:
    suffix = quest_id.rsplit("-", 1)[-1]
    try:
        return (int(suffix), quest_id)
    except ValueError:
        return (sys.maxsize, quest_id)

def discover_questbook_file_paths() -> list[Path]:
    return sorted(
        (
            path
            for path in (ROOT / "quests" / "memo").glob("*/AOA-MEM-Q-*.yaml")
            if path.is_file()
        ),
        key=lambda path: (quest_sort_key(path.stem), path.as_posix()),
    )

def duplicate_questbook_file_issues(paths: list[Path] | None = None) -> list[str]:
    by_quest_id: dict[str, list[Path]] = {}
    for path in paths if paths is not None else discover_questbook_file_paths():
        by_quest_id.setdefault(path.stem, []).append(path)

    issues: list[str] = []
    for quest_id in sorted(by_quest_id, key=quest_sort_key):
        duplicates = by_quest_id[quest_id]
        if len(duplicates) < 2:
            continue
        locations = ", ".join(path.relative_to(ROOT).as_posix() for path in duplicates)
        issues.append(f"duplicate quest id {quest_id}: {locations}")
    return issues

def discover_questbook_files(paths: list[Path] | None = None) -> dict[str, Path]:
    discovered: dict[str, Path] = {}
    for path in paths if paths is not None else discover_questbook_file_paths():
        discovered.setdefault(path.stem, path)
    if not discovered:
        return dict(FOUNDATION_QUESTBOOK_FILES)
    return {
        quest_id: discovered[quest_id]
        for quest_id in sorted(discovered, key=quest_sort_key)
    }

def quest_path_state(path: Path) -> str | None:
    try:
        relative = path.relative_to(ROOT / "quests")
    except ValueError:
        return None
    parts = relative.parts
    if len(parts) < 3:
        return None
    lane, state = parts[0], parts[1]
    if lane != "memo" or state not in QUEST_LIFECYCLE_STATES:
        return None
    return state

def quest_anchor_doc_ref(data: dict[str, object]) -> str | None:
    anchor_ref = data.get("anchor_ref")
    if isinstance(anchor_ref, str):
        return anchor_ref
    if isinstance(anchor_ref, dict):
        ref_value = anchor_ref.get("ref")
        if isinstance(ref_value, str):
            return ref_value
    return None

def validate_questbook_surface() -> None:
    errors: list[str] = []
    questbook_paths = discover_questbook_file_paths()
    errors.extend(duplicate_questbook_file_issues(questbook_paths))
    questbook_files = discover_questbook_files(questbook_paths)
    missing_foundation = [
        quest_id for quest_id in FOUNDATION_QUESTBOOK_FILES if quest_id not in questbook_files
    ]
    required_paths = [QUESTBOOK_PATH, QUESTBOOK_DOC, *FOUNDATION_QUESTBOOK_FILES.values()]
    for path in required_paths:
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
    for quest_id in missing_foundation:
        expected_path = FOUNDATION_QUESTBOOK_FILES[quest_id].relative_to(ROOT)
        errors.append(f"missing foundation quest file: {expected_path}")

    questbook_text = ""
    listed_quest_ids: set[str] = set()
    if QUESTBOOK_PATH.exists():
        questbook_text = load_text(QUESTBOOK_PATH)
        listed_quest_ids = set(QUEST_ID_PATTERN.findall(questbook_text))

    if QUESTBOOK_DOC.exists():
        doc_text = load_text(QUESTBOOK_DOC)
        if "WRITEBACK_TEMPERATURE_POLICY.md" not in doc_text:
            errors.append("mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md must stay anchored to mechanics/writeback/docs/WRITEBACK_TEMPERATURE_POLICY.md")
        lower_doc = doc_text.lower()
        for phrase in (
            "quest state remains source-owned",
            "good writeback candidates",
            "bad writeback candidates",
            "witness trace posture",
        ):
            if phrase not in lower_doc:
                errors.append(f"mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md must mention {phrase}")

    active_quest_ids: list[str] = []
    closed_quest_ids: list[str] = []
    expected_catalog_entries: list[dict[str, object]] = []
    expected_dispatch_entries: list[dict[str, object]] = []
    needs_orchestrator_memory_doc = ORCHESTRATOR_MEMORY_ALIGNMENT_DOC.exists()
    for quest_id, path in questbook_files.items():
        if not path.exists():
            continue
        data = load_yaml(path)
        if not isinstance(data, dict):
            errors.append(f"{path.relative_to(ROOT)} must parse to a mapping")
            continue
        schema_error = external_quest_schema_error(data, AOA_EVALS_ROOT / "schemas" / "quest.schema.json")
        if schema_error:
            errors.append(f"{path.relative_to(ROOT)} {schema_error}")
        if data.get("schema_version") != "work_quest_v1":
            errors.append(f"{path.relative_to(ROOT)} must keep schema_version work_quest_v1")
        if data.get("repo") != "aoa-memo":
            errors.append(f"{path.relative_to(ROOT)} must keep repo aoa-memo")
        if data.get("id") != quest_id:
            errors.append(f"{path.relative_to(ROOT)} must keep id {quest_id}")
        path_state = quest_path_state(path)
        if path_state is None:
            errors.append(
                f"{path.relative_to(ROOT)} must live under quests/memo/<state>/"
            )
        elif data.get("state") != path_state:
            errors.append(
                f"{path.relative_to(ROOT)} must keep state matching path state {path_state}"
            )
        if data.get("public_safe") is not True:
            errors.append(f"{path.relative_to(ROOT)} must keep public_safe true")
        orchestrator_class_ref = data.get("orchestrator_class_ref")
        capability_target = data.get("capability_target")
        if orchestrator_class_ref is None and capability_target is not None:
            errors.append(
                f"{path.relative_to(ROOT)} must not declare capability_target without orchestrator_class_ref"
            )
        if orchestrator_class_ref is not None:
            class_ref_error = validate_orchestrator_class_ref(
                orchestrator_class_ref,
                label=str(path.relative_to(ROOT)),
            )
            if class_ref_error:
                errors.append(class_ref_error)
            if capability_target not in ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS:
                errors.append(
                    f"{path.relative_to(ROOT)} must declare a supported capability_target when orchestrator_class_ref is present"
                )
            for field_name in ("playbook_family_refs", "proof_surface_refs", "memory_surface_refs"):
                if field_name not in data:
                    continue
                refs = data.get(field_name)
                if not isinstance(refs, list) or not refs:
                    errors.append(
                        f"{path.relative_to(ROOT)} must keep {field_name} as a non-empty list when present"
                    )
                    continue
                for index, ref in enumerate(refs):
                    error = local_ref_error(ref, f"{path.relative_to(ROOT)} {field_name}[{index}]")
                    if error:
                        errors.append(error)
        expected_orchestrator_pair = ORCHESTRATOR_MEMORY_QUESTS.get(quest_id)
        if expected_orchestrator_pair is not None:
            needs_orchestrator_memory_doc = True
            expected_ref, expected_target = expected_orchestrator_pair
            if data.get("kind") != "memory":
                errors.append(f"{path.relative_to(ROOT)} must keep kind memory")
            if data.get("owner_surface") != "mechanics/consumer-handoff/docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md":
                errors.append(
                    f"{path.relative_to(ROOT)} must keep owner_surface mechanics/consumer-handoff/docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md"
                )
            if orchestrator_class_ref != expected_ref:
                errors.append(
                    f"{path.relative_to(ROOT)} must keep orchestrator_class_ref {expected_ref}"
                )
            if capability_target != expected_target:
                errors.append(
                    f"{path.relative_to(ROOT)} must keep capability_target {expected_target}"
                )
        owner_surface = data.get("owner_surface")
        expected_owner_surface = EXPECTED_QUEST_OWNER_SURFACES.get(quest_id)
        if expected_owner_surface is not None:
            if owner_surface != expected_owner_surface:
                errors.append(
                    f"{path.relative_to(ROOT)} must keep owner_surface {expected_owner_surface}"
                )
            else:
                owner_error = local_ref_error(
                    owner_surface,
                    f"{path.relative_to(ROOT)} owner_surface",
                )
                if owner_error:
                    errors.append(owner_error)
        else:
            if not isinstance(owner_surface, str) or not owner_surface.startswith(
                QUEST_LOCAL_DOC_PREFIXES
            ):
                errors.append(
                    f"{path.relative_to(ROOT)} must keep owner_surface within local memo docs or mechanics docs"
                )
            else:
                owner_error = local_ref_error(
                    owner_surface,
                    f"{path.relative_to(ROOT)} owner_surface",
                )
                if owner_error:
                    errors.append(owner_error)
        anchor_ref = quest_anchor_doc_ref(data)
        if not isinstance(anchor_ref, str) or not anchor_ref.startswith(QUEST_LOCAL_DOC_PREFIXES):
            errors.append(
                f"{path.relative_to(ROOT)} must keep anchor_ref within local memo docs or mechanics docs"
            )
        else:
            anchor_error = local_ref_error(anchor_ref, f"{path.relative_to(ROOT)} anchor_ref")
            if anchor_error:
                errors.append(anchor_error)
        if data.get("state") in CLOSED_QUEST_STATES:
            closed_quest_ids.append(quest_id)
        else:
            active_quest_ids.append(quest_id)
        expected_catalog_entries.append(
            build_expected_quest_catalog_entry(
                data,
                source_path=path.relative_to(ROOT).as_posix(),
            )
        )
        expected_dispatch_entries.append(
            build_expected_quest_dispatch_entry(
                data,
                source_path=path.relative_to(ROOT).as_posix(),
            )
        )

    if needs_orchestrator_memory_doc:
        if not ORCHESTRATOR_MEMORY_ALIGNMENT_DOC.exists():
            errors.append("missing file: mechanics/consumer-handoff/docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md")
        else:
            memory_alignment_text = load_text(ORCHESTRATOR_MEMORY_ALIGNMENT_DOC)
            for token in ORCHESTRATOR_MEMORY_REQUIRED_TOKENS:
                if token not in memory_alignment_text:
                    errors.append(
                        f"mechanics/consumer-handoff/docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md must mention {token}"
                    )

    if questbook_text:
        for quest_id in active_quest_ids:
            if quest_id not in questbook_text:
                errors.append(f"QUESTBOOK.md must reference active quest id {quest_id}")
        for quest_id in closed_quest_ids:
            if quest_id in questbook_text:
                errors.append(f"QUESTBOOK.md must not list closed quest id {quest_id}")
        missing_listed_files = sorted(listed_quest_ids - set(questbook_files))
        for quest_id in missing_listed_files:
            errors.append(f"QUESTBOOK.md must not reference missing quest file quests/{quest_id}.yaml")

    try:
        actual_catalog = load_json(QUEST_CATALOG_PATH)
    except FileNotFoundError:
        errors.append("missing file: generated/quests/quest_catalog.min.json")
    else:
        if actual_catalog != expected_catalog_entries:
            errors.append("generated/quests/quest_catalog.min.json is out of date or mismatched")
    try:
        actual_catalog_example = load_json(QUEST_CATALOG_EXAMPLE_PATH)
    except FileNotFoundError:
        errors.append("missing file: generated/quests/quest_catalog.min.example.json")
    else:
        if actual_catalog_example != expected_catalog_entries:
            errors.append("generated/quests/quest_catalog.min.example.json is out of date or mismatched")
    try:
        actual_dispatch = load_json(QUEST_DISPATCH_PATH)
    except FileNotFoundError:
        errors.append("missing file: generated/quests/quest_dispatch.min.json")
        actual_dispatch = None
    if isinstance(actual_dispatch, list):
        for index, entry in enumerate(actual_dispatch):
            schema_error = external_quest_schema_error(
                entry,
                AOA_EVALS_ROOT / "schemas" / "quest_dispatch.schema.json",
            )
            if schema_error:
                errors.append(f"generated/quests/quest_dispatch.min.json[{index}] {schema_error}")
        if actual_dispatch != expected_dispatch_entries:
            errors.append("generated/quests/quest_dispatch.min.json is out of date or mismatched")
    elif actual_dispatch is not None:
        errors.append("generated/quests/quest_dispatch.min.json must be an array")
    try:
        actual_dispatch_example = load_json(QUEST_DISPATCH_EXAMPLE_PATH)
    except FileNotFoundError:
        errors.append("missing file: generated/quests/quest_dispatch.min.example.json")
        actual_dispatch_example = None
    if isinstance(actual_dispatch_example, list):
        for index, entry in enumerate(actual_dispatch_example):
            schema_error = external_quest_schema_error(
                entry,
                AOA_EVALS_ROOT / "schemas" / "quest_dispatch.schema.json",
            )
            if schema_error:
                errors.append(f"generated/quests/quest_dispatch.min.example.json[{index}] {schema_error}")
        if actual_dispatch_example != expected_dispatch_entries:
            errors.append("generated/quests/quest_dispatch.min.example.json is out of date or mismatched")
    elif actual_dispatch_example is not None:
        errors.append("generated/quests/quest_dispatch.min.example.json must be an array")

    if errors:
        print("[FAIL] questbook writeback surface")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   questbook writeback surface")

@lru_cache(maxsize=None)
def external_quest_schema_validator(schema_path: Path) -> Draft202012Validator | None:
    if not schema_path.exists():
        return None
    schema = load_json(schema_path)
    if not isinstance(schema, dict):
        print("[FAIL] questbook writeback surface")
        print(f"  - {schema_path.as_posix()} must remain a JSON object")
        raise SystemExit(1)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)

def external_quest_schema_error(data: object, schema_path: Path) -> str | None:
    validator = external_quest_schema_validator(schema_path)
    if validator is None:
        return None
    errors = sorted(
        validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    if not errors:
        return None
    first = errors[0]
    error_path = format_schema_path(list(first.absolute_path))
    if error_path:
        return f"schema violation at '{error_path}': {first.message}"
    return f"schema violation: {first.message}"

@lru_cache(maxsize=None)
def load_live_orchestrator_class_ids() -> set[str] | None:
    catalog_path = AOA_AGENTS_ROOT / "generated" / "orchestrator_class_catalog.min.json"
    if not catalog_path.exists():
        return None
    payload = load_json(catalog_path)
    if not isinstance(payload, dict):
        print("[FAIL] questbook writeback surface")
        print("  - aoa-agents generated/orchestrator_class_catalog.min.json must be a JSON object")
        raise SystemExit(1)
    entries = payload.get("orchestrator_classes")
    if not isinstance(entries, list):
        print("[FAIL] questbook writeback surface")
        print("  - aoa-agents generated/orchestrator_class_catalog.min.json must expose orchestrator_classes")
        raise SystemExit(1)
    class_ids: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            print("[FAIL] questbook writeback surface")
            print(
                "  - aoa-agents generated/orchestrator_class_catalog.min.json "
                f"orchestrator_classes[{index}] must be an object"
            )
            raise SystemExit(1)
        class_id = entry.get("id")
        if not isinstance(class_id, str) or not class_id:
            print("[FAIL] questbook writeback surface")
            print(
                "  - aoa-agents generated/orchestrator_class_catalog.min.json "
                f"orchestrator_classes[{index}] must expose a string id"
            )
            raise SystemExit(1)
        class_ids.add(class_id)
    return class_ids

def validate_orchestrator_class_ref(orchestrator_class_ref: object, *, label: str) -> str | None:
    if not isinstance(orchestrator_class_ref, str):
        return f"{label}: orchestrator_class_ref must be a string"
    repo_name, separator, class_id = orchestrator_class_ref.partition(":")
    if separator != ":" or repo_name != "aoa-agents" or not class_id:
        return f"{label}: orchestrator_class_ref must use the form aoa-agents:<class_id>"
    live_class_ids = load_live_orchestrator_class_ids()
    if live_class_ids is None:
        return None
    if class_id not in live_class_ids:
        return (
            f"{label}: orchestrator_class_ref must resolve in "
            "aoa-agents/generated/orchestrator_class_catalog.min.json"
        )
    return None

def build_expected_quest_catalog_entry(
    quest: dict[str, object], *, source_path: str
) -> dict[str, object]:
    entry: dict[str, object] = {
        "id": quest["id"],
        "title": quest["title"],
        "repo": quest["repo"],
        "theme_ref": quest.get("theme_ref", ""),
        "milestone_ref": quest.get("milestone_ref", ""),
        "state": quest["state"],
        "band": quest["band"],
        "kind": quest["kind"],
        "difficulty": quest["difficulty"],
        "risk": quest["risk"],
        "owner_surface": quest["owner_surface"],
        "source_path": source_path,
        "public_safe": quest["public_safe"],
    }
    for optional_key in (
        "orchestrator_class_ref",
        "capability_target",
        "playbook_family_refs",
        "proof_surface_refs",
        "memory_surface_refs",
    ):
        if optional_key in quest:
            entry[optional_key] = quest[optional_key]
    return entry

def build_expected_quest_dispatch_entry(
    quest: dict[str, object], *, source_path: str
) -> dict[str, object]:
    activation = quest.get("activation")
    if not isinstance(activation, dict):
        activation = {}
    requires_artifacts = ["recurrence_evidence", "promotion_decision"] if quest.get("kind") == "harvest" else [
        "bounded_plan",
        "work_result",
        "verification_result",
    ]
    entry: dict[str, object] = {
        "schema_version": "quest_dispatch_v1",
        "id": quest["id"],
        "repo": quest["repo"],
        "state": quest["state"],
        "band": quest["band"],
        "difficulty": quest["difficulty"],
        "risk": quest["risk"],
        "control_mode": quest["control_mode"],
        "delegate_tier": quest["delegate_tier"],
        "split_required": quest["split_required"],
        "write_scope": quest["write_scope"],
        "requires_artifacts": requires_artifacts,
        "activation_mode": activation.get("mode"),
        "source_path": source_path,
        "public_safe": quest["public_safe"],
    }
    if "fallback_tier" in quest:
        entry["fallback_tier"] = quest.get("fallback_tier")
    if "wrapper_class" in quest:
        entry["wrapper_class"] = quest.get("wrapper_class")
    for optional_key in ("orchestrator_class_ref", "capability_target"):
        if optional_key in quest:
            entry[optional_key] = quest.get(optional_key)
    return entry

def build_quest_catalog_projection() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for quest_id, path in discover_questbook_files().items():
        payload = load_yaml(path)
        if not isinstance(payload, dict):
            print("[FAIL] questbook writeback surface")
            print(f"  - {path.relative_to(ROOT)} must parse to a mapping")
            raise SystemExit(1)
        entries.append(
            build_expected_quest_catalog_entry(
                payload,
                source_path=path.relative_to(ROOT).as_posix(),
            )
        )
    return entries

def build_quest_dispatch_projection() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for _, path in discover_questbook_files().items():
        payload = load_yaml(path)
        if not isinstance(payload, dict):
            print("[FAIL] questbook writeback surface")
            print(f"  - {path.relative_to(ROOT)} must parse to a mapping")
            raise SystemExit(1)
        entries.append(
            build_expected_quest_dispatch_entry(
                payload,
                source_path=path.relative_to(ROOT).as_posix(),
            )
        )
    return entries
