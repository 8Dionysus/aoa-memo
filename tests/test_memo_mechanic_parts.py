from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from memo_mechanics_common import load_config  # noqa: E402
from validate_memo_mechanic_parts import active_parts_table, part_slug, split_table_row, validate  # noqa: E402


def test_memo_mechanic_parts_shape_is_valid() -> None:
    assert validate() == []


def test_active_parts_have_physical_part_nodes() -> None:
    config = load_config()
    total_parts = 0

    for package in config["packages"]:
        package_root = REPO_ROOT / "mechanics" / package["slug"]
        parts_root = package_root / "parts"
        parts_lines = (package_root / "PARTS.md").read_text(encoding="utf-8").splitlines()

        assert (parts_root / "AGENTS.md").is_file()
        assert (parts_root / "README.md").is_file()

        _, rows = active_parts_table(parts_lines)
        for line in rows[2:]:
            part_name = split_table_row(line)[0]
            part_root = parts_root / part_slug(part_name)
            assert (part_root / "README.md").is_file()
            assert (part_root / "CONTRACT.md").is_file()
            assert (part_root / "VALIDATION.md").is_file()
            total_parts += 1

    assert total_parts == 53
