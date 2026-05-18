from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_memo_mechanic_parts import validate  # noqa: E402


def test_memo_mechanic_parts_shape_is_valid() -> None:
    assert validate() == []
