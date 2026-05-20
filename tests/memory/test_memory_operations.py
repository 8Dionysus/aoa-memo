from __future__ import annotations

import copy
import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "memory" / "validate_memory_operations.py"
spec = importlib.util.spec_from_file_location("validate_memory_operations", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
validate_memory_operations = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_memory_operations)


def test_memory_operations_validate() -> None:
    assert validate_memory_operations.validate() == []


def test_high_risk_write_guard_rejects_reviewed_write() -> None:
    example = (
        REPO_ROOT
        / "mechanics"
        / "operational-gate"
        / "parts"
        / "write-path-guardrails"
        / "examples"
        / "memory_write_path_guard.untrusted_prompt_injection.example.json"
    )
    payload = copy.deepcopy(validate_memory_operations.load_json(example))
    payload["allowed_write_result"] = "reviewed_write"
    original_load_json = validate_memory_operations.load_json

    def fake_load_json(path: Path):
        if Path(path) == example:
            return copy.deepcopy(payload)
        return original_load_json(path)

    validate_memory_operations.load_json = fake_load_json
    try:
        errors = validate_memory_operations.validate_write_path_guards()
    finally:
        validate_memory_operations.load_json = original_load_json

    assert any("high-risk input must not allow reviewed_write" in error for error in errors)


def test_operation_modes_require_complete_mode_set() -> None:
    example = REPO_ROOT / "examples" / "recall" / "memory_operation_modes.example.json"
    payload = copy.deepcopy(validate_memory_operations.load_json(example))
    payload["modes"] = payload["modes"][:-1]
    original_load_json = validate_memory_operations.load_json

    def fake_load_json(path: Path):
        if Path(path) == example:
            return copy.deepcopy(payload)
        return original_load_json(path)

    validate_memory_operations.load_json = fake_load_json
    try:
        errors = validate_memory_operations.validate_operation_modes()
    finally:
        validate_memory_operations.load_json = original_load_json

    assert any("must expose modes" in error for error in errors)
