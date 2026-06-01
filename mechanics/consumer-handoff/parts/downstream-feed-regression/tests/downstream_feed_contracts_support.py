from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_ROOT = REPO_ROOT / "scripts" / "memory"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))
SCRIPT_PATHS = {
    "generate_memory_object_surfaces.py": SCRIPTS_ROOT / "generate_memory_object_surfaces.py",
    "generate_kag_export.py": REPO_ROOT
    / "mechanics"
    / "consumer-handoff"
    / "parts"
    / "kag-source-export"
    / "scripts"
    / "generate_kag_export.py",
    "generate_runtime_writeback_targets.py": REPO_ROOT
    / "mechanics"
    / "writeback"
    / "parts"
    / "runtime-and-temperature"
    / "scripts"
    / "generate_runtime_writeback_targets.py",
    "generate_runtime_writeback_intake.py": REPO_ROOT
    / "mechanics"
    / "writeback"
    / "parts"
    / "runtime-and-temperature"
    / "scripts"
    / "generate_runtime_writeback_intake.py",
    "generate_runtime_writeback_governance.py": REPO_ROOT
    / "mechanics"
    / "writeback"
    / "parts"
    / "runtime-and-temperature"
    / "scripts"
    / "generate_runtime_writeback_governance.py",
}


def load_module(script_name: str):
    path = SCRIPT_PATHS[script_name]
    spec = importlib.util.spec_from_file_location(script_name.replace(".py", ""), path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generate_memory_object_surfaces = load_module("generate_memory_object_surfaces.py")
generate_kag_export = load_module("generate_kag_export.py")
generate_runtime_writeback_targets = load_module("generate_runtime_writeback_targets.py")
generate_runtime_writeback_intake = load_module("generate_runtime_writeback_intake.py")
generate_runtime_writeback_governance = load_module("generate_runtime_writeback_governance.py")

GENERATED_MEMORY_ROOT = REPO_ROOT / "generated" / "memory"
GENERATED_MEMORY_OBJECTS_ROOT = REPO_ROOT / "generated" / "memory-objects"
RECALL_EXAMPLES_ROOT = REPO_ROOT / "examples" / "recall"
CONSUMER_HANDOFF_GENERATED_ROOT = (
    REPO_ROOT
    / "mechanics"
    / "consumer-handoff"
    / "parts"
    / "kag-source-export"
    / "generated"
)
CHECKPOINT_EXAMPLES_ROOT = (
    REPO_ROOT
    / "mechanics"
    / "checkpoint"
    / "parts"
    / "checkpoint-to-memory-mapping"
    / "examples"
)
WRITEBACK_GENERATED_ROOT = (
    REPO_ROOT
    / "mechanics"
    / "writeback"
    / "parts"
    / "runtime-and-temperature"
    / "generated"
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))
