from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
TOPOLOGY_PATH = REPO_ROOT / "docs" / "testing" / "TEST_TOPOLOGY.md"
INVENTORY_PATH = REPO_ROOT / "docs" / "testing" / "test_inventory.json"
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


def discovered_test_files() -> set[str]:
    roots = (REPO_ROOT / "tests", REPO_ROOT / "mechanics", REPO_ROOT / ".agents")
    return {
        path.relative_to(REPO_ROOT).as_posix()
        for root in roots
        for path in root.glob("**/test*.py")
        if "__pycache__" not in path.parts
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


def test_inventory_and_lane_manifest_cross_reference_each_other() -> None:
    inventory = load_inventory()
    lane_manifest = json.loads((REPO_ROOT / "config" / "validation_lanes.json").read_text(encoding="utf-8"))

    assert inventory["owner"] == "docs/testing/TEST_TOPOLOGY.md"
    assert lane_manifest["owner"] == "docs/validation/VALIDATOR_TOPOLOGY.md"
    assert lane_manifest["testing_inventory_ref"] == "docs/testing/test_inventory.json"
    assert lane_manifest["command_authority"] == "config/validation_lanes.json"
