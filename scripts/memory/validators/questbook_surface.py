"""Quest source and projection checks for the memory-context profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403

from .questbook_discovery import (
    discover_questbook_file_paths,
    discover_questbook_files,
    duplicate_questbook_file_issues,
    quest_anchor_doc_ref,
    quest_path_state,
)
from .questbook_external import (
    external_quest_schema_error,
    validate_orchestrator_class_ref,
)
from .questbook_projection import (
    build_expected_quest_catalog_entry,
    build_expected_quest_dispatch_entry,
)

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
