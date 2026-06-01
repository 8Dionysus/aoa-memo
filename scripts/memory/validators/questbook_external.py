"""Quest source and projection checks for the memory-context profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403

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
