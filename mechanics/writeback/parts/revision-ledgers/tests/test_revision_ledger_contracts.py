from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = REPO_ROOT / "mechanics" / "writeback" / "parts" / "revision-ledgers"
CONTRACTS = {
    "assistant_revision_ledger_entry": "assistant_revision_ledger_entry_v1.json",
    "release_revision_ledger_entry_v1": "release_revision_ledger_entry_v1.json",
    "revocation_ledger_entry": "revocation_ledger_entry_v1.json",
}


def load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_revision_ledger_contracts_are_part_local_and_validate() -> None:
    for stem, schema_file in CONTRACTS.items():
        schema_path = PART_ROOT / "schemas" / schema_file
        example_path = PART_ROOT / "examples" / f"{stem}.example.json"

        assert schema_path.is_file()
        assert example_path.is_file()

        schema = load_json(schema_path)
        example = load_json(example_path)
        Draft202012Validator.check_schema(schema)
        errors = sorted(Draft202012Validator(schema).iter_errors(example), key=lambda error: list(error.path))
        assert not errors, f"{example_path.relative_to(REPO_ROOT)}: {errors[0].message if errors else ''}"


def test_revision_ledger_schemas_reject_missing_required_identity() -> None:
    for stem, schema_file in CONTRACTS.items():
        schema = load_json(PART_ROOT / "schemas" / schema_file)
        example = load_json(PART_ROOT / "examples" / f"{stem}.example.json")
        required = schema.get("required")
        assert isinstance(required, list) and required
        field = next(field for field in ("id", "entry_id") if field in required)

        mutated = dict(example)
        mutated.pop(field)

        assert list(Draft202012Validator(schema).iter_errors(mutated))
