from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class DocsDistrictsTestCase(unittest.TestCase):
    def test_docs_district_validator_passes(self) -> None:
        completed = subprocess.run(
            (sys.executable, "scripts/validate_docs_districts.py"),
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

    def test_agon_docs_live_in_agon_district(self) -> None:
        flat = sorted((REPO_ROOT / "docs").glob("AGON_*.md"))
        district = sorted((REPO_ROOT / "docs" / "agon").glob("AGON_*.md"))

        self.assertEqual([], flat)
        self.assertEqual(27, len(district))
        self.assertTrue((REPO_ROOT / "docs" / "agon" / "AGENTS.md").is_file())
        self.assertTrue((REPO_ROOT / "docs" / "agon" / "README.md").is_file())

    def test_titan_docs_live_in_titan_district(self) -> None:
        flat = sorted((REPO_ROOT / "docs").glob("TITAN_*.md"))
        district = sorted((REPO_ROOT / "docs" / "titan").glob("TITAN_*.md"))

        self.assertEqual([], flat)
        self.assertEqual(10, len(district))
        self.assertTrue((REPO_ROOT / "docs" / "titan" / "AGENTS.md").is_file())
        self.assertTrue((REPO_ROOT / "docs" / "titan" / "README.md").is_file())


if __name__ == "__main__":
    unittest.main()
