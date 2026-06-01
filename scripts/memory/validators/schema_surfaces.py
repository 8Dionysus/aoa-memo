"""Source/schema validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403

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

def validate_support_schema(schema_name: str) -> None:
    validator_for(schema_name)
    print(f"[OK]   {schema_name}")

def validate_memory_object_surface_manifest() -> None:
    validator = validator_for("memory_object_surface_manifest.schema.json")
    data = load_json(example_path_for("memory_object_surface_manifest.json"))

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
