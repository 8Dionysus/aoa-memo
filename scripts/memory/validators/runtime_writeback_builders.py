"""Runtime writeback projection and governance checks."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def load_runtime_writeback_targets_builder():
    module_path = WRITEBACK_RUNTIME_PART / "scripts" / "generate_runtime_writeback_targets.py"
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_writeback_targets",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] runtime_writeback_targets.min.json")
        print("  - unable to load runtime writeback target generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_runtime_writeback_intake_builder():
    module_path = WRITEBACK_RUNTIME_PART / "scripts" / "generate_runtime_writeback_intake.py"
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_writeback_intake",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] runtime_writeback_intake.min.json")
        print("  - unable to load runtime writeback intake generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_runtime_writeback_governance_builder():
    module_path = WRITEBACK_RUNTIME_PART / "scripts" / "generate_runtime_writeback_governance.py"
    spec = importlib.util.spec_from_file_location(
        "generate_runtime_writeback_governance",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] runtime_writeback_governance.min.json")
        print("  - unable to load runtime writeback governance generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_growth_refinery_writeback_lanes_builder():
    module_path = WRITEBACK_GROWTH_PART / "scripts" / "generate_growth_refinery_writeback_lanes.py"
    spec = importlib.util.spec_from_file_location(
        "generate_growth_refinery_writeback_lanes",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] growth_refinery_writeback_lanes.min.json")
        print("  - unable to load growth refinery writeback lane generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_phase_alpha_writeback_builder():
    module_path = WRITEBACK_GROWTH_PART / "scripts" / "generate_phase_alpha_writeback_map.py"
    spec = importlib.util.spec_from_file_location(
        "generate_phase_alpha_writeback_map",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] phase_alpha_writeback_map.min.json")
        print("  - unable to load Phase Alpha writeback map generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
