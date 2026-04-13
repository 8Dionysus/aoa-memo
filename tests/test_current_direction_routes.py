from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class CurrentDirectionRoutesTestCase(unittest.TestCase):
    def test_root_entrypoints_route_to_roadmap(self) -> None:
        roadmap_path = REPO_ROOT / "ROADMAP.md"
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")

        self.assertTrue(roadmap_path.is_file())
        self.assertIn("ROADMAP.md", readme)
        self.assertIn("ROADMAP.md", agents)

    def test_pre_agon_memory_readiness_is_routed(self) -> None:
        doc_ref = "docs/PRE_AGON_MEMORY_READINESS.md"
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        doc = (REPO_ROOT / doc_ref).read_text(encoding="utf-8")
        registry = json.loads(
            (REPO_ROOT / "generated" / "memo_registry.min.json").read_text(encoding="utf-8")
        )

        self.assertIn(doc_ref, readme)
        self.assertIn(doc_ref, roadmap)
        self.assertIn(doc_ref, agents)
        self.assertIn(doc_ref, registry["core_docs"])

        for phrase in (
            "not a live Agon memory ledger",
            "scar",
            "retention",
            "memory is not proof",
            "aoa-evals",
            "aoa-kag",
            "aoa-routing",
        ):
            self.assertIn(phrase, doc)


if __name__ == "__main__":
    unittest.main()
