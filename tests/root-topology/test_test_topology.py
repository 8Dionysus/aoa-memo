from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
TOPOLOGY_PATH = REPO_ROOT / "docs" / "testing" / "TEST_TOPOLOGY.md"
INVENTORY_PATH = REPO_ROOT / "docs" / "testing" / "test_inventory.json"
PYTEST_INI_PATH = REPO_ROOT / "pytest.ini"
REQUIRED_INVENTORY_FIELDS = {
    "family",
    "paths",
    "protects",
    "owner_surface",
    "lane",
    "mode",
    "runtime_cost",
    "focused_target",
    "failure_route",
}
MAX_ACTIVE_TEST_LINES = 300
REQUIRED_AGENTIC_TEST_LAYERS = {
    "contract_core",
    "tool_boundary",
    "scenario_replay",
    "trace_eval",
    "state_memory_session",
    "fault_safety",
    "offline_online_loop",
    "performance_budget",
}


def discovered_test_files() -> set[str]:
    roots = (REPO_ROOT / "tests", REPO_ROOT / "mechanics", REPO_ROOT / ".agents")
    return {
        path.relative_to(REPO_ROOT).as_posix()
        for root in roots
        for path in root.glob("**/test*.py")
        if "__pycache__" not in path.parts
        and "legacy" not in path.parts
    }


def load_inventory() -> dict:
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def test_topology_doc_names_memo_route_shape() -> None:
    text = TOPOLOGY_PATH.read_text(encoding="utf-8")

    for required in (
        "family -> protects -> owner source -> lane ->",
        "`memory/*`",
        "`mechanics/*`",
        "`validation/test-topology`",
        "Memory remains weaker than proof",
        "config/validation_lanes.json",
        "docs/validation/VALIDATOR_TOPOLOGY.md",
        "Agentic Test Layers",
        "Scenario replay",
        "Trace eval",
        "Fault/safety",
    ):
        assert required in text


def test_inventory_covers_all_test_files() -> None:
    inventory = load_inventory()
    required_fields = set(inventory["required_fields"])
    assert required_fields == REQUIRED_INVENTORY_FIELDS

    inventory_paths: list[str] = []
    for entry in inventory["entries"]:
        assert required_fields.issubset(entry)
        assert entry["lane"] in {"memory", "mechanics", "topology", "agents", "release"}
        assert entry["mode"] in {"blocking", "blocking-in-release", "advisory", "soft-live"}
        assert entry["runtime_cost"] in {"fast", "medium", "slow"}
        assert not re.match(r"^(python|git|bash|sh)\b", entry["focused_target"])

        owner_path = Path(str(entry["owner_surface"]).split("#", 1)[0])
        assert not owner_path.is_absolute()
        assert (REPO_ROOT / owner_path).exists(), entry["owner_surface"]

        paths = entry["paths"]
        assert isinstance(paths, list) and paths
        for path in paths:
            inventory_paths.append(path)
            assert (REPO_ROOT / path).is_file(), path

    assert len(inventory_paths) == len(set(inventory_paths))
    assert discovered_test_files() == set(inventory_paths)


def test_legacy_tests_are_not_active_test_inventory() -> None:
    inventory = load_inventory()

    for entry in inventory["entries"]:
        assert "legacy" not in entry["family"], entry
        assert "/legacy/" not in entry["owner_surface"], entry
        for path in entry["paths"]:
            assert "/legacy/" not in path, entry


def test_pytest_policy_excludes_legacy_from_collection() -> None:
    text = PYTEST_INI_PATH.read_text(encoding="utf-8")

    assert "norecursedirs" in text
    assert "legacy" in text
    assert not (REPO_ROOT / "mechanics" / "readiness-boundary" / "legacy" / "raw" / "conftest.py").exists()
    assert not list((REPO_ROOT / "mechanics").glob("*/legacy/**/test*.py"))


def test_agentic_test_layers_are_explicitly_routed() -> None:
    inventory = load_inventory()
    layers = inventory["agentic_test_layers"]

    assert set(layers) == REQUIRED_AGENTIC_TEST_LAYERS
    for layer_id, layer in layers.items():
        assert layer["status"] in {"implemented", "partial", "routed"}, layer_id
        assert layer["repo_role"]
        assert isinstance(layer["primary_entries"], list) and layer["primary_entries"]

    assert layers["trace_eval"]["status"] == "routed"
    assert "aoa-evals" in layers["trace_eval"]["repo_role"]
    assert layers["fault_safety"]["status"] == "implemented"
    assert layers["scenario_replay"]["status"] == "implemented"


def test_memory_validator_regressions_stay_split_by_boundary() -> None:
    assert not (REPO_ROOT / "tests" / "memory" / "test_memo_validators.py").exists()

    required_split_files = {
        "test_memo_schema_contracts.py",
        "test_memo_memory_context_boundaries.py",
        "test_memo_runtime_writeback_boundaries.py",
        "test_memo_live_receipt_boundaries.py",
        "test_memo_questbook_boundaries.py",
        "test_memo_handoff_boundaries.py",
        "test_memo_eval_guardrails.py",
        "test_memo_generated_surface_contracts.py",
    }
    actual_split_files = {
        path.name
        for path in (REPO_ROOT / "tests" / "memory").glob("test_memo_*.py")
    }
    assert required_split_files <= actual_split_files

    for path in (REPO_ROOT / "tests" / "memory").glob("test_memo_*.py"):
        assert len(path.read_text(encoding="utf-8").splitlines()) <= MAX_ACTIVE_TEST_LINES, path


def test_active_test_files_stay_compact() -> None:
    for test_path in discovered_test_files():
        path = REPO_ROOT / test_path
        assert len(path.read_text(encoding="utf-8").splitlines()) <= MAX_ACTIVE_TEST_LINES, path


def test_inventory_and_lane_manifest_cross_reference_each_other() -> None:
    inventory = load_inventory()
    lane_manifest = json.loads((REPO_ROOT / "config" / "validation_lanes.json").read_text(encoding="utf-8"))

    assert inventory["owner"] == "docs/testing/TEST_TOPOLOGY.md"
    assert lane_manifest["owner"] == "docs/validation/VALIDATOR_TOPOLOGY.md"
    assert lane_manifest["testing_inventory_ref"] == "docs/testing/test_inventory.json"
    assert lane_manifest["command_authority"] == "config/validation_lanes.json"
