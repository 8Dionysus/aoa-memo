from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "agents"))

import validation_lanes  # noqa: E402
from validate_agents_mesh import (  # noqa: E402
    validation_command_ownership_issues,
    validation_route_issues,
)


def release_command_text() -> str:
    return "\n".join(" ".join(step.command) for step in validation_lanes.RELEASE_CHECK_COMMAND_SEQUENCE)


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
        self.assertEqual(0, payload["counts"]["migration"])

        paths = {card["path"] for card in payload["cards"]}
        self.assertEqual(payload["counts"]["canonical"], len(paths))
        self.assertFalse(any("/legacy/" in path for path in paths))
        self.assertTrue(
            {
                ".agents/AGENTS.md",
                ".github/AGENTS.md",
                "AGENTS.md",
                "docs/decisions/AGENTS.md",
                "docs/testing/AGENTS.md",
                "docs/validation/AGENTS.md",
                "evals/AGENTS.md",
                "manifests/AGENTS.md",
                "memo/AGENTS.md",
                "quests/AGENTS.md",
                "stats/AGENTS.md",
                "skills/AGENTS.md",
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
                "kag/AGENTS.md",
                "schemas/generated-surfaces/AGENTS.md",
                "schemas/memory-objects/AGENTS.md",
                "schemas/memory-ports/AGENTS.md",
                "schemas/recall-posture/AGENTS.md",
                "schemas/support-objects/AGENTS.md",
                "scripts/agents/AGENTS.md",
                "scripts/mechanics/AGENTS.md",
                "scripts/memory/AGENTS.md",
                "scripts/memory/validators/AGENTS.md",
                "scripts/release/AGENTS.md",
                "scripts/root-topology/AGENTS.md",
                "tests/agents/AGENTS.md",
                "tests/mechanics/AGENTS.md",
                "tests/memory/AGENTS.md",
                "tests/root-topology/AGENTS.md",
            }.issubset(paths)
        )

    def test_release_check_runs_agents_mesh_gate(self) -> None:
        text = release_command_text()
        for snippet in (
            "scripts/agents/validate_agents_mesh.py",
            "scripts/agents/build_agents_mesh_index.py",
            "--check",
            "scripts/agents/validate_agents_mesh_index.py",
        ):
            self.assertIn(snippet, text)

    def test_release_check_has_no_retired_spark_lane_gate(self) -> None:
        text = release_command_text()
        self.assertNotIn(".agents/spark", text)

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
            "executable validation commands live in route cards",
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
                r"python scripts/(?!(ci_gate\.py|release_check\.py|validation_lanes\.py|memory/|agents/|mechanics/|root-topology/|release/))",
                msg=f"{rel_path} contains a stale flat root script route",
            )

    def test_agents_mesh_ignores_dependency_checkouts(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "agents" / "agents_mesh.json").read_text())
        self.assertIn(".deps", config["ignored_directory_names"])
        self.assertIn(".deps", config["top_level_exemptions"])

    def test_validation_routes_are_local_and_not_recursive_aggregates(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            (root / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
            nested = root / "docs" / "validation"
            nested.mkdir(parents=True)
            (nested / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
            (nested / "VALIDATION.md").write_text(
                "# VALIDATION.md\n\n"
                "<!-- Preserved on-demand procedure from `other/VALIDATION.md`. -->\n"
                "# VALIDATION.md\n",
                encoding="utf-8",
            )

            issues = validation_route_issues(
                root, ("AGENTS.md", "docs/validation/AGENTS.md")
            )

            self.assertTrue(
                any("same-directory on-demand route is missing" in issue for issue in issues)
            )
            self.assertTrue(
                any("exactly one level-1 heading" in issue for issue in issues)
            )
            self.assertTrue(any("aggregate marker" in issue for issue in issues))

            (root / "VALIDATION.md").write_text("# Root validation\n", encoding="utf-8")
            (nested / "VALIDATION.md").write_text(
                "# Validator topology validation\n", encoding="utf-8"
            )
            self.assertEqual(
                [],
                validation_route_issues(
                    root, ("AGENTS.md", "docs/validation/AGENTS.md")
                ),
            )

    def test_validation_routes_reject_stale_or_ambiguous_command_handoffs(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            nested = root / "docs"
            nested.mkdir()
            (root / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
            (root / "VALIDATION.md").write_text("# Root validation\n", encoding="utf-8")
            (nested / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
            (nested / "VALIDATION.md").write_text(
                "# Docs validation\n\n"
                "Run from the repository root:\n\n"
                "Shared executable routes remain owned by `VALIDATION.md`.\n"
                "Then run commands from `../AGENTS.md#validation`.\n",
                encoding="utf-8",
            )

            issues = validation_route_issues(
                root, ("AGENTS.md", "docs/AGENTS.md")
            )

            self.assertTrue(any("AGENTS.md#validation" in issue for issue in issues))
            self.assertTrue(any("bare VALIDATION.md" in issue for issue in issues))
            self.assertTrue(any("dangling repository-root" in issue for issue in issues))

            (nested / "VALIDATION.md").write_text(
                "# Docs validation\n\n"
                "This surface owns no distinct executable procedure. Use the "
                "[root validation route](../VALIDATION.md).\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [],
                validation_route_issues(
                    root, ("AGENTS.md", "docs/AGENTS.md")
                ),
            )

    def test_validation_commands_have_one_human_owner(self) -> None:
        with tempfile.TemporaryDirectory() as raw_root:
            root = Path(raw_root)
            (root / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
            (root / "VALIDATION.md").write_text(
                "# Root validation\n\n```bash\npython scripts/check.py --all\n```\n",
                encoding="utf-8",
            )
            nested = root / "docs"
            nested.mkdir()
            (nested / "AGENTS.md").write_text("# AGENTS.md\n", encoding="utf-8")
            (nested / "VALIDATION.md").write_text(
                "# Docs validation\n\n```bash\npython scripts/check.py --all\n```\n",
                encoding="utf-8",
            )

            issues = validation_command_ownership_issues(
                root, ("AGENTS.md", "docs/AGENTS.md")
            )
            self.assertEqual(1, len(issues))
            self.assertIn("multiple human owners", issues[0])

            (nested / "VALIDATION.md").write_text(
                "# Docs validation\n\nUse the root validation route.\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [],
                validation_command_ownership_issues(
                    root, ("AGENTS.md", "docs/AGENTS.md")
                ),
            )


if __name__ == "__main__":
    unittest.main()
