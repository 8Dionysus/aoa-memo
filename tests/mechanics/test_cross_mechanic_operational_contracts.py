from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
OPERATIONAL_CONTRACT_PREFIX_BASES = {
    "assistant_revision_": "mechanics/writeback/parts/revision-ledgers",
    "certification_": "mechanics/governance/parts/install-and-certification-boundary",
    "deployment_": "mechanics/operational-gate/parts/deployment-incident-gate",
    "post_release_": "mechanics/retention/parts/post-release-retention",
    "rollback_": "mechanics/writeback/parts/rollback-and-recovery",
}
ROOT_DISTRICTS_CONFIG = ROOT / "config" / "root-topology" / "root_technical_districts.json"


def schema_path_for_example(schemas_root: Path, example_path: Path) -> Path:
    stem = example_path.name.removesuffix(".example.json")
    if stem.endswith("_v1"):
        return schemas_root / f"{stem}.json"
    return schemas_root / f"{stem}_v1.json"


def operational_contract_pairs() -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    missing_pairs: list[str] = []
    for prefix, base_ref in OPERATIONAL_CONTRACT_PREFIX_BASES.items():
        base = ROOT / base_ref
        examples_root = base / "examples"
        schemas_root = base / "schemas"
        for example_path in sorted(examples_root.glob(f"{prefix}*.example.json")):
            schema_path = schema_path_for_example(schemas_root, example_path)
            if not schema_path.exists():
                missing_pairs.append(f"{example_path.relative_to(ROOT)} -> {schema_path.relative_to(ROOT)}")
                continue
            pairs.append((schema_path, example_path))
    assert not missing_pairs, "missing operational contract schema pair(s): " + ", ".join(missing_pairs)
    return pairs


def declared_operational_contract_schema_paths() -> list[Path]:
    config = json.loads(ROOT_DISTRICTS_CONFIG.read_text(encoding="utf-8"))
    families = {
        family["id"]: family for family in config["test_families"] if isinstance(family, dict)
    }
    family = families["cross_mechanic_operational_contracts"]
    return [ROOT / ref for ref in family["protects"]]


def test_declared_operational_contracts_are_exercised() -> None:
    covered = {schema_path for schema_path, _example_path in operational_contract_pairs()}
    missing = [
        schema_path.relative_to(ROOT).as_posix()
        for schema_path in declared_operational_contract_schema_paths()
        if schema_path not in covered
    ]
    assert not missing, "declared operational contract schema(s) not exercised: " + ", ".join(missing)


def test_operational_contract_examples_match_schemas() -> None:
    pairs = operational_contract_pairs()
    assert pairs
    for schema_path, example_path in pairs:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        example = json.loads(example_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        errors = sorted(Draft202012Validator(schema).iter_errors(example), key=lambda error: list(error.path))
        assert not errors, f"{example_path.name}: {errors[0].message if errors else ''}"
