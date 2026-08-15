#!/usr/bin/env python3
"""Validate the reviewed memory corpus under memo/."""

from __future__ import annotations

from pathlib import Path

from validate_memo import load_json, local_ref_error, validator_for

ROOT = Path(__file__).resolve().parents[2]
MEMO = ROOT / "memo"
OBJECTS = MEMO / "objects"
INTAKE = MEMO / "intake"
REVIEWED_INTAKE = INTAKE / "reviewed"
INTAKE_RECEIPTS = INTAKE / "receipts"

KIND_DIRS = {
    "anchor": "anchors",
    "state_capsule": "state-capsules",
    "episode": "episodes",
    "claim": "claims",
    "decision": "decisions",
    "pattern": "patterns",
    "bridge": "bridges",
    "audit_event": "audit-events",
}

KIND_SCHEMAS = {
    "anchor": "anchor.schema.json",
    "state_capsule": "state_capsule.schema.json",
    "episode": "episode.schema.json",
    "claim": "claim.schema.json",
    "decision": "decision.schema.json",
    "pattern": "pattern.schema.json",
    "bridge": "bridge.schema.json",
    "audit_event": "audit_event.schema.json",
}

REQUIRED_PATHS = (
    "memo/AGENTS.md",
    "memo/README.md",
    "memo/OBJECT_SHAPE.md",
    "memo/objects/README.md",
    "memo/support/README.md",
    "memo/support/provenance-threads",
    "memo/support/recall-contracts",
    "memo/intake/README.md",
    "memo/intake/reviewed",
    "memo/intake/quarantine",
    "memo/intake/receipts",
)

FORBIDDEN_LOCAL_PORT_SURFACES = (
    "memo/PORT.yaml",
    "memo/candidates",
    "memo/exports",
    "memo/local",
)


def _rel(path: Path) -> str:
    if path.is_absolute():
        return path.relative_to(ROOT).as_posix()
    return path.as_posix()


def _schema_errors(path: Path, data: dict, schema_name: str) -> list[str]:
    validator = validator_for(schema_name)
    return [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]


def _append_ref_error(errors: list[str], label: str, value: object) -> None:
    error = local_ref_error(value, label)
    if error:
        errors.append(error)


def validate_required_paths(errors: list[str]) -> None:
    for rel_path in REQUIRED_PATHS:
        if not (ROOT / rel_path).exists():
            errors.append(f"{rel_path}: required corpus path is missing")
    for rel_path in FORBIDDEN_LOCAL_PORT_SURFACES:
        if (ROOT / rel_path).exists():
            errors.append(f"{rel_path}: aoa-memo corpus must not use local memo port topology")


def validate_object_path(path: Path, data: dict, errors: list[str]) -> None:
    rel_parts = path.relative_to(OBJECTS).parts
    if len(rel_parts) != 4 or rel_parts[-1] != "object.json":
        errors.append(f"{_rel(path)}: object path must be objects/<kind-dir>/<year>/<slug>/object.json")
        return

    kind_dir, year, slug, _ = rel_parts
    expected_kind = next((kind for kind, directory in KIND_DIRS.items() if directory == kind_dir), None)
    if expected_kind is None:
        errors.append(f"{_rel(path)}: unsupported object kind directory '{kind_dir}'")
        return

    if not year.isdigit() or len(year) != 4:
        errors.append(f"{_rel(path)}: object year directory must be YYYY")
    if not slug or slug.startswith("."):
        errors.append(f"{_rel(path)}: object slug directory must be visible and non-empty")
    if data.get("kind") != expected_kind:
        errors.append(f"{_rel(path)}: kind must be '{expected_kind}' for {kind_dir}/")


def validate_object_bundle(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)

    for schema_name in ("memory_object.schema.json", KIND_SCHEMAS.get(data.get("kind"), "")):
        if not schema_name:
            continue
        for error in _schema_errors(path, data, schema_name):
            errors.append(f"{_rel(path)}: {error}")

    validate_object_path(path, data, errors)

    memo_path = path.with_name("MEMO.md")
    if not memo_path.exists():
        errors.append(f"{_rel(path)}: object bundle must include MEMO.md")

    _append_ref_error(errors, f"{_rel(path)}:payload_ref", data.get("payload_ref"))
    bridges = data.get("bridges")
    if isinstance(bridges, dict):
        _append_ref_error(errors, f"{_rel(path)}:bridges.route_capsule_ref", bridges.get("route_capsule_ref"))

    provenance = data.get("provenance")
    if isinstance(provenance, dict):
        for index, ref in enumerate(provenance.get("source_refs", [])):
            _append_ref_error(errors, f"{_rel(path)}:provenance.source_refs[{index}]", ref)

    return errors


def validate_json_placement(errors: list[str]) -> None:
    for path in OBJECTS.rglob("*.json"):
        if path.name != "object.json":
            errors.append(f"{_rel(path)}: JSON files under memo/objects must be named object.json")
            continue
        errors.extend(validate_object_bundle(path))


def validate_reviewed_intake_packets(errors: list[str]) -> None:
    if not REVIEWED_INTAKE.exists():
        return
    for path in sorted(REVIEWED_INTAKE.glob("*.json")):
        data = load_json(path)
        for error in _schema_errors(path, data, "local_memo_export.schema.json"):
            errors.append(f"{_rel(path)}: {error}")
        if data.get("target_owner") != "aoa-memo":
            errors.append(f"{_rel(path)}: target_owner must be aoa-memo")
        if data.get("target_route") != "reviewed_intake":
            errors.append(f"{_rel(path)}: target_route must be reviewed_intake")
        if data.get("allowed_result") != "reviewed_write":
            errors.append(f"{_rel(path)}: allowed_result must be reviewed_write after corpus landing")


def validate_landing_receipt(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)
    for error in _schema_errors(path, data, "reviewed_intake_landing_receipt.schema.json"):
        errors.append(f"{_rel(path)}: {error}")

    _append_ref_error(errors, f"{_rel(path)}:copied_intake_ref", data.get("copied_intake_ref"))
    _append_ref_error(errors, f"{_rel(path)}:object_path", data.get("object_path"))

    object_path = data.get("object_path")
    if isinstance(object_path, str) and object_path:
        object_data_path = ROOT / object_path
        if object_data_path.exists():
            object_data = load_json(object_data_path)
            if object_data.get("id") != data.get("object_ref"):
                errors.append(f"{_rel(path)}: object_ref must match object_path id")
            if object_data.get("payload_ref") != data.get("copied_intake_ref"):
                errors.append(f"{_rel(path)}: copied_intake_ref must match object payload_ref")
        else:
            errors.append(f"{_rel(path)}: object_path points to missing object")

    copied_intake_ref = data.get("copied_intake_ref")
    if isinstance(copied_intake_ref, str) and copied_intake_ref:
        copied_intake_path = ROOT / copied_intake_ref
        if copied_intake_path.exists():
            export_data = load_json(copied_intake_path)
            if export_data.get("allowed_result") != "reviewed_write":
                errors.append(f"{_rel(path)}: copied intake must preserve allowed_result reviewed_write")
        else:
            errors.append(f"{_rel(path)}: copied_intake_ref points to missing intake packet")

    return errors


def validate_landing_receipts(errors: list[str]) -> None:
    if not INTAKE_RECEIPTS.exists():
        return
    receipts: list[tuple[Path, dict]] = []
    for path in sorted(INTAKE_RECEIPTS.glob("*.json")):
        data = load_json(path)
        receipts.append((path, data))
        errors.extend(validate_landing_receipt(path))
    errors.extend(validate_active_landing_receipts(receipts))


def validate_active_landing_receipts(receipts: list[tuple[Path, dict]]) -> list[str]:
    """Reject duplicate successful landing authorities for one object."""

    by_object: dict[str, list[Path]] = {}
    for path, data in receipts:
        if data.get("result") != "landed":
            continue
        object_ref = data.get("object_ref")
        if isinstance(object_ref, str) and object_ref:
            by_object.setdefault(object_ref, []).append(path)

    errors: list[str] = []
    for object_ref, paths in sorted(by_object.items()):
        if len(paths) < 2:
            continue
        rendered_paths = ", ".join(_rel(path) for path in paths)
        errors.append(
            "memo/intake/receipts: multiple active landed receipts for "
            f"object_ref {object_ref}: {rendered_paths}"
        )
    return errors


def main() -> int:
    errors: list[str] = []
    validate_required_paths(errors)
    validate_json_placement(errors)
    validate_reviewed_intake_packets(errors)
    validate_landing_receipts(errors)

    if errors:
        print("[FAIL] memo corpus")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("[OK]   memo corpus")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
