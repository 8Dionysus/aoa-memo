from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class TopologySpineTestCase(unittest.TestCase):
    def test_topology_spine_files_exist_and_have_role_language(self) -> None:
        required = {
            "DESIGN.md": (
                "system form",
                "memory and recall layer",
                "Memory is not proof",
                "ROOT_SURFACE_LAW",
            ),
            "DESIGN.AGENTS.md": (
                "agent-facing guidance",
                "Generated companions",
                "MEMORY_INDEX.md",
                "Decision Review",
                "memory became another layer",
            ),
            "MEMORY_INDEX.md": (
                "MEMORY_INDEX",
                "Memory Object Kinds",
                "Support Objects",
                "Generated Companions",
                "not proof",
            ),
            "docs/README.md": (
                "Documentation Map",
                "MEMORY_INDEX",
                "Source Families",
                "Topology Rule",
                "decisions",
            ),
            "docs/root/ROOT_SURFACE_LAW.md": (
                "Root Surface Law",
                "MEMORY_INDEX.md",
                "Docs-Root Principle",
                "Migration Procedure Before Moving Flat Docs",
                ".agents/spark/",
            ),
            ".agents/AGENTS.md": (
                "agent-facing companion district",
                ".agents/<lane>/",
                "tests/root-topology/test_topology_spine.py",
            ),
            ".agents/spark/AGENTS.md": (
                "only governs work started from `.agents/spark/`",
                "fast-loop lane",
                "memory remains explicit and bounded",
                "done-or-handoff",
            ),
            ".agents/spark/SWARM.md": (
                ".agents/spark/SWARM.md",
                "memory seam",
                "memory did not become proof",
                ".agents/spark/registry.json",
            ),
            "docs/decisions/AGENTS.md": (
                "Decision records",
                "public-safe",
                "python scripts/release/release_check.py",
            ),
            "docs/decisions/README.md": (
                "Decision Records Index",
                "indexes/by-number.md",
                "Addressing",
                "Review Rule",
            ),
            "docs/decisions/0023-memory-topology-spine.md": (
                "Add Memory Topology Spine Before Moving Flat Docs",
                "Do not move flat docs in this change",
                "Do not move root `Spark/` as part of this topology-spine decision",
                "Memory remains weaker than proof",
            ),
            "docs/decisions/0039-spark-agent-lane-home.md": (
                "Move Spark Agent Lane Under `.agents`",
                "Move root `Spark/` to `.agents/spark/`",
                "This change does not move flat `docs/` surfaces",
                "Spark remains a fast-loop helper",
            ),
        }

        for relative_path, snippets in required.items():
            with self.subTest(path=relative_path):
                text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
                for snippet in snippets:
                    self.assertIn(snippet, text)

    def test_entrypoints_route_to_topology_spine(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

        for snippet in (
            "DESIGN.md",
            "DESIGN.AGENTS.md",
            "MEMORY_INDEX.md",
            "docs/README.md",
            "docs/root/ROOT_SURFACE_LAW.md",
            "docs/decisions/",
        ):
            self.assertIn(snippet, agents)

        for snippet in (
            "DESIGN.md",
            "DESIGN.AGENTS.md",
            "MEMORY_INDEX.md",
            "docs/README.md",
            "docs/root/ROOT_SURFACE_LAW.md",
            "docs/decisions",
        ):
            self.assertIn(snippet, readme)

        for snippet in (
            "DESIGN.md",
            "DESIGN.AGENTS.md",
            "MEMORY_INDEX.md",
            "docs/root/ROOT_SURFACE_LAW.md",
            "docs/decisions/",
        ):
            self.assertIn(snippet, roadmap)

        self.assertIn("source-authored topology spine", changelog)
        self.assertIn("MEMORY_INDEX.md", changelog)
        self.assertIn(".agents/spark/", changelog)

    def test_spark_lane_moved_out_of_root(self) -> None:
        self.assertFalse((REPO_ROOT / "Spark").exists())
        self.assertTrue((REPO_ROOT / ".agents" / "AGENTS.md").is_file())
        self.assertTrue((REPO_ROOT / ".agents" / "spark" / "AGENTS.md").is_file())
        self.assertTrue((REPO_ROOT / ".agents" / "spark" / "SWARM.md").is_file())
        self.assertTrue((REPO_ROOT / ".agents" / "spark" / "registry.json").is_file())
        self.assertTrue((REPO_ROOT / ".agents" / "spark" / "scripts" / "validate_spark_lane.py").is_file())

    def test_decision_indexes_are_generated_from_canonical_ids(self) -> None:
        by_number = (REPO_ROOT / "docs" / "decisions" / "indexes" / "by-number.md").read_text(
            encoding="utf-8"
        )
        alias_map = json.loads(
            (REPO_ROOT / "docs" / "decisions" / "indexes" / "alias-map.min.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertIn("AOA-MEM-D-0001", by_number)
        self.assertIn("AOA-MEM-D-0071", by_number)
        self.assertIn("AOA-MEM-D-0072", by_number)
        self.assertIn("Numbered path", by_number)
        self.assertEqual(alias_map["schema_version"], "aoa_memo_decision_alias_map_v2")
        self.assertEqual(len(alias_map["entries"]), 72)
        self.assertEqual(alias_map["entries"][0]["decision_id"], "AOA-MEM-D-0001")
        self.assertEqual(
            alias_map["entries"][0]["legacy_path"],
            "docs/decisions/2026-05-18-adoption-writeback-retention-mechanics.md",
        )
        self.assertEqual(
            alias_map["entries"][0]["current_path"],
            "docs/decisions/0001-adoption-writeback-retention-mechanics.md",
        )
        self.assertEqual(
            alias_map["entries"][0]["canonical_path_status"],
            "canonical_numbered_path_active",
        )


if __name__ == "__main__":
    unittest.main()
