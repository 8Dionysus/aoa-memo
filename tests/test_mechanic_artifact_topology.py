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
