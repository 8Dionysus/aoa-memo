from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_mechanic_artifact_topology import validate  # noqa: E402


def test_single_mechanic_artifacts_do_not_return_to_root_technical_dirs() -> None:
    assert validate() == []
