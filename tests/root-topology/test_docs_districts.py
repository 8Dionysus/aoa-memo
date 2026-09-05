from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class DocsDistrictsTestCase(unittest.TestCase):
    def test_docs_district_validator_passes(self) -> None:
        completed = subprocess.run(
            (sys.executable, "scripts/root-topology/validate_docs_districts.py"),
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            self.fail(
                "validate_docs_districts.py failed\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            )

    def test_agon_docs_live_in_agon_mechanic(self) -> None:
        flat = sorted((REPO_ROOT / "docs").glob("AGON_*.md"))
        retired_district = REPO_ROOT / "docs" / "agon"
        mechanic = sorted((REPO_ROOT / "mechanics" / "agon" / "docs").glob("AGON_*.md"))

        self.assertEqual([], flat)
        self.assertFalse(retired_district.exists())
        self.assertEqual(27, len(mechanic))
        self.assertTrue((REPO_ROOT / "mechanics" / "agon" / "AGENTS.md").is_file())
        self.assertTrue((REPO_ROOT / "mechanics" / "agon" / "docs" / "AGENTS.md").is_file())
        self.assertFalse((REPO_ROOT / "mechanics" / "agon" / "legacy").exists())

    def test_titan_docs_live_in_titan_mechanic(self) -> None:
        flat = sorted((REPO_ROOT / "docs").glob("TITAN_*.md"))
        retired_district = REPO_ROOT / "docs" / "titan"
        mechanic = sorted((REPO_ROOT / "mechanics" / "titan" / "docs").glob("TITAN_*.md"))

        self.assertEqual([], flat)
        self.assertFalse(retired_district.exists())
        self.assertEqual(10, len(mechanic))
        self.assertTrue((REPO_ROOT / "mechanics" / "titan" / "AGENTS.md").is_file())
        self.assertTrue((REPO_ROOT / "mechanics" / "titan" / "docs" / "AGENTS.md").is_file())
        self.assertFalse((REPO_ROOT / "mechanics" / "titan" / "legacy").exists())

    def test_mechanic_owned_families_do_not_create_docs_subdistricts(self) -> None:
        for district_name in ("agon", "titan", "adoption", "governance", "writeback", "retention"):
            self.assertFalse((REPO_ROOT / "docs" / district_name).exists())


if __name__ == "__main__":
    unittest.main()
