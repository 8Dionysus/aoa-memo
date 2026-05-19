from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[5]


class GovernanceMechanicTestCase(unittest.TestCase):
    def test_governance_mechanic_registers_source_docs(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "memo_mechanics.json").read_text())
        packages = {package["slug"]: package for package in config["packages"]}
        governance = packages["governance"]

        self.assertEqual("Governance Memo Mechanic", governance["title"])
        self.assertEqual(9, len(governance["docs"]))
        self.assertNotIn("VIA_NEGATIVA_CHECKLIST.md", governance["docs"])

        for filename in governance["docs"]:
            self.assertFalse((REPO_ROOT / "docs" / filename).exists())
            self.assertTrue((REPO_ROOT / "mechanics" / "governance" / "docs" / filename).is_file())

        self.assertFalse(
            (REPO_ROOT / "mechanics" / "governance" / "docs" / "VIA_NEGATIVA_CHECKLIST.md").exists()
        )

    def test_governance_owner_map_preserves_stronger_owner_boundaries(self) -> None:
        owner_map = (REPO_ROOT / "mechanics" / "governance" / "OWNER_MAP.md").read_text(
            encoding="utf-8"
        )
        for owner in (
            "Agents-of-Abyss",
            "Tree-of-Sophia",
            "aoa-evals",
            "aoa-routing",
            "aoa-agents",
            "aoa-playbooks",
            "abyss-stack",
        ):
            self.assertIn(owner, owner_map)

        readme = (REPO_ROOT / "mechanics" / "governance" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("### Must not claim", readme)
        self.assertIn("Tree-of-Sophia may be written directly", readme)


if __name__ == "__main__":
    unittest.main()
