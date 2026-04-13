#!/usr/bin/env python3
"""Validate bootstrap aoa-memo artifacts.

This script is intentionally small and honest. It validates the current example
objects against the local JSON schemas, checks the local artifact refs they
expose, validates the compact questbook writeback surface, and performs a light
structural check on `generated/memo_registry.min.json`.
"""

from __future__ import annotations

import importlib.util
import json
from datetime import datetime
from functools import lru_cache
import os
from pathlib import Path
import re
import sys

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: jsonschema. Install it with: pip install jsonschema")
    raise SystemExit(2) from exc

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: PyYAML. Install it with: pip install PyYAML")
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parents[1]
AOA_AGENTS_ROOT = Path(os.environ.get("AOA_AGENTS_ROOT", ROOT.parent / "aoa-agents")).expanduser().resolve()
AOA_EVALS_ROOT = Path(os.environ.get("AOA_EVALS_ROOT", ROOT.parent / "aoa-evals")).expanduser().resolve()
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples"
GENERATED = ROOT / "generated"
RUNTIME_WRITEBACK_TARGETS_PATH = GENERATED / "runtime_writeback_targets.min.json"
RUNTIME_WRITEBACK_INTAKE_PATH = GENERATED / "runtime_writeback_intake.min.json"
RUNTIME_WRITEBACK_GOVERNANCE_PATH = GENERATED / "runtime_writeback_governance.min.json"
LIVE_RECEIPT_LOG_PATH = ROOT / ".aoa" / "live_receipts" / "memo-writeback-receipts.jsonl"
RECALL_SURFACE_PREFIX = "repo:aoa-memo/generated/memory_object_catalog.min.json#"
PHASE_ALPHA_WRITEBACK_MAP_PATH = EXAMPLES / "phase_alpha_writeback_map.example.json"
PHASE_ALPHA_WRITEBACK_OUTPUT_PATH = GENERATED / "phase_alpha_writeback_map.min.json"
QUESTBOOK_PATH = ROOT / "QUESTBOOK.md"
QUESTBOOK_DOC = ROOT / "docs" / "QUEST_EVIDENCE_WRITEBACK.md"
ORCHESTRATOR_MEMORY_ALIGNMENT_DOC = ROOT / "docs" / "ORCHESTRATOR_MEMORY_ALIGNMENT.md"
QUEST_CATALOG_PATH = GENERATED / "quest_catalog.min.json"
QUEST_CATALOG_EXAMPLE_PATH = GENERATED / "quest_catalog.min.example.json"
QUEST_DISPATCH_PATH = GENERATED / "quest_dispatch.min.json"
QUEST_DISPATCH_EXAMPLE_PATH = GENERATED / "quest_dispatch.min.example.json"
FOUNDATION_QUESTBOOK_FILES = {
    "AOA-MEM-Q-0001": ROOT / "quests" / "AOA-MEM-Q-0001.yaml",
    "AOA-MEM-Q-0002": ROOT / "quests" / "AOA-MEM-Q-0002.yaml",
}
QUESTBOOK_FILES = FOUNDATION_QUESTBOOK_FILES
CLOSED_QUEST_STATES = {"done", "dropped"}
ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS = {
    "repo_layer_selection",
    "evidence_closure",
    "bounded_next_step",
}
ORCHESTRATOR_MEMORY_QUESTS = {
    "AOA-MEM-Q-0004": ("aoa-agents:router", "repo_layer_selection"),
    "AOA-MEM-Q-0005": ("aoa-agents:review", "evidence_closure"),
    "AOA-MEM-Q-0006": ("aoa-agents:bounded_execution", "bounded_next_step"),
}
ORCHESTRATOR_MEMORY_REQUIRED_TOKENS = (
    "## Router",
    "## Review",
    "## Bounded execution",
    "## Boundary rule",
    "must not redefine orchestrator identity or make memo the owner of active quest state",
)
FORMAT_CHECKER = FormatChecker()
RFC3339_DATETIME = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
README_CURRENT_RELEASE = re.compile(r"Current release:\s+`v(?P<version>\d+\.\d+\.\d+)`")
CHANGELOG_RELEASE_HEADING = re.compile(r"^## \[(?P<version>\d+\.\d+\.\d+)\]", re.MULTILINE)
SYMBOLIC_REF = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*:")
WINDOWS_ABSOLUTE_PATH = re.compile(r"^[A-Za-z]:[\\\\/]")
QUEST_ID_PATTERN = re.compile(r"\bAOA-MEM-Q-\d{4}\b")
CORE_KIND_SCHEMA_MAP = {
    "anchor": "schemas/anchor.schema.json",
    "state_capsule": "schemas/state_capsule.schema.json",
    "episode": "schemas/episode.schema.json",
    "claim": "schemas/claim.schema.json",
    "decision": "schemas/decision.schema.json",
    "pattern": "schemas/pattern.schema.json",
    "bridge": "schemas/bridge.schema.json",
    "audit_event": "schemas/audit_event.schema.json",
}
CORE_KIND_EXAMPLE_MAP = {
    "anchor": "anchor.example.json",
    "state_capsule": "state_capsule.example.json",
    "episode": "episode.example.json",
    "claim": "claim.example.json",
    "decision": "checkpoint_approval_record.example.json",
    "pattern": "pattern.example.json",
    "bridge": "bridge.kag-lift.example.json",
    "audit_event": "audit_event.supersession.example.json",
}
PHASE_ALPHA_OBJECT_EXAMPLES_BY_KIND = {
    "state_capsule": [
        "state_capsule.phase-alpha-local-stack.example.json",
        "state_capsule.phase-alpha-long-horizon.example.json",
        "state_capsule.phase-alpha-restartable-inquiry.example.json",
    ],
    "episode": [
        "episode.phase-alpha-local-stack.example.json",
        "episode.phase-alpha-validation-remediation.example.json",
        "episode.phase-alpha-validation-remediation-rerun.example.json",
        "episode.phase-alpha-long-horizon.example.json",
    ],
    "decision": [
        "decision.phase-alpha-local-stack.example.json",
        "decision.phase-alpha-self-agent-checkpoint.example.json",
        "decision.phase-alpha-validation-remediation.example.json",
        "decision.phase-alpha-validation-remediation-rerun.example.json",
        "decision.phase-alpha-long-horizon.example.json",
        "decision.phase-alpha-restartable-inquiry.example.json",
    ],
    "claim": [
        "claim.phase-alpha-closure-with-residual-runtime-history.example.json",
        "claim.phase-alpha-rerun-pending-handoff.example.json",
        "claim.phase-alpha-runtime-history-fully-retired.example.json",
        "claim.phase-alpha-runtime-history-later-infra-track.example.json",
    ],
    "pattern": [
        "pattern.phase-alpha-remediation-recurrence.example.json",
    ],
    "audit_event": [
        "audit_event.phase-alpha-self-agent-checkpoint.example.json",
        "audit_event.phase-alpha-validation-remediation.example.json",
        "audit_event.phase-alpha-validation-remediation-rerun.example.json",
        "audit_event.phase-alpha-rerun-pending-supersession.example.json",
        "audit_event.phase-alpha-runtime-history-overread-retraction.example.json",
    ],
}
PHASE_ALPHA_OBJECT_EXAMPLE_NAMES = tuple(
    example_name
    for example_names in PHASE_ALPHA_OBJECT_EXAMPLES_BY_KIND.values()
    for example_name in example_names
)
PHASE_ALPHA_PROVENANCE_THREAD_EXAMPLE = "provenance_thread.phase-alpha-curated.example.json"
KAG_EXPORT_REQUIRED_FIELDS = {
    "owner_repo",
    "kind",
    "object_id",
    "primary_question",
    "summary_50",
    "summary_200",
    "source_inputs",
    "entry_surface",
    "section_handles",
    "direct_relations",
    "provenance_note",
    "non_identity_boundary",
}


def load_runtime_writeback_targets_builder():
    module_path = ROOT / "scripts" / "generate_runtime_writeback_targets.py"
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_writeback_targets",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] runtime_writeback_targets.min.json")
        print("  - unable to load runtime writeback target generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_runtime_writeback_intake_builder():
    module_path = ROOT / "scripts" / "generate_runtime_writeback_intake.py"
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_writeback_intake",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] runtime_writeback_intake.min.json")
        print("  - unable to load runtime writeback intake generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_runtime_writeback_governance_builder():
    module_path = ROOT / "scripts" / "generate_runtime_writeback_governance.py"
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_writeback_governance",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] runtime_writeback_governance.min.json")
        print("  - unable to load runtime writeback governance generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_phase_alpha_writeback_builder():
    module_path = ROOT / "scripts" / "generate_phase_alpha_writeback_map.py"
    spec = importlib.util.spec_from_file_location(
        "generate_phase_alpha_writeback_map",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] phase_alpha_writeback_map.min.json")
        print("  - unable to load Phase Alpha writeback map generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def quest_sort_key(quest_id: str) -> tuple[int, str]:
    suffix = quest_id.rsplit("-", 1)[-1]
    try:
        return (int(suffix), quest_id)
    except ValueError:
        return (sys.maxsize, quest_id)


def discover_questbook_files() -> dict[str, Path]:
    discovered = {
        path.stem: path
        for path in (ROOT / "quests").glob("AOA-MEM-Q-*.yaml")
        if path.is_file()
    }
    if not discovered:
        return dict(FOUNDATION_QUESTBOOK_FILES)
    return {
        quest_id: discovered[quest_id]
        for quest_id in sorted(discovered, key=quest_sort_key)
    }


def quest_anchor_doc_ref(data: dict[str, object]) -> str | None:
    anchor_ref = data.get("anchor_ref")
    if isinstance(anchor_ref, str):
        return anchor_ref
    if isinstance(anchor_ref, dict):
        ref_value = anchor_ref.get("ref")
        if isinstance(ref_value, str):
            return ref_value
    return None


def validate_nested_agents_surface() -> None:
    try:
        from validate_nested_agents import validate_nested_agents_docs
    except Exception as exc:  # pragma: no cover - defensive wiring guard
        print("[FAIL] nested AGENTS docs")
        print(f"  - unable to load nested AGENTS validator: {exc}")
        raise SystemExit(1) from exc

    try:
        validate_nested_agents_docs()
    except RuntimeError as exc:
        print("[FAIL] nested AGENTS docs")
        print(f"  - {exc}")
        raise SystemExit(1) from exc

    print("[OK]   nested AGENTS docs")


def validate_questbook_surface() -> None:
    errors: list[str] = []
    questbook_files = discover_questbook_files()
    missing_foundation = [
        quest_id for quest_id in FOUNDATION_QUESTBOOK_FILES if quest_id not in questbook_files
    ]
    required_paths = [QUESTBOOK_PATH, QUESTBOOK_DOC, *FOUNDATION_QUESTBOOK_FILES.values()]
    for path in required_paths:
        if not path.exists():
            errors.append(f"missing file: {path.relative_to(ROOT)}")
    for quest_id in missing_foundation:
        errors.append(f"missing foundation quest file: quests/{quest_id}.yaml")

    questbook_text = ""
    listed_quest_ids: set[str] = set()
    if QUESTBOOK_PATH.exists():
        questbook_text = load_text(QUESTBOOK_PATH)
        listed_quest_ids = set(QUEST_ID_PATTERN.findall(questbook_text))

    if QUESTBOOK_DOC.exists():
        doc_text = load_text(QUESTBOOK_DOC)
        if "WRITEBACK_TEMPERATURE_POLICY.md" not in doc_text:
            errors.append("docs/QUEST_EVIDENCE_WRITEBACK.md must stay anchored to docs/WRITEBACK_TEMPERATURE_POLICY.md")
        lower_doc = doc_text.lower()
        for phrase in (
            "quest state remains source-owned",
            "good writeback candidates",
            "bad writeback candidates",
            "witness trace posture",
        ):
            if phrase not in lower_doc:
                errors.append(f"docs/QUEST_EVIDENCE_WRITEBACK.md must mention {phrase}")

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
            if data.get("owner_surface") != "docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md":
                errors.append(
                    f"{path.relative_to(ROOT)} must keep owner_surface docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md"
                )
            if orchestrator_class_ref != expected_ref:
                errors.append(
                    f"{path.relative_to(ROOT)} must keep orchestrator_class_ref {expected_ref}"
                )
            if capability_target != expected_target:
                errors.append(
                    f"{path.relative_to(ROOT)} must keep capability_target {expected_target}"
                )
        if quest_id in FOUNDATION_QUESTBOOK_FILES:
            if data.get("owner_surface") != "docs/QUEST_EVIDENCE_WRITEBACK.md":
                errors.append(
                    f"{path.relative_to(ROOT)} must keep owner_surface docs/QUEST_EVIDENCE_WRITEBACK.md"
                )
        else:
            anchor_ref = quest_anchor_doc_ref(data)
            if not isinstance(anchor_ref, str) or not anchor_ref.startswith("docs/"):
                errors.append(
                    f"{path.relative_to(ROOT)} must keep anchor_ref within local docs/ for additive memo quests"
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
            errors.append("missing file: docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md")
        else:
            memory_alignment_text = load_text(ORCHESTRATOR_MEMORY_ALIGNMENT_DOC)
            for token in ORCHESTRATOR_MEMORY_REQUIRED_TOKENS:
                if token not in memory_alignment_text:
                    errors.append(
                        f"docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md must mention {token}"
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
        errors.append("missing file: generated/quest_catalog.min.json")
    else:
        if actual_catalog != expected_catalog_entries:
            errors.append("generated/quest_catalog.min.json is out of date or mismatched")
    try:
        actual_catalog_example = load_json(QUEST_CATALOG_EXAMPLE_PATH)
    except FileNotFoundError:
        errors.append("missing file: generated/quest_catalog.min.example.json")
    else:
        if actual_catalog_example != expected_catalog_entries:
            errors.append("generated/quest_catalog.min.example.json is out of date or mismatched")
    try:
        actual_dispatch = load_json(QUEST_DISPATCH_PATH)
    except FileNotFoundError:
        errors.append("missing file: generated/quest_dispatch.min.json")
        actual_dispatch = None
    if isinstance(actual_dispatch, list):
        for index, entry in enumerate(actual_dispatch):
            schema_error = external_quest_schema_error(
                entry,
                AOA_EVALS_ROOT / "schemas" / "quest_dispatch.schema.json",
            )
            if schema_error:
                errors.append(f"generated/quest_dispatch.min.json[{index}] {schema_error}")
        if actual_dispatch != expected_dispatch_entries:
            errors.append("generated/quest_dispatch.min.json is out of date or mismatched")
    elif actual_dispatch is not None:
        errors.append("generated/quest_dispatch.min.json must be an array")
    try:
        actual_dispatch_example = load_json(QUEST_DISPATCH_EXAMPLE_PATH)
    except FileNotFoundError:
        errors.append("missing file: generated/quest_dispatch.min.example.json")
        actual_dispatch_example = None
    if isinstance(actual_dispatch_example, list):
        for index, entry in enumerate(actual_dispatch_example):
            schema_error = external_quest_schema_error(
                entry,
                AOA_EVALS_ROOT / "schemas" / "quest_dispatch.schema.json",
            )
            if schema_error:
                errors.append(f"generated/quest_dispatch.min.example.json[{index}] {schema_error}")
        if actual_dispatch_example != expected_dispatch_entries:
            errors.append("generated/quest_dispatch.min.example.json is out of date or mismatched")
    elif actual_dispatch_example is not None:
        errors.append("generated/quest_dispatch.min.example.json must be an array")

    if errors:
        print("[FAIL] questbook writeback surface")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   questbook writeback surface")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> object:
    return yaml.safe_load(load_text(path))


def format_schema_path(path_parts: list[object]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)


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


@FORMAT_CHECKER.checks("date-time")
def is_rfc3339_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    if not RFC3339_DATETIME.fullmatch(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def markdown_anchor(text: str) -> str:
    anchor = text.strip().lower()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")


@lru_cache(maxsize=None)
def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MARKDOWN_HEADING.match(line)
        if not match:
            continue
        base = markdown_anchor(match.group(2))
        if not base:
            continue
        suffix = seen.get(base, 0)
        seen[base] = suffix + 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors


def local_ref_error(ref_value: object, label: str) -> str | None:
    if not isinstance(ref_value, str) or not ref_value:
        return None
    if ref_value.startswith(("http://", "https://", "repo:")):
        return None
    if SYMBOLIC_REF.match(ref_value) and not WINDOWS_ABSOLUTE_PATH.match(ref_value):
        return None

    path_text, _, anchor = ref_value.partition("#")
    target = ROOT / path_text

    if not target.exists():
        return f"{label}: referenced path does not exist: {ref_value}"
    if anchor and target.suffix.lower() == ".md" and anchor not in markdown_anchors(target):
        return f"{label}: referenced markdown anchor does not exist: {ref_value}"
    return None


def append_ref_errors(errors: list[str], ref_checks: list[tuple[str, object]]) -> None:
    errors.extend(filter(None, (local_ref_error(value, label) for label, value in ref_checks)))


LINEAGE_REF_CHAIN = ("cluster_ref", "candidate_ref", "seed_ref", "object_ref")


def append_lineage_chain_errors(errors: list[str], lineage_refs: object) -> None:
    if not isinstance(lineage_refs, dict):
        return

    for index, field_name in enumerate(LINEAGE_REF_CHAIN):
        value = lineage_refs.get(field_name)
        if value is None:
            continue
        for required_name in LINEAGE_REF_CHAIN[:index]:
            if lineage_refs.get(required_name) is None:
                errors.append(
                    f"lineage_refs.{field_name} requires lineage_refs.{required_name} when later chain links are present"
                )
                break


@lru_cache(maxsize=None)
def schema_registry() -> Registry:
    resources: list[tuple[str, Resource]] = []
    for path in SCHEMAS.glob("*.json"):
        schema = load_json(path)
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            resources.append((schema_id, Resource.from_contents(schema)))
    return Registry().with_resources(resources)


def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(SCHEMAS / schema_name)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FORMAT_CHECKER, registry=schema_registry())


def validate_example(validator: Draft202012Validator, example_name: str) -> None:
    data = load_json(EXAMPLES / example_name)
    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]
    lineage_refs = data.get("lineage_refs")
    if not isinstance(lineage_refs, dict):
        lineage_refs = {}
    lineage_context = data.get("lineage_context")
    if not isinstance(lineage_context, dict):
        lineage_context = {}

    ref_checks = [
        ("payload_ref", data.get("payload_ref")),
        ("bridges.route_capsule_ref", data.get("bridges", {}).get("route_capsule_ref")),
        ("inspect_surface", data.get("inspect_surface")),
        ("capsule_surface", data.get("capsule_surface")),
        ("expand_surface", data.get("expand_surface")),
        ("lineage_refs.cluster_ref", lineage_refs.get("cluster_ref")),
        ("lineage_refs.candidate_ref", lineage_refs.get("candidate_ref")),
        ("lineage_refs.seed_ref", lineage_refs.get("seed_ref")),
        ("lineage_refs.object_ref", lineage_refs.get("object_ref")),
        ("lineage_context.merged_into", lineage_context.get("merged_into")),
    ]
    for list_name in (
        "evidence_pack_refs",
        "contradiction_pack_refs",
        "witness_refs",
        "memory_delta_refs",
        "canon_delta_refs",
    ):
        values = data.get(list_name)
        if not isinstance(values, list):
            continue
        for index, value in enumerate(values):
            ref_checks.append((f"{list_name}[{index}]", value))
    return_pack = data.get("return_pack")
    if isinstance(return_pack, dict):
        for list_name in ("anchor_refs", "reentry_refs"):
            values = return_pack.get(list_name)
            if not isinstance(values, list):
                continue
            for index, value in enumerate(values):
                ref_checks.append((f"return_pack.{list_name}[{index}]", value))
    errors.extend(filter(None, (local_ref_error(value, label) for label, value in ref_checks)))
    append_lineage_chain_errors(errors, lineage_refs)

    if errors:
        print(f"[FAIL] {example_name}")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print(f"[OK]   {example_name}")


def validate_support_schema(schema_name: str) -> None:
    validator_for(schema_name)
    print(f"[OK]   {schema_name}")


def validate_memory_object_profiles() -> None:
    profile_validator = validator_for("memory_object_profile.schema.json")

    for kind, schema_path in CORE_KIND_SCHEMA_MAP.items():
        schema_name = Path(schema_path).name
        example_name = CORE_KIND_EXAMPLE_MAP[kind]
        validate_example(validator_for(schema_name), example_name)
        validate_example(profile_validator, example_name)

    extra_kind_examples = {
        "episode": [
            "checkpoint_health_check.example.json",
            "episode.tos-interpretation.example.json",
        ],
        "claim": [
            "claim.tos-bridge-ready.example.json",
            "claim.current-entrypoint.example.json",
            "claim.superseded.example.json",
            "claim.retracted.example.json",
        ],
        "audit_event": [
            "audit_event.retraction.example.json",
        ],
    }
    for kind, example_names in PHASE_ALPHA_OBJECT_EXAMPLES_BY_KIND.items():
        extra_kind_examples.setdefault(kind, []).extend(example_names)

    for kind, example_names in extra_kind_examples.items():
        schema_name = Path(CORE_KIND_SCHEMA_MAP[kind]).name
        for example_name in example_names:
            validate_example(validator_for(schema_name), example_name)
            validate_example(profile_validator, example_name)


def validate_trust_lifecycle_contracts() -> None:
    registry = load_json(GENERATED / "memo_registry.min.json")
    errors: list[str] = []

    for ref in (
        "docs/MEMORY_TRUST_POSTURE.md",
        "docs/LIFECYCLE.md",
        "schemas/trust_posture.schema.json",
        "schemas/lifecycle_posture.schema.json",
    ):
        if ref.endswith(".md") and ref not in registry.get("core_docs", []):
            errors.append(f"generated/memo_registry.min.json must list {ref}")
        if ref.endswith(".json") and ref not in registry.get("schemas", []):
            errors.append(f"generated/memo_registry.min.json must list {ref}")

    memory_examples = [
        "anchor.example.json",
        "state_capsule.example.json",
        "episode.example.json",
        "episode.tos-interpretation.example.json",
        "claim.example.json",
        "claim.current-entrypoint.example.json",
        "claim.superseded.example.json",
        "claim.retracted.example.json",
        "claim.tos-bridge-ready.example.json",
        "checkpoint_approval_record.example.json",
        "checkpoint_health_check.example.json",
        "pattern.example.json",
        "bridge.kag-lift.example.json",
        "audit_event.supersession.example.json",
        "audit_event.retraction.example.json",
    ]
    memory_examples.extend(PHASE_ALPHA_OBJECT_EXAMPLE_NAMES)

    for example_name in memory_examples:
        data = load_json(EXAMPLES / example_name)
        trust = data.get("trust", {})
        lifecycle = data.get("lifecycle", {})
        current_recall = lifecycle.get("current_recall", {})

        if trust.get("temperature") == "frozen" and lifecycle.get("review_state") != "frozen":
            errors.append(f"{example_name} must keep lifecycle.review_state == 'frozen' when trust.temperature == 'frozen'")
        if current_recall.get("status") == "withdrawn" and lifecycle.get("review_state") != "retracted":
            errors.append(f"{example_name} withdrawn current_recall posture must stay tied to review_state 'retracted'")

    if errors:
        print("[FAIL] trust/lifecycle contract surfaces")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   trust/lifecycle contract surfaces")


def validate_memory_object_surface_manifest() -> None:
    validator = validator_for("memory_object_surface_manifest.schema.json")
    data = load_json(EXAMPLES / "memory_object_surface_manifest.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    seen_paths: set[str] = set()
    for index, entry in enumerate(data.get("entries", [])):
        path = entry.get("example_path")
        if path in seen_paths:
            errors.append(f"entries[{index}].example_path duplicates {path}")
        if isinstance(path, str):
            seen_paths.add(path)
        error = local_ref_error(path, f"entries[{index}].example_path")
        if error:
            errors.append(error)

    if errors:
        print("[FAIL] memory_object_surface_manifest.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   memory_object_surface_manifest.json")


def validate_recall_contract_example(
    example_name: str,
    *,
    expected_mode: str,
    expected_allowed_scopes: list[str],
    expected_preferred_kinds: list[str],
    expected_temperature_order: list[str],
    expected_inspect_surface: str,
    expected_expand_surface: str,
    expected_source_route_required: bool,
    expected_capsule_surface: str | None = None,
    expected_checkpoint_continuity_supported: bool | None = None,
    expected_return_ready: bool | None = None,
    expected_preferred_anchor_kinds: list[str] | None = None,
    expected_support_artifact_refs: list[str] | None = None,
) -> None:
    validator = validator_for("recall_contract.schema.json")
    data = load_json(EXAMPLES / example_name)

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]
    support_artifact_refs = data.get("support_artifact_refs")
    if not isinstance(support_artifact_refs, list):
        support_artifact_refs = []
    append_ref_errors(
        errors,
        [
            ("inspect_surface", data.get("inspect_surface")),
            ("capsule_surface", data.get("capsule_surface")),
            ("expand_surface", data.get("expand_surface")),
        ]
        + [
            (f"support_artifact_refs[{index}]", value)
            for index, value in enumerate(support_artifact_refs)
        ],
    )

    if data.get("mode") != expected_mode:
        errors.append(f"{example_name} mode must stay '{expected_mode}'")
    if data.get("allowed_scopes") != expected_allowed_scopes:
        errors.append(f"{example_name} allowed_scopes must stay {expected_allowed_scopes}")
    if data.get("preferred_kinds") != expected_preferred_kinds:
        errors.append(f"{example_name} preferred_kinds must stay {expected_preferred_kinds}")
    if data.get("temperature_order") != expected_temperature_order:
        errors.append(f"{example_name} temperature_order must stay {expected_temperature_order}")
    if data.get("inspect_surface") != expected_inspect_surface:
        errors.append(f"{example_name} inspect_surface must stay {expected_inspect_surface}")
    if expected_capsule_surface is not None and data.get("capsule_surface") != expected_capsule_surface:
        errors.append(f"{example_name} capsule_surface must stay {expected_capsule_surface}")
    if data.get("expand_surface") != expected_expand_surface:
        errors.append(f"{example_name} expand_surface must stay {expected_expand_surface}")
    if data.get("source_route_required") is not expected_source_route_required:
        errors.append(f"{example_name} source_route_required must stay {expected_source_route_required}")
    if expected_checkpoint_continuity_supported is not None and data.get("checkpoint_continuity_supported") is not expected_checkpoint_continuity_supported:
        errors.append(
            f"{example_name} checkpoint_continuity_supported must stay {expected_checkpoint_continuity_supported}"
        )
    if expected_return_ready is not None and data.get("return_ready") is not expected_return_ready:
        errors.append(f"{example_name} return_ready must stay {expected_return_ready}")
    if expected_preferred_anchor_kinds is not None and data.get("preferred_anchor_kinds") != expected_preferred_anchor_kinds:
        errors.append(f"{example_name} preferred_anchor_kinds must stay {expected_preferred_anchor_kinds}")
    if expected_support_artifact_refs is not None and data.get("support_artifact_refs") != expected_support_artifact_refs:
        errors.append(f"{example_name} support_artifact_refs must stay {expected_support_artifact_refs}")

    if errors:
        print(f"[FAIL] {example_name}")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print(f"[OK]   {example_name}")


def validate_registry() -> None:
    data = load_json(GENERATED / "memo_registry.min.json")
    required = [
        "layer",
        "version",
        "status",
        "memory_object_kinds",
        "supporting_objects",
        "recall_modes",
        "temperature_scale",
        "core_docs",
        "schemas",
        "generated_surface_families",
        "validation_commands",
    ]
    missing = [key for key in required if key not in data]
    errors = [f"missing key: {key}" for key in missing]

    registry_version = data.get("version")
    readme_release = README_CURRENT_RELEASE.search(load_text(ROOT / "README.md"))
    changelog_release = CHANGELOG_RELEASE_HEADING.search(load_text(ROOT / "CHANGELOG.md"))
    roadmap = load_text(ROOT / "ROADMAP.md")
    if not isinstance(registry_version, str) or not registry_version:
        errors.append("generated/memo_registry.min.json version must be a non-empty string")
    if readme_release is None:
        errors.append("README.md must publish a Current release line")
    if changelog_release is None:
        errors.append("CHANGELOG.md must publish at least one numeric release heading")
    if isinstance(registry_version, str) and readme_release is not None:
        readme_version = readme_release.group("version")
        if registry_version != readme_version:
            errors.append(
                "generated/memo_registry.min.json version must match README.md current release "
                f"{readme_version!r}"
            )
        if f"`v{registry_version}`" not in roadmap:
            errors.append(
                "ROADMAP.md must mention the current memo registry release as "
                f"`v{registry_version}`"
            )
    if isinstance(registry_version, str) and changelog_release is not None:
        changelog_version = changelog_release.group("version")
        if registry_version != changelog_version:
            errors.append(
                "generated/memo_registry.min.json version must match CHANGELOG.md latest release "
                f"{changelog_version!r}"
            )

    for key in ("core_docs", "schemas"):
        for index, ref in enumerate(data.get(key, [])):
            error = local_ref_error(ref, f"{key}[{index}]")
            if error:
                errors.append(error)

    expected_schemas = {
        "schemas/failure_lesson_memory_v1.json",
        "schemas/memory_object_surface_manifest.schema.json",
        "schemas/memory_object_catalog.schema.json",
        "schemas/memory_object_capsules.schema.json",
        "schemas/memory_object_sections.schema.json",
        "schemas/recovery_pattern_memory_v1.json",
    }
    for schema_ref in sorted(expected_schemas):
        if schema_ref not in data.get("schemas", []):
            errors.append(f"generated/memo_registry.min.json must list {schema_ref}")
    required_core_docs = (
        "docs/FAILURE_LESSON_MEMORY.md",
        "docs/FAILURE_LESSON_RECALL.md",
        "docs/RECOVERY_PATTERN_MEMORY.md",
        "docs/RECOVERY_PATTERN_RECALL.md",
        "docs/GROWTH_REFINERY_WRITEBACK.md",
        "docs/QUEST_CHRONICLE_WRITEBACK.md",
        "docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
        "docs/KAG_SOURCE_EXPORT.md",
    )
    for doc_ref in required_core_docs:
        if doc_ref not in data.get("core_docs", []):
            errors.append(f"generated/memo_registry.min.json must list {doc_ref}")

    families = {
        item.get("family"): item
        for item in data.get("generated_surface_families", [])
        if isinstance(item, dict) and isinstance(item.get("family"), str)
    }
    if "doctrine" not in families:
        errors.append("generated/memo_registry.min.json must publish doctrine generated_surface_families entry")
    if "memory_objects" not in families:
        errors.append("generated/memo_registry.min.json must publish memory_objects generated_surface_families entry")
    if "kag_export" not in families:
        errors.append("generated/memo_registry.min.json must publish kag_export generated_surface_families entry")

    doctrine = families.get("doctrine", {})
    doctrine_outputs = [
        "generated/memory_catalog.json",
        "generated/memory_catalog.min.json",
        "generated/memory_capsules.json",
        "generated/memory_sections.full.json",
    ]
    if doctrine.get("source_of_truth") != "aoa-memo-doctrine-route-surfaces-v1":
        errors.append("doctrine generated_surface_families entry must keep source_of_truth aoa-memo-doctrine-route-surfaces-v1")
    if doctrine.get("outputs") != doctrine_outputs:
        errors.append("doctrine generated_surface_families entry must list the doctrine output family")
    if doctrine.get("validator_command") != "python scripts/validate_memory_surfaces.py":
        errors.append("doctrine generated_surface_families entry must keep validator_command python scripts/validate_memory_surfaces.py")

    memory_objects = families.get("memory_objects", {})
    object_outputs = [
        "generated/memory_object_catalog.json",
        "generated/memory_object_catalog.min.json",
        "generated/memory_object_capsules.json",
        "generated/memory_object_sections.full.json",
    ]
    if memory_objects.get("source_of_truth") != "aoa-memo-object-example-surfaces-v1":
        errors.append("memory_objects generated_surface_families entry must keep source_of_truth aoa-memo-object-example-surfaces-v1")
    if memory_objects.get("manifest") != "examples/memory_object_surface_manifest.json":
        errors.append("memory_objects generated_surface_families entry must list examples/memory_object_surface_manifest.json as the manifest")
    if memory_objects.get("outputs") != object_outputs:
        errors.append("memory_objects generated_surface_families entry must list the object output family")
    if memory_objects.get("generator_command") != "python scripts/generate_memory_object_surfaces.py":
        errors.append("memory_objects generated_surface_families entry must keep generator_command python scripts/generate_memory_object_surfaces.py")
    if memory_objects.get("validator_command") != "python scripts/validate_memory_object_surfaces.py":
        errors.append("memory_objects generated_surface_families entry must keep validator_command python scripts/validate_memory_object_surfaces.py")

    kag_export = families.get("kag_export", {})
    if kag_export.get("source_of_truth") != "aoa-memo-kag-source-export-v1":
        errors.append("kag_export generated_surface_families entry must keep source_of_truth aoa-memo-kag-source-export-v1")
    if kag_export.get("outputs") != ["generated/kag_export.min.json"]:
        errors.append("kag_export generated_surface_families entry must list generated/kag_export.min.json")
    if kag_export.get("generator_command") != "python scripts/generate_kag_export.py":
        errors.append("kag_export generated_surface_families entry must keep generator_command python scripts/generate_kag_export.py")
    if kag_export.get("validator_command") != "python scripts/validate_memo.py":
        errors.append("kag_export generated_surface_families entry must keep validator_command python scripts/validate_memo.py")

    for family_name, family in families.items():
        manifest = family.get("manifest")
        if manifest is not None:
            error = local_ref_error(manifest, f"generated_surface_families.{family_name}.manifest")
            if error:
                errors.append(error)
        for index, ref in enumerate(family.get("outputs", [])):
            error = local_ref_error(ref, f"generated_surface_families.{family_name}.outputs[{index}]")
            if error:
                errors.append(error)

    required_validation_commands = {
        "python scripts/validate_memo.py",
        "python scripts/validate_memory_surfaces.py",
        "python scripts/validate_memory_object_surfaces.py",
        "python scripts/validate_lifecycle_audit_examples.py",
    }
    missing_commands = sorted(required_validation_commands - set(data.get("validation_commands", [])))
    if missing_commands:
        errors.append("generated/memo_registry.min.json missing validation commands: " + ", ".join(missing_commands))

    if errors:
        print("[FAIL] generated/memo_registry.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   generated/memo_registry.min.json")


def validate_core_memory_contract() -> None:
    validator = validator_for("core-memory-contract.schema.json")
    data = load_json(EXAMPLES / "core_memory_contract.example.json")
    registry = load_json(GENERATED / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    expected_core = registry.get("memory_object_kinds", [])
    expected_supporting = registry.get("supporting_objects", [])
    expected_profile_schema = "schemas/memory_object_profile.schema.json"
    expected_kind_schemas = CORE_KIND_SCHEMA_MAP

    append_ref_errors(
        errors,
        [("profile_schema", data.get("profile_schema"))]
        + [
            (f"kind_profile_schemas.{kind}", ref)
            for kind, ref in data.get("kind_profile_schemas", {}).items()
        ],
    )

    if sorted(data.get("core_memory_surfaces", [])) != sorted(expected_core):
        errors.append("core_memory_surfaces does not match generated/memo_registry.min.json memory_object_kinds")
    if sorted(data.get("supporting_objects", [])) != sorted(expected_supporting):
        errors.append("supporting_objects does not match generated/memo_registry.min.json supporting_objects")
    if data.get("profile_schema") != expected_profile_schema:
        errors.append("profile_schema must stay schemas/memory_object_profile.schema.json")
    if data.get("kind_profile_schemas") != expected_kind_schemas:
        errors.append("kind_profile_schemas does not match the shipped per-kind profile schema map")

    for ref in [expected_profile_schema, *expected_kind_schemas.values()]:
        if ref not in registry.get("schemas", []):
            errors.append(f"generated/memo_registry.min.json must list {ref}")
    if "docs/MEMORY_OBJECT_PROFILES.md" not in registry.get("core_docs", []):
        errors.append("generated/memo_registry.min.json must list docs/MEMORY_OBJECT_PROFILES.md")

    if errors:
        print("[FAIL] core_memory_contract.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   core_memory_contract.example.json")


def validate_witness_trace_contract() -> None:
    validator = validator_for("witness-trace.schema.json")
    data = load_json(EXAMPLES / "witness_trace.example.json")
    registry = load_json(GENERATED / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    if "witness_trace" in registry.get("memory_object_kinds", []):
        errors.append("witness_trace must not appear in generated/memo_registry.min.json memory_object_kinds")
    if "witness_trace" in registry.get("supporting_objects", []):
        errors.append("witness_trace must not appear in generated/memo_registry.min.json supporting_objects")
    if "schemas/witness-trace.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memo_registry.min.json must list schemas/witness-trace.schema.json")
    if "docs/WITNESS_TRACE_CONTRACT.md" not in registry.get("core_docs", []):
        errors.append("generated/memo_registry.min.json must list docs/WITNESS_TRACE_CONTRACT.md")

    if not any(step.get("kind") == "tool" for step in data.get("steps", [])):
        errors.append("witness_trace.example.json must include at least one tool-visible step")
    if not any("state_delta" in step for step in data.get("steps", [])):
        errors.append("witness_trace.example.json must include at least one state_delta example")
    summary_output = data.get("summary_output", {})
    if summary_output.get("format") != "markdown":
        errors.append("witness_trace.example.json summary_output.format must stay 'markdown'")

    if errors:
        print("[FAIL] witness_trace.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   witness_trace.example.json")


def validate_checkpoint_to_memory_contract() -> None:
    validator = validator_for("checkpoint-to-memory-contract.schema.json")
    data = load_json(EXAMPLES / "checkpoint_to_memory_contract.example.json")
    registry = load_json(GENERATED / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    ref_checks = [("source_seed_ref", data.get("source_seed_ref"))]
    checkpoint_artifact = data.get("checkpoint_artifact", {})
    if isinstance(checkpoint_artifact, dict):
        ref_checks.append(("checkpoint_artifact.schema_ref", checkpoint_artifact.get("schema_ref")))
    runtime_boundary = data.get("runtime_boundary", {})
    if isinstance(runtime_boundary, dict):
        for index, value in enumerate(runtime_boundary.get("review_boundary_refs", [])):
            ref_checks.append((f"runtime_boundary.review_boundary_refs[{index}]", value))
    for index, rule in enumerate(data.get("mapping_rules", [])):
        if not isinstance(rule, dict):
            continue
        for ref_index, value in enumerate(rule.get("runtime_refs", [])):
            ref_checks.append((f"mapping_rules[{index}].runtime_refs[{ref_index}]", value))
    append_ref_errors(errors, ref_checks)

    if data.get("contract_type") != "checkpoint_to_memory_contract":
        errors.append("checkpoint_to_memory_contract.example.json contract_type must stay 'checkpoint_to_memory_contract'")
    if checkpoint_artifact.get("artifact_name") != "inquiry_checkpoint":
        errors.append("checkpoint_to_memory_contract.example.json must keep inquiry_checkpoint as the checkpoint artifact")
    if runtime_boundary.get("scratchpad_posture") != "runtime_local_only":
        errors.append("runtime scratchpad posture must stay runtime_local_only")
    if runtime_boundary.get("checkpoint_export_kind") != "state_capsule":
        errors.append("checkpoint export kind must stay state_capsule")
    if runtime_boundary.get("distillation_review_posture") != "review_required":
        errors.append("distillation review posture must stay review_required")

    expected_pairs = {
        ("checkpoint_export", "state_capsule"),
        ("approval_record", "decision"),
        ("transition_record", "decision"),
        ("execution_trace", "episode"),
        ("review_trace", "audit_event"),
        ("distillation_claim_candidate", "claim"),
        ("distillation_pattern_candidate", "pattern"),
        ("distillation_bridge_candidate", "bridge"),
    }
    seen_pairs = {
        (rule.get("runtime_surface"), rule.get("target_kind"))
        for rule in data.get("mapping_rules", [])
        if isinstance(rule, dict)
    }
    missing_pairs = sorted(expected_pairs - seen_pairs)
    if missing_pairs:
        errors.append(
            "checkpoint_to_memory_contract.example.json is missing required runtime-to-memo mappings: "
            + ", ".join(f"{surface}->{kind}" for surface, kind in missing_pairs)
        )

    runtime_surface_targets: dict[str, set[str]] = {}
    for rule in data.get("mapping_rules", []):
        if not isinstance(rule, dict):
            continue
        runtime_surface = rule.get("runtime_surface")
        target_kind = rule.get("target_kind")
        if not isinstance(runtime_surface, str) or not isinstance(target_kind, str):
            continue
        runtime_surface_targets.setdefault(runtime_surface, set()).add(target_kind)
    conflicting_runtime_mappings = {
        runtime_surface: sorted(target_kinds)
        for runtime_surface, target_kinds in runtime_surface_targets.items()
        if len(target_kinds) > 1
    }
    for runtime_surface, target_kinds in sorted(conflicting_runtime_mappings.items()):
        errors.append(
            "checkpoint_to_memory_contract.example.json has conflicting target kinds for "
            f"{runtime_surface}: {', '.join(target_kinds)}"
        )

    for target_kind in ("claim", "pattern", "bridge"):
        matching_rules = [
            rule
            for rule in data.get("mapping_rules", [])
            if isinstance(rule, dict) and rule.get("target_kind") == target_kind
        ]
        if not matching_rules:
            continue
        for rule in matching_rules:
            if rule.get("writeback_class") != "reviewed_candidate":
                errors.append(f"{target_kind} mappings must stay reviewed_candidate writeback")
            if rule.get("requires_human_review") is not True:
                errors.append(f"{target_kind} mappings must require human review")

    if "schemas/checkpoint-to-memory-contract.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memo_registry.min.json must list schemas/checkpoint-to-memory-contract.schema.json")
    if "docs/RUNTIME_WRITEBACK_SEAM.md" not in registry.get("core_docs", []):
        errors.append("generated/memo_registry.min.json must list docs/RUNTIME_WRITEBACK_SEAM.md")

    if errors:
        print("[FAIL] checkpoint_to_memory_contract.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   checkpoint_to_memory_contract.example.json")


def validate_runtime_writeback_targets() -> None:
    validator = validator_for("runtime-writeback-targets.schema.json")
    builder = load_runtime_writeback_targets_builder()
    expected = builder.build_runtime_writeback_targets_payload()
    data = load_json(RUNTIME_WRITEBACK_TARGETS_PATH)
    contract = load_json(EXAMPLES / "checkpoint_to_memory_contract.example.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    if data != expected:
        errors.append(
            "generated/runtime_writeback_targets.min.json is out of date; "
            "run scripts/generate_runtime_writeback_targets.py"
        )

    if data.get("contract_id") != "aoa-memo.runtime-writeback.v1":
        errors.append("generated/runtime_writeback_targets.min.json must keep contract_id aoa-memo.runtime-writeback.v1")
    if data.get("source_of_truth") != "examples/checkpoint_to_memory_contract.example.json":
        errors.append("generated/runtime_writeback_targets.min.json must keep source_of_truth examples/checkpoint_to_memory_contract.example.json")
    if data.get("runtime_boundary") != contract.get("runtime_boundary", {}):
        errors.append("generated/runtime_writeback_targets.min.json must keep runtime_boundary aligned with checkpoint_to_memory_contract.example.json")

    targets = data.get("targets")
    if not isinstance(targets, list):
        errors.append("generated/runtime_writeback_targets.min.json targets must be a list")
    else:
        expected_targets = contract.get("mapping_rules", [])
        if len(targets) != len(expected_targets):
            errors.append("generated/runtime_writeback_targets.min.json must include every mapping rule exactly once")
        runtime_surfaces = [
            target.get("runtime_surface")
            for target in targets
            if isinstance(target, dict) and isinstance(target.get("runtime_surface"), str)
        ]
        if len(runtime_surfaces) != len(set(runtime_surfaces)):
            errors.append("generated/runtime_writeback_targets.min.json must not duplicate runtime_surface entries")
        for index, target in enumerate(targets):
            if not isinstance(target, dict):
                errors.append(f"targets[{index}] must be an object")
                continue
            runtime_surface = target.get("runtime_surface")
            if not isinstance(runtime_surface, str):
                continue
            matching_rule = next(
                (
                    rule
                    for rule in expected_targets
                    if isinstance(rule, dict) and rule.get("runtime_surface") == runtime_surface
                ),
                None,
            )
            if matching_rule is None:
                errors.append(f"targets[{index}] references unknown runtime_surface {runtime_surface!r}")
                continue
            for field_name in (
                "target_kind",
                "writeback_class",
                "requires_human_review",
                "review_state_default",
                "runtime_refs",
                "notes",
            ):
                if target.get(field_name) != matching_rule.get(field_name):
                    errors.append(
                        f"targets[{index}].{field_name} must stay aligned with checkpoint_to_memory_contract.example.json"
                    )
            runtime_refs = target.get("runtime_refs")
            if not isinstance(runtime_refs, list) or not runtime_refs or not all(
                isinstance(item, str) and item for item in runtime_refs
            ):
                errors.append(f"targets[{index}].runtime_refs must stay a non-empty string list")

            if target.get("writeback_class") == "reviewed_candidate":
                if target.get("review_state_default") != "proposed":
                    errors.append(f"targets[{index}].review_state_default must stay 'proposed' for reviewed_candidate mappings")
                if target.get("requires_human_review") is not True:
                    errors.append(f"targets[{index}].requires_human_review must stay true for reviewed_candidate mappings")

    if errors:
        print("[FAIL] runtime_writeback_targets.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   runtime_writeback_targets.min.json")


def validate_runtime_writeback_intake() -> None:
    builder = load_runtime_writeback_intake_builder()
    expected = builder.build_runtime_writeback_intake_payload()
    data = load_json(RUNTIME_WRITEBACK_INTAKE_PATH)
    target_surface = load_json(RUNTIME_WRITEBACK_TARGETS_PATH)

    errors: list[str] = []
    if data != expected:
        errors.append(
            "generated/runtime_writeback_intake.min.json is out of date; "
            "run scripts/generate_runtime_writeback_intake.py"
        )

    expected_source_of_truth = {
        "runtime_writeback_targets": "generated/runtime_writeback_targets.min.json",
        "checkpoint_to_memory_contract": "examples/checkpoint_to_memory_contract.example.json",
        "runtime_writeback_seam": "docs/RUNTIME_WRITEBACK_SEAM.md",
        "quest_evidence_writeback": "docs/QUEST_EVIDENCE_WRITEBACK.md",
    }
    if data.get("source_of_truth") != expected_source_of_truth:
        errors.append("generated/runtime_writeback_intake.min.json must keep the canonical source_of_truth map")

    targets = data.get("targets")
    source_targets = target_surface.get("targets") if isinstance(target_surface, dict) else None
    if not isinstance(targets, list):
        errors.append("generated/runtime_writeback_intake.min.json targets must be a list")
    elif not isinstance(source_targets, list):
        errors.append("generated/runtime_writeback_intake.min.json requires generated/runtime_writeback_targets.min.json targets")
    else:
        if len(targets) != len(source_targets):
            errors.append("generated/runtime_writeback_intake.min.json must include every runtime writeback target exactly once")
        source_by_surface = {
            item.get("runtime_surface"): item
            for item in source_targets
            if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
        }
        seen_runtime_surfaces: set[str] = set()
        for index, item in enumerate(targets):
            if not isinstance(item, dict):
                errors.append(f"targets[{index}] must be an object")
                continue
            runtime_surface = item.get("runtime_surface")
            if not isinstance(runtime_surface, str):
                errors.append(f"targets[{index}].runtime_surface must be a non-empty string")
                continue
            if runtime_surface in seen_runtime_surfaces:
                errors.append(f"targets[{index}].runtime_surface duplicates {runtime_surface!r}")
                continue
            seen_runtime_surfaces.add(runtime_surface)

            source_item = source_by_surface.get(runtime_surface)
            if source_item is None:
                errors.append(f"targets[{index}] references unknown runtime_surface {runtime_surface!r}")
                continue

            for field_name in (
                "target_kind",
                "writeback_class",
                "requires_human_review",
                "review_state_default",
                "runtime_refs",
            ):
                if item.get(field_name) != source_item.get(field_name):
                    errors.append(
                        f"targets[{index}].{field_name} must stay aligned with generated/runtime_writeback_targets.min.json"
                    )

            owner_review_refs = item.get("owner_review_refs")
            if not isinstance(owner_review_refs, list) or not owner_review_refs or not all(
                isinstance(ref, str) and ref for ref in owner_review_refs
            ):
                errors.append(f"targets[{index}].owner_review_refs must stay a non-empty string list")
            else:
                if "docs/RUNTIME_WRITEBACK_SEAM.md" not in owner_review_refs:
                    errors.append(f"targets[{index}].owner_review_refs must include docs/RUNTIME_WRITEBACK_SEAM.md")
                if "docs/QUEST_EVIDENCE_WRITEBACK.md" not in owner_review_refs:
                    errors.append(f"targets[{index}].owner_review_refs must include docs/QUEST_EVIDENCE_WRITEBACK.md")

            writeback_class = item.get("writeback_class")
            requires_human_review = item.get("requires_human_review")
            expected_posture = (
                "review_candidate_only"
                if writeback_class == "reviewed_candidate"
                else "review_before_writeback"
                if requires_human_review is True
                else "capturable_runtime_export"
            )
            if item.get("intake_posture") != expected_posture:
                errors.append(f"targets[{index}].intake_posture must stay {expected_posture!r}")

            if writeback_class == "reviewed_candidate":
                if requires_human_review is not True:
                    errors.append(f"targets[{index}].requires_human_review must stay true for reviewed_candidate mappings")
                if item.get("review_state_default") != "proposed":
                    errors.append(f"targets[{index}].review_state_default must stay 'proposed' for reviewed_candidate mappings")

    if errors:
        print("[FAIL] runtime_writeback_intake.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   runtime_writeback_intake.min.json")


def validate_runtime_writeback_governance() -> None:
    builder = load_runtime_writeback_governance_builder()
    expected = builder.build_runtime_writeback_governance_payload()
    data = load_json(RUNTIME_WRITEBACK_GOVERNANCE_PATH)
    target_surface = load_json(RUNTIME_WRITEBACK_TARGETS_PATH)
    intake_surface = load_json(RUNTIME_WRITEBACK_INTAKE_PATH)

    errors: list[str] = []
    if data != expected:
        errors.append(
            "generated/runtime_writeback_governance.min.json is out of date; "
            "run scripts/generate_runtime_writeback_governance.py"
        )
    if data.get("schema_version") != 1:
        errors.append("generated/runtime_writeback_governance.min.json must declare schema_version 1")
    if data.get("layer") != "aoa-memo":
        errors.append("generated/runtime_writeback_governance.min.json must declare layer aoa-memo")
    if data.get("scope") != "runtime-writeback":
        errors.append("generated/runtime_writeback_governance.min.json must declare scope runtime-writeback")

    expected_source_of_truth = {
        "runtime_writeback_targets": "generated/runtime_writeback_targets.min.json",
        "runtime_writeback_intake": "generated/runtime_writeback_intake.min.json",
    }
    if data.get("source_of_truth") != expected_source_of_truth:
        errors.append("generated/runtime_writeback_governance.min.json must keep the canonical source_of_truth map")

    targets = data.get("targets")
    source_targets = target_surface.get("targets") if isinstance(target_surface, dict) else None
    intake_targets = intake_surface.get("targets") if isinstance(intake_surface, dict) else None
    if not isinstance(targets, list):
        errors.append("generated/runtime_writeback_governance.min.json targets must be a list")
    elif not isinstance(source_targets, list) or not isinstance(intake_targets, list):
        errors.append(
            "generated/runtime_writeback_governance.min.json requires runtime writeback target and intake surfaces"
        )
    else:
        source_by_surface = {
            item.get("runtime_surface"): item
            for item in source_targets
            if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
        }
        intake_by_surface = {
            item.get("runtime_surface"): item
            for item in intake_targets
            if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
        }
        expected_surfaces = sorted(set(source_by_surface) | set(intake_by_surface))
        actual_surfaces = [
            item.get("runtime_surface")
            for item in targets
            if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
        ]
        if actual_surfaces != expected_surfaces:
            errors.append("generated/runtime_writeback_governance.min.json must cover every runtime writeback surface exactly once")
        if len(actual_surfaces) != len(set(actual_surfaces)):
            errors.append("generated/runtime_writeback_governance.min.json must not duplicate runtime_surface entries")

        for index, item in enumerate(targets):
            if not isinstance(item, dict):
                errors.append(f"targets[{index}] must be an object")
                continue
            runtime_surface = item.get("runtime_surface")
            if not isinstance(runtime_surface, str):
                errors.append(f"targets[{index}].runtime_surface must be a non-empty string")
                continue

            source_item = source_by_surface.get(runtime_surface)
            intake_item = intake_by_surface.get(runtime_surface)
            if item.get("in_writeback_targets") is not (source_item is not None):
                errors.append(f"targets[{index}].in_writeback_targets must reflect generated/runtime_writeback_targets.min.json")
            if item.get("in_writeback_intake") is not (intake_item is not None):
                errors.append(f"targets[{index}].in_writeback_intake must reflect generated/runtime_writeback_intake.min.json")

            if source_item is None:
                errors.append(f"targets[{index}] references missing runtime writeback target {runtime_surface!r}")
                continue
            if intake_item is None:
                errors.append(f"targets[{index}] references missing runtime writeback intake {runtime_surface!r}")
                continue

            for field_name in (
                "target_kind",
                "writeback_class",
                "requires_human_review",
                "review_state_default",
            ):
                if item.get(field_name) != source_item.get(field_name):
                    errors.append(
                        f"targets[{index}].{field_name} must match generated/runtime_writeback_targets.min.json"
                    )
                if item.get(field_name) != intake_item.get(field_name):
                    errors.append(
                        f"targets[{index}].{field_name} must match generated/runtime_writeback_intake.min.json"
                    )

            intake_posture = item.get("intake_posture")
            if intake_posture != intake_item.get("intake_posture"):
                errors.append(
                    f"targets[{index}].intake_posture must match generated/runtime_writeback_intake.min.json"
                )
            if not isinstance(intake_posture, str) or not intake_posture:
                errors.append(f"targets[{index}].intake_posture must be a non-empty string")

            blockers = item.get("blockers")
            if not isinstance(blockers, list) or not all(isinstance(entry, str) for entry in blockers):
                errors.append(f"targets[{index}].blockers must be a list of strings")
                continue
            if item.get("governance_passed") is not (len(blockers) == 0):
                errors.append(f"targets[{index}].governance_passed must reflect whether blockers is empty")
            if blockers:
                errors.append(f"targets[{index}] must not carry blockers in the committed governance surface")

    if errors:
        print("[FAIL] runtime_writeback_governance.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   runtime_writeback_governance.min.json")


def validate_live_receipt_log() -> None:
    if not LIVE_RECEIPT_LOG_PATH.exists():
        print("[OK]   live receipt log absent")
        return

    catalog = load_json(GENERATED / "memory_object_catalog.min.json")
    runtime_targets = load_json(RUNTIME_WRITEBACK_TARGETS_PATH)
    catalog_entries_by_id = {
        item["id"]: item
        for item in catalog.get("memory_objects", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    runtime_targets_by_surface = {
        item["runtime_surface"]: item
        for item in runtime_targets.get("targets", [])
        if isinstance(item, dict) and isinstance(item.get("runtime_surface"), str)
    }
    catalog_ids = set(catalog_entries_by_id)
    errors: list[str] = []
    seen_event_ids: set[str] = set()

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

        if receipt.get("event_kind") != "memo_writeback_receipt":
            errors.append(
                f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: event_kind must equal 'memo_writeback_receipt'"
            )

        object_ref = receipt.get("object_ref")
        object_id = object_ref.get("id") if isinstance(object_ref, dict) else None
        if not isinstance(object_ref, dict):
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref must be an object")
        else:
            if object_ref.get("repo") != "aoa-memo":
                errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.repo must equal 'aoa-memo'")
            if object_ref.get("kind") != "memory_object":
                errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.kind must equal 'memory_object'")
            if not isinstance(object_id, str) or not object_id:
                errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.id must be a non-empty string")
            elif object_id not in catalog_ids:
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: object_ref.id {object_id!r} "
                    "is absent from generated/memory_object_catalog.min.json"
                )

        payload = receipt.get("payload")
        if not isinstance(payload, dict):
            errors.append(f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload must be an object")
        else:
            for field in ("target_kind", "writeback_class", "review_state"):
                if not isinstance(payload.get(field), str) or not payload[field]:
                    errors.append(
                        f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: payload.{field} "
                        "must be a non-empty string"
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
                    elif memory_object_ref != catalog_entry.get("source_path"):
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
                                f"{runtime_surface!r} is absent from generated/runtime_writeback_targets.min.json"
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
            local_path = ROOT / path_text
            if not local_path.exists():
                errors.append(
                    f"{LIVE_RECEIPT_LOG_PATH}:{line_number}: evidence_refs[{evidence_index}].ref "
                    f"points to missing local path {path_text!r}"
                )
                continue
            if path_text == "generated/memory_object_catalog.min.json":
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
        if isinstance(object_id, str) and object_id in catalog_ids:
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

    if errors:
        print("[FAIL] live receipt log")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   live receipt log")


def validate_phase_alpha_writeback_map() -> None:
    builder = load_phase_alpha_writeback_builder()
    expected = builder.build_phase_alpha_writeback_map_payload()
    data = load_json(PHASE_ALPHA_WRITEBACK_OUTPUT_PATH)
    source = load_json(PHASE_ALPHA_WRITEBACK_MAP_PATH)

    errors: list[str] = []
    if data != expected:
        errors.append(
            "generated/phase_alpha_writeback_map.min.json is out of date; "
            "run scripts/generate_phase_alpha_writeback_map.py"
        )
    if not isinstance(source, dict):
        errors.append("examples/phase_alpha_writeback_map.example.json must stay an object")
    else:
        if source.get("surface_type") != "phase_alpha_writeback_map":
            errors.append(
                "examples/phase_alpha_writeback_map.example.json surface_type must stay phase_alpha_writeback_map"
            )
        playbooks = source.get("playbooks")
        if not isinstance(playbooks, list) or len(playbooks) != 5:
            errors.append(
                "examples/phase_alpha_writeback_map.example.json must keep the five Alpha playbook mappings"
            )
        else:
            expected_ids = ["AOA-P-0014", "AOA-P-0006", "AOA-P-0018", "AOA-P-0008", "AOA-P-0009"]
            seen_ids: list[str] = []
            for index, item in enumerate(playbooks):
                if not isinstance(item, dict):
                    errors.append(f"playbooks[{index}] must be an object")
                    continue
                playbook_id = item.get("playbook_id")
                seen_ids.append(playbook_id)
                for field_name in ("writeback_kinds", "source_refs"):
                    value = item.get(field_name)
                    if not isinstance(value, list) or not value:
                        errors.append(f"playbooks[{index}].{field_name} must be a non-empty list")
                        continue
                    for ref_index, ref in enumerate(value):
                        if field_name == "source_refs":
                            error = local_ref_error(ref, f"playbooks[{index}].source_refs[{ref_index}]")
                            if error:
                                errors.append(error)
                if playbook_id == "AOA-P-0018" and item.get("pattern_after_second_recurrence") is not True:
                    errors.append("validation-driven-remediation must keep pattern_after_second_recurrence true")
                if playbook_id == "AOA-P-0008" and item.get("claim_candidate_after_reviewer") is not True:
                    errors.append("long-horizon-model-tier-orchestra must keep claim_candidate_after_reviewer true")
                if playbook_id == "AOA-P-0009":
                    retained = item.get("route_artifacts_retained")
                    if retained != ["inquiry_checkpoint"]:
                        errors.append("restartable-inquiry-loop must keep inquiry_checkpoint as a retained route artifact")
            if seen_ids != expected_ids:
                errors.append(
                    "examples/phase_alpha_writeback_map.example.json playbooks drifted from the fixed Alpha order"
                )

        recall_posture = source.get("recall_posture")
        if not isinstance(recall_posture, dict):
            errors.append("examples/phase_alpha_writeback_map.example.json must keep recall_posture")
        else:
            if recall_posture.get("path") != ["inspect", "capsule", "expand"]:
                errors.append("Phase Alpha recall_posture.path must stay inspect -> capsule -> expand")
            if recall_posture.get("memo_first_only") is not True:
                errors.append("Phase Alpha recall_posture.memo_first_only must stay true")
            expected_contract_ref = "examples/recall_contract.object.working.phase-alpha.json"
            if recall_posture.get("contract_ref") != expected_contract_ref:
                errors.append(f"Phase Alpha recall_posture.contract_ref must stay {expected_contract_ref}")
            error = local_ref_error(recall_posture.get("contract_ref"), "recall_posture.contract_ref")
            if error:
                errors.append(error)

    if errors:
        print("[FAIL] phase_alpha_writeback_map")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   phase_alpha_writeback_map")


def validate_bridge_export_contracts() -> None:
    chunk_validator = validator_for("memory_chunk_face.schema.json")
    graph_validator = validator_for("memory_graph_face.schema.json")
    registry = load_json(GENERATED / "memo_registry.min.json")

    episode = load_json(EXAMPLES / "episode.tos-interpretation.example.json")
    claim = load_json(EXAMPLES / "claim.tos-bridge-ready.example.json")
    bridge = load_json(EXAMPLES / "bridge.kag-lift.example.json")
    thread = load_json(EXAMPLES / "provenance_thread.kag-lift.example.json")
    chunk = load_json(EXAMPLES / "memory_chunk_face.bridge.example.json")
    graph = load_json(EXAMPLES / "memory_graph_face.bridge.example.json")

    errors = [
        f"chunk.{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(chunk_validator.iter_errors(chunk), key=lambda err: list(err.absolute_path))
    ]
    errors.extend(
        f"graph.{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(graph_validator.iter_errors(graph), key=lambda err: list(err.absolute_path))
    )

    ref_checks: list[tuple[str, object]] = []
    for index, value in enumerate(thread.get("source_refs", [])):
        ref_checks.append((f"provenance_thread.kag-lift.source_refs[{index}]", value))
    for list_name in ("section_refs", "source_refs", "source_fragment_refs", "strongest_next_sources"):
        for index, value in enumerate(chunk.get(list_name, [])):
            ref_checks.append((f"memory_chunk_face.bridge.{list_name}[{index}]", value))
    for index, value in enumerate(graph.get("tos_refs", [])):
        ref_checks.append((f"memory_graph_face.bridge.tos_refs[{index}]", value))
    for index, value in enumerate(graph.get("strongest_authored_refs", [])):
        ref_checks.append((f"memory_graph_face.bridge.strongest_authored_refs[{index}]", value))
    for rel_index, relation in enumerate(graph.get("relation_candidates", [])):
        if not isinstance(relation, dict):
            continue
        for ref_index, value in enumerate(relation.get("evidence_refs", [])):
            ref_checks.append((f"memory_graph_face.bridge.relation_candidates[{rel_index}].evidence_refs[{ref_index}]", value))
    append_ref_errors(errors, ref_checks)

    episode_id = episode.get("id")
    claim_id = claim.get("id")
    bridge_id = bridge.get("id")
    thread_id = thread.get("id")

    if episode_id not in claim.get("provenance", {}).get("episode_refs", []):
        errors.append("claim.tos-bridge-ready.example.json must point back to the ToS interpretation episode")
    if claim.get("provenance", {}).get("provenance_thread_id") != thread_id:
        errors.append("claim.tos-bridge-ready.example.json must stay attached to provenance_thread.kag-lift.example.json")
    if bridge.get("provenance", {}).get("provenance_thread_id") != thread_id:
        errors.append("bridge.kag-lift.example.json must stay attached to provenance_thread.kag-lift.example.json")
    if sorted(thread.get("memory_object_ids", [])) != sorted([episode_id, claim_id, bridge_id]):
        errors.append("provenance_thread.kag-lift.example.json must track the episode, claim, and bridge example ids")

    if chunk.get("source_memory_id") != bridge_id:
        errors.append("memory_chunk_face.bridge.example.json must export the bridge.kag-lift example")
    if bridge_id not in chunk.get("bridge_refs", []):
        errors.append("memory_chunk_face.bridge.example.json must keep the bridge id in bridge_refs")
    if graph.get("source_memory_id") != bridge_id:
        errors.append("memory_graph_face.bridge.example.json must export the bridge.kag-lift example")
    if thread_id not in graph.get("provenance_thread_ids", []):
        errors.append("memory_graph_face.bridge.example.json must preserve the provenance thread id")

    relation_targets = {relation.get("target_ref") for relation in graph.get("relation_candidates", []) if isinstance(relation, dict)}
    if episode_id not in relation_targets:
        errors.append("memory_graph_face.bridge.example.json must expose a relation candidate back to the source episode")
    if claim_id not in relation_targets:
        errors.append("memory_graph_face.bridge.example.json must expose a relation candidate back to the reviewed claim")

    bridge_bridges = bridge.get("bridges", {})
    shared_envelope_ref = bridge_bridges.get("shared_envelope_ref")
    if shared_envelope_ref != "repo:aoa-kag/examples/aoa_tos_bridge_envelope.example.json":
        errors.append("bridge.kag-lift.example.json must keep shared_envelope_ref pointed at the canonical aoa-kag envelope example")
    append_ref_errors(
        errors,
        [("bridge.kag-lift.shared_envelope_ref", shared_envelope_ref)],
    )
    if bridge_bridges.get("kag_lift_status") != "candidate":
        errors.append("bridge.kag-lift.example.json must keep kag_lift_status as candidate")
    if not bridge_bridges.get("tos_refs"):
        errors.append("bridge.kag-lift.example.json must keep at least one ToS ref")
    if graph.get("kag_lift_status") != bridge_bridges.get("kag_lift_status"):
        errors.append("memory_graph_face.bridge.example.json must match the bridge kag_lift_status")

    if "schemas/memory_chunk_face.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memo_registry.min.json must list schemas/memory_chunk_face.schema.json")
    if "schemas/memory_graph_face.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memo_registry.min.json must list schemas/memory_graph_face.schema.json")
    if "docs/KAG_TOS_BRIDGE_CONTRACT.md" not in registry.get("core_docs", []):
        errors.append("generated/memo_registry.min.json must list docs/KAG_TOS_BRIDGE_CONTRACT.md")

    if errors:
        print("[FAIL] bridge export contract surfaces")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   bridge export contract surfaces")


def validate_kag_source_export() -> None:
    try:
        from generate_kag_export import KAG_EXPORT_PATH, build_kag_export_payload
    except Exception as exc:  # pragma: no cover - defensive wiring guard
        print("[FAIL] generated/kag_export.min.json")
        print(f"  - unable to load KAG export generator: {exc}")
        raise SystemExit(1) from exc

    errors: list[str] = []
    expected_payload = build_kag_export_payload()
    if not KAG_EXPORT_PATH.exists():
        errors.append("generated/kag_export.min.json must exist")
        actual_payload = {}
    else:
        actual_payload = load_json(KAG_EXPORT_PATH)

    if actual_payload != expected_payload:
        errors.append("generated/kag_export.min.json must match the committed generator-backed payload")

    missing_fields = sorted(KAG_EXPORT_REQUIRED_FIELDS - set(actual_payload))
    if missing_fields:
        errors.append(
            "generated/kag_export.min.json is missing required fields: "
            + ", ".join(missing_fields)
        )

    append_ref_errors(
        errors,
        [
            ("kag_export.entry_surface.path", actual_payload.get("entry_surface", {}).get("path")),
        ]
        + [
            (f"kag_export.direct_relations[{index}].target_ref", relation.get("target_ref"))
            for index, relation in enumerate(actual_payload.get("direct_relations", []))
            if isinstance(relation, dict)
        ],
    )

    source_inputs = actual_payload.get("source_inputs")
    if not isinstance(source_inputs, list) or len(source_inputs) != 2:
        errors.append("generated/kag_export.min.json must keep exactly two source_inputs")
    else:
        expected_source_inputs = expected_payload["source_inputs"]
        if source_inputs != expected_source_inputs:
            errors.append("generated/kag_export.min.json must keep the memo-primary / ToS-supporting source_inputs split")

    if actual_payload.get("section_handles") != expected_payload["section_handles"]:
        errors.append("generated/kag_export.min.json must keep the canonical bridge section_handles")
    if actual_payload.get("direct_relations") != expected_payload["direct_relations"]:
        errors.append("generated/kag_export.min.json must keep the narrow claim/episode/ToS direct_relations trio")

    kag_root_text = os.environ.get("AOA_KAG_ROOT")
    if kag_root_text:
        kag_root = Path(kag_root_text).expanduser().resolve()
        schema_path = kag_root / "schemas" / "federation-kag-export.schema.json"
        if not schema_path.exists():
            errors.append(
                f"AOA_KAG_ROOT canonical schema path does not exist: {schema_path}"
            )
        else:
            schema = load_json(schema_path)
            validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
            schema_errors = [
                f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
                for err in sorted(
                    validator.iter_errors(actual_payload),
                    key=lambda err: list(err.absolute_path),
                )
            ]
            errors.extend(
                f"AOA_KAG_ROOT federation-kag-export.schema.json -> {message}"
                for message in schema_errors
            )

    if errors:
        print("[FAIL] generated/kag_export.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   generated/kag_export.min.json")


def _guardrail_case_input_refs(case: dict[str, object]) -> set[str]:
    values = case.get("input_refs", [])
    if not isinstance(values, list):
        return set()
    return {value for value in values if isinstance(value, str)}


def _validate_guardrail_pilot_cases(
    case_by_focus: dict[str, dict[str, object]],
    errors: list[str],
) -> None:
    pilot_focuses = {"recall_precision", "provenance_fidelity", "staleness"}
    missing_pilot_focuses = sorted(pilot_focuses - set(case_by_focus))
    if missing_pilot_focuses:
        errors.append(
            "memory_eval_guardrail_pack.example.json must keep first-pilot focuses: "
            + ", ".join(missing_pilot_focuses)
        )

    precision_case = case_by_focus.get("recall_precision")
    if isinstance(precision_case, dict):
        refs = _guardrail_case_input_refs(precision_case)
        recall_contract_refs = [
            ref for ref in refs if ref.startswith("examples/recall_contract.")
        ]
        if not recall_contract_refs:
            errors.append(
                "recall_precision guardrail case must reference at least one recall contract example"
            )
        doctrine_surface_family = {
            "generated/memory_catalog.min.json",
            "generated/memory_capsules.json",
            "generated/memory_sections.full.json",
        }
        object_surface_family = {
            "generated/memory_object_catalog.min.json",
            "generated/memory_object_capsules.json",
            "generated/memory_object_sections.full.json",
        }
        if not (
            doctrine_surface_family.issubset(refs) or object_surface_family.issubset(refs)
        ):
            errors.append(
                "recall_precision guardrail case must reference one inspect/capsule/expand surface family"
            )

    provenance_case = case_by_focus.get("provenance_fidelity")
    if isinstance(provenance_case, dict):
        refs = _guardrail_case_input_refs(provenance_case)
        if not any(ref.startswith("examples/provenance_thread.") for ref in refs):
            errors.append(
                "provenance_fidelity guardrail case must reference a provenance_thread example"
            )
        if not any(ref.startswith("examples/claim.") for ref in refs):
            errors.append(
                "provenance_fidelity guardrail case must reference a claim example"
            )
        if not any(ref.startswith("examples/bridge.") for ref in refs):
            errors.append(
                "provenance_fidelity guardrail case must reference a bridge example"
            )

    staleness_case = case_by_focus.get("staleness")
    if isinstance(staleness_case, dict):
        refs = _guardrail_case_input_refs(staleness_case)
        required_docs = {
            "docs/LIFECYCLE.md",
            "docs/MEMORY_TRUST_POSTURE.md",
        }
        missing_docs = sorted(required_docs - refs)
        if missing_docs:
            errors.append(
                "staleness guardrail case must reference lifecycle/trust docs: "
                + ", ".join(missing_docs)
            )
        required_examples = {
            "examples/claim.current-entrypoint.example.json",
            "examples/claim.superseded.example.json",
            "examples/claim.retracted.example.json",
        }
        missing_examples = sorted(required_examples - refs)
        if missing_examples:
            errors.append(
                "staleness guardrail case must reference current/superseded/retracted examples: "
                + ", ".join(missing_examples)
            )


def _validate_guardrail_wider_cases(
    case_by_focus: dict[str, dict[str, object]],
    errors: list[str],
) -> None:
    contradiction_case = case_by_focus.get("contradiction_handling")
    if isinstance(contradiction_case, dict):
        refs = _guardrail_case_input_refs(contradiction_case)
        required_refs = {
            "docs/LIFECYCLE.md",
            "examples/claim.current-entrypoint.example.json",
            "examples/claim.superseded.example.json",
            "examples/claim.retracted.example.json",
        }
        missing_refs = sorted(required_refs - refs)
        if missing_refs:
            errors.append(
                "contradiction_handling guardrail case must reference lifecycle and current/superseded/retracted claims: "
                + ", ".join(missing_refs)
            )

    permission_case = case_by_focus.get("permission_leakage")
    if isinstance(permission_case, dict):
        refs = _guardrail_case_input_refs(permission_case)
        required_prefixes = {
            "docs/AGENT_MEMORY_POSTURE_SEAM.md": "agent memory posture seam",
            "docs/BOUNDARIES.md": "memo boundary doc",
            "docs/OPERATIONAL_BOUNDARY.md": "operational boundary doc",
        }
        missing_labels = [
            label
            for prefix, label in required_prefixes.items()
            if not any(ref.startswith(prefix) for ref in refs)
        ]
        if missing_labels:
            errors.append(
                "permission_leakage guardrail case must reference: "
                + ", ".join(sorted(missing_labels))
            )

    promotion_case = case_by_focus.get("over_promotion")
    if isinstance(promotion_case, dict):
        refs = _guardrail_case_input_refs(promotion_case)
        required_prefixes = {
            "docs/WRITEBACK_TEMPERATURE_POLICY.md": "writeback temperature policy",
            "docs/AGENT_MEMORY_POSTURE_SEAM.md": "agent memory posture seam",
            "examples/bridge.": "bridge candidate example",
        }
        missing_labels = [
            label
            for prefix, label in required_prefixes.items()
            if not any(ref.startswith(prefix) for ref in refs)
        ]
        if missing_labels:
            errors.append(
                "over_promotion guardrail case must reference: "
                + ", ".join(sorted(missing_labels))
            )

    merge_case = case_by_focus.get("hallucinated_merge")
    if isinstance(merge_case, dict):
        refs = _guardrail_case_input_refs(merge_case)
        required_prefixes = {
            "examples/episode.": "episode example",
            "examples/claim.": "claim example",
            "examples/bridge.": "bridge example",
            "examples/provenance_thread.": "provenance_thread example",
        }
        missing_labels = [
            label
            for prefix, label in required_prefixes.items()
            if not any(ref.startswith(prefix) for ref in refs)
        ]
        if missing_labels:
            errors.append(
                "hallucinated_merge guardrail case must reference: "
                + ", ".join(sorted(missing_labels))
            )


def validate_memory_eval_guardrail_pack() -> None:
    validator = validator_for("memory_eval_guardrail_pack.schema.json")
    data = load_json(EXAMPLES / "memory_eval_guardrail_pack.example.json")
    registry = load_json(GENERATED / "memo_registry.min.json")

    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]

    ref_checks: list[tuple[str, object]] = []
    for index, value in enumerate(data.get("source_refs", [])):
        ref_checks.append((f"memory_eval_guardrail_pack.source_refs[{index}]", value))
    for case_index, case in enumerate(data.get("cases", [])):
        if not isinstance(case, dict):
            continue
        for ref_index, value in enumerate(case.get("input_refs", [])):
            ref_checks.append((f"memory_eval_guardrail_pack.cases[{case_index}].input_refs[{ref_index}]", value))
    append_ref_errors(errors, ref_checks)

    seen_case_ids: set[str] = set()
    seen_focuses: set[str] = set()
    case_by_focus: dict[str, dict[str, object]] = {}
    for case in data.get("cases", []):
        if not isinstance(case, dict):
            continue
        case_id = case.get("case_id")
        focus = case.get("focus")
        if isinstance(case_id, str):
            if case_id in seen_case_ids:
                errors.append(f"duplicate guardrail case id: {case_id}")
            seen_case_ids.add(case_id)
        if isinstance(focus, str):
            seen_focuses.add(focus)
            case_by_focus[focus] = case

    required_focuses = {
        "recall_precision",
        "provenance_fidelity",
        "staleness",
        "contradiction_handling",
        "permission_leakage",
        "over_promotion",
        "hallucinated_merge",
    }
    missing_focuses = sorted(required_focuses - seen_focuses)
    if missing_focuses:
        errors.append("memory_eval_guardrail_pack.example.json is missing required focuses: " + ", ".join(missing_focuses))

    _validate_guardrail_pilot_cases(case_by_focus, errors)
    _validate_guardrail_wider_cases(case_by_focus, errors)

    if data.get("handoff_target") != "aoa-evals":
        errors.append("memory_eval_guardrail_pack.example.json must hand off to aoa-evals")
    if "schemas/memory_eval_guardrail_pack.schema.json" not in registry.get("schemas", []):
        errors.append("generated/memo_registry.min.json must list schemas/memory_eval_guardrail_pack.schema.json")
    if "docs/MEMORY_EVAL_GUARDRAILS.md" not in registry.get("core_docs", []):
        errors.append("generated/memo_registry.min.json must list docs/MEMORY_EVAL_GUARDRAILS.md")

    if errors:
        print("[FAIL] memory_eval_guardrail_pack.example.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   memory_eval_guardrail_pack.example.json")


def main() -> int:
    validate_nested_agents_surface()
    validate_support_schema("memory_object_profile.schema.json")
    validate_support_schema("trust_posture.schema.json")
    validate_support_schema("lifecycle_posture.schema.json")
    validate_support_schema("anchor.schema.json")
    validate_support_schema("state_capsule.schema.json")
    validate_support_schema("episode.schema.json")
    validate_support_schema("claim.schema.json")
    validate_support_schema("decision.schema.json")
    validate_support_schema("pattern.schema.json")
    validate_support_schema("bridge.schema.json")
    validate_support_schema("audit_event.schema.json")
    validate_support_schema("failure_lesson_memory_v1.json")
    validate_support_schema("recovery_pattern_memory_v1.json")
    validate_support_schema("memory_object_surface_manifest.schema.json")
    validate_support_schema("memory_object_catalog.schema.json")
    validate_support_schema("memory_object_capsules.schema.json")
    validate_support_schema("memory_object_sections.schema.json")
    validate_support_schema("decay_policy.schema.json")
    validate_support_schema("inquiry_checkpoint.schema.json")
    validate_support_schema("checkpoint-to-memory-contract.schema.json")
    validate_support_schema("memory_chunk_face.schema.json")
    validate_support_schema("memory_graph_face.schema.json")
    validate_support_schema("memory_eval_guardrail_pack.schema.json")
    validate_memory_object_surface_manifest()
    validate_example(validator_for("memory_object.schema.json"), "episode.example.json")
    validate_example(validator_for("memory_object.schema.json"), "claim.example.json")
    validate_example(validator_for("memory_object.schema.json"), "checkpoint_approval_record.example.json")
    validate_example(validator_for("memory_object.schema.json"), "checkpoint_health_check.example.json")
    validate_example(validator_for("memory_object.schema.json"), "episode.tos-interpretation.example.json")
    validate_example(validator_for("memory_object.schema.json"), "claim.tos-bridge-ready.example.json")
    validate_example(validator_for("memory_object.schema.json"), "bridge.kag-lift.example.json")
    validate_example(validator_for("inquiry_checkpoint.schema.json"), "inquiry_checkpoint.example.json")
    validate_example(validator_for("inquiry_checkpoint.schema.json"), "inquiry_checkpoint.return.example.json")
    validate_example(validator_for("provenance_thread.schema.json"), "provenance_thread.example.json")
    validate_example(validator_for("provenance_thread.schema.json"), "checkpoint_improvement_thread.example.json")
    validate_example(validator_for("provenance_thread.schema.json"), "provenance_thread.kag-lift.example.json")
    validate_example(
        validator_for("provenance_thread.schema.json"),
        "provenance_thread.self-agency-continuity.example.json",
    )
    validate_example(validator_for("provenance_thread.schema.json"), PHASE_ALPHA_PROVENANCE_THREAD_EXAMPLE)
    validate_example(validator_for("failure_lesson_memory_v1.json"), "failure_lesson_memory.example.json")
    validate_example(validator_for("failure_lesson_memory_v1.json"), "failure_lesson_memory.lineage.example.json")
    validate_example(validator_for("failure_lesson_memory_v1.json"), "failure_lesson_memory.rollout.example.json")
    validate_example(validator_for("recovery_pattern_memory_v1.json"), "recovery_pattern_memory.example.json")
    validate_example(validator_for("recovery_pattern_memory_v1.json"), "recovery_pattern_memory.lineage.example.json")
    validate_example(validator_for("recovery_pattern_memory_v1.json"), "recovery_pattern_memory.rollout.example.json")
    validate_example(
        validator_for("recovery_pattern_memory_v1.json"),
        "recovery_pattern_memory.component_refresh.example.json",
    )
    validate_recall_contract_example(
        "recall_contract.semantic.json",
        expected_mode="semantic",
        expected_allowed_scopes=["repo", "project", "ecosystem"],
        expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memo_registry.min.json",
        expected_expand_surface="docs/MEMORY_MODEL.md",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.router.semantic.json",
        expected_mode="semantic",
        expected_allowed_scopes=["repo", "project", "ecosystem"],
        expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory_catalog.min.json",
        expected_capsule_surface="generated/memory_capsules.json",
        expected_expand_surface="generated/memory_sections.full.json",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.working.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory_catalog.min.json",
        expected_expand_surface="docs/RUNTIME_WRITEBACK_SEAM.md",
        expected_source_route_required=False,
    )
    validate_recall_contract_example(
        "recall_contract.lineage.json",
        expected_mode="lineage",
        expected_allowed_scopes=["project", "workspace", "ecosystem"],
        expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory_catalog.min.json",
        expected_expand_surface="docs/KAG_TOS_BRIDGE_CONTRACT.md",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.router.lineage.json",
        expected_mode="lineage",
        expected_allowed_scopes=["project", "workspace", "ecosystem"],
        expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory_catalog.min.json",
        expected_capsule_surface="generated/memory_capsules.json",
        expected_expand_surface="generated/memory_sections.full.json",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.object.working.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory_object_catalog.min.json",
        expected_expand_surface="generated/memory_object_sections.full.json",
        expected_source_route_required=False,
    )
    validate_recall_contract_example(
        "recall_contract.object.working.return.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event", "anchor"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory_object_catalog.min.json",
        expected_capsule_surface="generated/memory_object_capsules.json",
        expected_expand_surface="generated/memory_object_sections.full.json",
        expected_source_route_required=False,
        expected_checkpoint_continuity_supported=True,
        expected_return_ready=True,
        expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
        expected_support_artifact_refs=[
            "schemas/inquiry_checkpoint.schema.json",
            "schemas/checkpoint-to-memory-contract.schema.json",
            "docs/RUNTIME_WRITEBACK_SEAM.md",
            "docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
        ],
    )
    validate_recall_contract_example(
        "recall_contract.object.working.phase-alpha.json",
        expected_mode="working",
        expected_allowed_scopes=["thread", "session", "project"],
        expected_preferred_kinds=["state_capsule", "decision", "episode", "audit_event", "anchor"],
        expected_temperature_order=["hot", "warm", "cool", "frozen", "cold"],
        expected_inspect_surface="generated/memory_object_catalog.min.json",
        expected_capsule_surface="generated/memory_object_capsules.json",
        expected_expand_surface="generated/memory_object_sections.full.json",
        expected_source_route_required=False,
        expected_checkpoint_continuity_supported=True,
        expected_return_ready=True,
        expected_preferred_anchor_kinds=["state_capsule", "decision", "anchor"],
        expected_support_artifact_refs=[
            "generated/phase_alpha_writeback_map.min.json",
            "schemas/inquiry_checkpoint.schema.json",
            "docs/RUNTIME_WRITEBACK_SEAM.md",
            "docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md",
        ],
    )
    validate_recall_contract_example(
        "recall_contract.object.semantic.json",
        expected_mode="semantic",
        expected_allowed_scopes=["repo", "project", "ecosystem"],
        expected_preferred_kinds=["claim", "decision", "pattern", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory_object_catalog.min.json",
        expected_capsule_surface="generated/memory_object_capsules.json",
        expected_expand_surface="generated/memory_object_sections.full.json",
        expected_source_route_required=True,
    )
    validate_recall_contract_example(
        "recall_contract.object.lineage.json",
        expected_mode="lineage",
        expected_allowed_scopes=["project", "workspace", "ecosystem"],
        expected_preferred_kinds=["bridge", "claim", "episode", "anchor"],
        expected_temperature_order=["warm", "cool", "frozen", "cold", "hot"],
        expected_inspect_surface="generated/memory_object_catalog.min.json",
        expected_capsule_surface="generated/memory_object_capsules.json",
        expected_expand_surface="generated/memory_object_sections.full.json",
        expected_source_route_required=True,
    )
    validate_memory_object_profiles()
    validate_trust_lifecycle_contracts()
    validate_registry()
    validate_core_memory_contract()
    validate_checkpoint_to_memory_contract()
    validate_runtime_writeback_targets()
    validate_runtime_writeback_intake()
    validate_runtime_writeback_governance()
    validate_live_receipt_log()
    validate_phase_alpha_writeback_map()
    validate_witness_trace_contract()
    validate_bridge_export_contracts()
    validate_kag_source_export()
    validate_memory_eval_guardrail_pack()
    validate_questbook_surface()
    print("\nValidation completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
