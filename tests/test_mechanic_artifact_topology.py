from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_mechanic_artifact_topology import validate  # noqa: E402


def test_single_mechanic_artifacts_do_not_return_to_root_technical_dirs() -> None:
    assert validate() == []


def test_root_generated_outputs_have_family_contracts() -> None:
    payload = json.loads((REPO_ROOT / "config" / "root_technical_districts.json").read_text())
    allowed = set(payload["districts"]["generated"]["allowed_files"])
    covered = {
        output
        for family in payload["generated_families"]
        for output in family["outputs"]
    }

    assert covered == allowed


def test_root_generated_builder_backed_families_name_builders_and_validators() -> None:
    payload = json.loads((REPO_ROOT / "config" / "root_technical_districts.json").read_text())

    for family in payload["generated_families"]:
        assert family["source_refs"]
        assert family["validators"]
        if family["source_kind"] in {"generator-backed", "projection"}:
            assert family["builders"]


def test_root_scripts_have_family_contracts() -> None:
    payload = json.loads((REPO_ROOT / "config" / "root_technical_districts.json").read_text())
    allowed = set(payload["districts"]["scripts"]["allowed_files"])
    covered = {
        script
        for family in payload["script_families"]
        for script in family["scripts"]
    }

    assert covered == allowed


def test_root_script_families_name_owner_and_coverage_refs() -> None:
    payload = json.loads((REPO_ROOT / "config" / "root_technical_districts.json").read_text())

    for family in payload["script_families"]:
        assert family["owner_surface"]
        assert family["scripts"]
        assert family["covered_by"]


def test_root_tests_have_family_contracts() -> None:
    payload = json.loads((REPO_ROOT / "config" / "root_technical_districts.json").read_text())
    allowed = set(payload["districts"]["tests"]["allowed_files"])
    covered = {
        test
        for family in payload["test_families"]
        for test in family["tests"]
    }

    assert covered == allowed


def test_root_test_families_name_owner_and_protected_refs() -> None:
    payload = json.loads((REPO_ROOT / "config" / "root_technical_districts.json").read_text())

    for family in payload["test_families"]:
        assert family["owner_surface"]
        assert family["tests"]
        assert family["protects"]
