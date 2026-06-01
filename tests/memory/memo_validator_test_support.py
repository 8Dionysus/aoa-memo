from __future__ import annotations

import copy
import io
import importlib.util
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_ROOT = REPO_ROOT / "scripts" / "memory"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validate_memo
import validate_memory_object_surfaces
import validate_memory_surfaces


def load_script_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generate_kag_export = load_script_module(
    "generate_kag_export",
    REPO_ROOT
    / "mechanics"
    / "consumer-handoff"
    / "parts"
    / "kag-source-export"
    / "scripts"
    / "generate_kag_export.py",
)
build_quest_surfaces = load_script_module(
    "build_quest_surfaces",
    REPO_ROOT
    / "mechanics"
    / "questbook"
    / "parts"
    / "quest-read-model-projections"
    / "scripts"
    / "build_quest_surfaces.py",
)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class MemoValidatorTestCase(unittest.TestCase):
    def assert_system_exit_quietly(self, func, /, *args, **kwargs) -> SystemExit:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as context:
                    func(*args, **kwargs)
        return context.exception

    def guardrail_payload(self) -> dict:
        payload = load_json(validate_memo.example_path_for("memory_eval_guardrail_pack.example.json"))
        assert isinstance(payload, dict)
        return copy.deepcopy(payload)

    def assert_guardrail_payload_fails(self, payload: dict) -> None:
        guardrail_path = validate_memo.example_path_for("memory_eval_guardrail_pack.example.json")
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> dict:
            if Path(path) == guardrail_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_memory_eval_guardrail_pack)

    def kag_export_payload(self) -> dict:
        payload = load_json(generate_kag_export.KAG_EXPORT_PATH)
        assert isinstance(payload, dict)
        return copy.deepcopy(payload)

    def assert_kag_export_payload_fails(self, payload: dict) -> None:
        export_path = generate_kag_export.KAG_EXPORT_PATH
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> dict:
            if Path(path) == export_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_kag_source_export)

    def questbook_payload(self, quest_id: str) -> dict:
        payload = load_json(validate_memo.discover_questbook_files()[quest_id])
        assert isinstance(payload, dict)
        return copy.deepcopy(payload)
