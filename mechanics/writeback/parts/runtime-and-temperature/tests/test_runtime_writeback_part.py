from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = REPO_ROOT / "mechanics" / "writeback" / "parts" / "runtime-and-temperature"
SCRIPTS_ROOT = PART_ROOT / "scripts"
GENERATED_ROOT = PART_ROOT / "generated"


def load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def load_module(script_name: str):
    path = SCRIPTS_ROOT / script_name
    spec = importlib.util.spec_from_file_location(script_name.removesuffix(".py"), path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runtime_writeback_targets_schema_and_generator_are_part_local() -> None:
    schema = load_json(PART_ROOT / "schemas" / "runtime-writeback-targets.schema.json")
    current = load_json(GENERATED_ROOT / "runtime_writeback_targets.min.json")
    generator = load_module("generate_runtime_writeback_targets.py")

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(current)
    assert current == generator.build_runtime_writeback_targets_payload()
    assert current["source_of_truth"] == "mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json"


def test_runtime_writeback_intake_and_governance_are_generator_backed() -> None:
    intake = load_json(GENERATED_ROOT / "runtime_writeback_intake.min.json")
    governance = load_json(GENERATED_ROOT / "runtime_writeback_governance.min.json")
    intake_generator = load_module("generate_runtime_writeback_intake.py")
    governance_generator = load_module("generate_runtime_writeback_governance.py")

    assert intake == intake_generator.build_runtime_writeback_intake_payload()
    assert governance == governance_generator.build_runtime_writeback_governance_payload()
    assert intake["source_of_truth"]["runtime_writeback_targets"] == (
        "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_targets.min.json"
    )
    assert governance["source_of_truth"]["runtime_writeback_intake"] == (
        "mechanics/writeback/parts/runtime-and-temperature/generated/runtime_writeback_intake.min.json"
    )
