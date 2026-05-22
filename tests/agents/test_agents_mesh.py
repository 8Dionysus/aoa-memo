from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class AgentsMeshTestCase(unittest.TestCase):
    def run_script(self, *args: str) -> None:
        completed = subprocess.run(
            (sys.executable, *args),
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            self.fail(
                f"{' '.join(args)} failed\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            )

    def test_agents_mesh_validators_pass(self) -> None:
        for args in (
            ("scripts/agents/validate_agents_mesh.py",),
            ("scripts/agents/build_agents_mesh_index.py", "--check"),
            ("scripts/agents/validate_agents_mesh_index.py",),
        ):
            with self.subTest(script=args):
                self.run_script(*args)

    def test_agents_mesh_index_names_current_cards(self) -> None:
        payload = json.loads((REPO_ROOT / "generated/agents/agents_mesh.min.json").read_text())

        self.assertEqual("aoa_memo_agents_mesh_index_v1", payload["schema_version"])
        self.assertEqual("agents-md-mesh-v1", payload["source_of_truth"])
        self.assertEqual("config/agents/agents_mesh.json", payload["config_ref"])
        self.assertEqual("DESIGN.AGENTS.md", payload["authority_ref"])
        self.assertEqual(112, payload["counts"]["canonical"])
        self.assertEqual(0, payload["counts"]["migration"])

        paths = {card["path"] for card in payload["cards"]}
        self.assertEqual(payload["counts"]["canonical"], len(paths))
        self.assertTrue(
            {
                ".agents/AGENTS.md",
                ".agents/skills/AGENTS.md",
                ".agents/spark/AGENTS.md",
                ".github/AGENTS.md",
                "AGENTS.md",
                "docs/decisions/AGENTS.md",
                "manifests/AGENTS.md",
                "memo/AGENTS.md",
                "mechanics/writeback/legacy/AGENTS.md",
                "quests/AGENTS.md",
            }.issubset(paths)
        )
        self.assertTrue(
            {
                "config/agents/AGENTS.md",
                "config/mechanics/AGENTS.md",
                "config/memory-ports/AGENTS.md",
                "config/root-topology/AGENTS.md",
                "docs/boundaries/AGENTS.md",
                "docs/memory/AGENTS.md",
                "docs/posture/AGENTS.md",
                "docs/root/AGENTS.md",
                "examples/generated-surfaces/AGENTS.md",
                "examples/lifecycle/AGENTS.md",
                "examples/memory-objects/AGENTS.md",
                "examples/memory-ports/AGENTS.md",
                "examples/phase-alpha/AGENTS.md",
                "examples/recall/AGENTS.md",
                "examples/support-objects/AGENTS.md",
                "generated/agents/AGENTS.md",
                "generated/mechanics/AGENTS.md",
                "generated/memory-objects/AGENTS.md",
                "generated/memory/AGENTS.md",
                "generated/quests/AGENTS.md",
                "generated/root-topology/AGENTS.md",
                "schemas/generated-surfaces/AGENTS.md",
                "schemas/memory-objects/AGENTS.md",
                "schemas/memory-ports/AGENTS.md",
                "schemas/recall-posture/AGENTS.md",
                "schemas/support-objects/AGENTS.md",
                "scripts/agents/AGENTS.md",
                "scripts/mechanics/AGENTS.md",
                "scripts/memory/AGENTS.md",
                "scripts/release/AGENTS.md",
                "scripts/root-topology/AGENTS.md",
                "tests/agents/AGENTS.md",
                "tests/mechanics/AGENTS.md",
                "tests/memory/AGENTS.md",
                "tests/root-topology/AGENTS.md",
            }.issubset(paths)
        )

    def test_release_check_runs_agents_mesh_gate(self) -> None:
        text = (REPO_ROOT / "scripts" / "release" / "release_check.py").read_text(encoding="utf-8")
        for snippet in (
            "scripts/agents/validate_agents_mesh.py",
            "scripts/agents/build_agents_mesh_index.py",
            "--check",
            "scripts/agents/validate_agents_mesh_index.py",
        ):
            self.assertIn(snippet, text)

    def test_release_check_runs_spark_lane_gate(self) -> None:
        text = (REPO_ROOT / "scripts" / "release" / "release_check.py").read_text(encoding="utf-8")
        for snippet in (
            ".agents/spark/scripts/validate_spark_lane.py",
            ".agents/spark/tests",
        ):
            self.assertIn(snippet, text)

    def test_neighbor_doc_boundary_rules_pin_agents_owned_guidance(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "agents" / "agents_mesh.json").read_text())
        rules = {rule["path"]: rule for rule in config["neighbor_doc_boundaries"]}

        self.assertEqual(
            {
                "README.md",
                "CHARTER.md",
                "DESIGN.AGENTS.md",
                "mechanics/agon/docs/README.md",
                "mechanics/titan/docs/TITAN_MEMORY_POSTURE.md",
            },
            set(rules),
        )
        self.assertIn("## Route Modes", rules["README.md"]["forbidden_snippets"])
        self.assertIn("## Editing posture", rules["CHARTER.md"]["forbidden_snippets"])
        self.assertIn(
            "The current broad validation path remains:",
            rules["DESIGN.AGENTS.md"]["forbidden_snippets"],
        )
        self.assertIn(
            "`config/agon_*.source.json`",
            rules["mechanics/agon/docs/README.md"]["forbidden_snippets"],
        )
        self.assertIn(
            "## Closeout\n",
            rules["mechanics/titan/docs/TITAN_MEMORY_POSTURE.md"]["forbidden_snippets"],
        )

    def test_agents_cards_do_not_reference_flat_root_script_commands(self) -> None:
        for path in REPO_ROOT.rglob("AGENTS.md"):
            rel_path = path.relative_to(REPO_ROOT).as_posix()
            if ".git/" in rel_path or ".deps/" in rel_path:
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(
                text,
                r"python scripts/(?!memory/|agents/|mechanics/|root-topology/|release/)",
                msg=f"{rel_path} contains a stale flat root script route",
            )

    def test_agents_mesh_ignores_dependency_checkouts(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "agents" / "agents_mesh.json").read_text())
        self.assertIn(".deps", config["ignored_directory_names"])
        self.assertIn(".deps", config["top_level_exemptions"])


if __name__ == "__main__":
    unittest.main()
