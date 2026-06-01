from __future__ import annotations

from functools import lru_cache
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: jsonschema. Install it with: pip install jsonschema")
    raise SystemExit(2) from exc

from ._shared_io import load_json
from ._shared_paths import EXAMPLES, MECHANIC_EXAMPLE_DIRS, MECHANIC_SCHEMA_DIRS, ROOT, SCHEMAS
from ._shared_refs import append_lineage_chain_errors, local_ref_error
from ._shared_schema_constants import FORMAT_CHECKER

@lru_cache(maxsize=None)
def schema_registry() -> Registry:
    resources: list[tuple[str, Resource]] = []
    for path in iter_schema_paths():
        schema = load_json(path)
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            resources.append((schema_id, Resource.from_contents(schema)))
    return Registry().with_resources(resources)

def iter_schema_paths() -> tuple[Path, ...]:
    paths: list[Path] = []
    for schema_dir in (*root_schema_dirs(), *MECHANIC_SCHEMA_DIRS):
        paths.extend(sorted(schema_dir.glob("*.json")))
    return tuple(paths)

def root_schema_dirs() -> tuple[Path, ...]:
    return (SCHEMAS, *tuple(sorted(path for path in SCHEMAS.iterdir() if path.is_dir())))

def root_example_dirs() -> tuple[Path, ...]:
    return (EXAMPLES, *tuple(sorted(path for path in EXAMPLES.iterdir() if path.is_dir())))

def _find_unique_by_name(name: str, dirs: tuple[Path, ...], label: str) -> Path:
    primary = dirs[0] / name
    if primary.is_file():
        return primary
    matches = [directory / name for directory in dirs[1:] if (directory / name).is_file()]
    if not matches:
        raise FileNotFoundError(f"missing {label}: {name}")
    if len(matches) > 1:
        rendered = ", ".join(
            path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix()
            for path in matches
        )
        raise ValueError(f"ambiguous {label} {name}: {rendered}")
    return matches[0]

def schema_path_for(schema_ref: str) -> Path:
    if "/" in schema_ref:
        return ROOT / schema_ref
    return _find_unique_by_name(schema_ref, (*root_schema_dirs(), *MECHANIC_SCHEMA_DIRS), "schema")

def example_path_for(example_ref: str) -> Path:
    if "/" in example_ref:
        return ROOT / example_ref
    return _find_unique_by_name(example_ref, (*root_example_dirs(), *MECHANIC_EXAMPLE_DIRS), "example")

def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(schema_path_for(schema_name))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FORMAT_CHECKER, registry=schema_registry())

def validate_example(validator: Draft202012Validator, example_name: str) -> None:
    data = load_json(example_path_for(example_name))
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
        ("lineage_refs.source_ref", lineage_refs.get("source_ref")),
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
