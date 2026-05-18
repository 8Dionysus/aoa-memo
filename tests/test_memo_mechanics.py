from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class MemoMechanicsTestCase(unittest.TestCase):
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

    def test_memo_mechanics_validators_pass(self) -> None:
        for args in (
            ("scripts/validate_memo_mechanics.py",),
            ("scripts/build_memo_mechanics_index.py", "--check"),
            ("scripts/validate_memo_mechanics_index.py",),
        ):
            with self.subTest(script=args):
                self.run_script(*args)

    def test_memo_mechanics_index_names_packages(self) -> None:
        payload = json.loads((REPO_ROOT / "generated" / "memo_mechanics.min.json").read_text())

        self.assertEqual("aoa_memo_mechanics_index_v2", payload["schema_version"])
        self.assertEqual("memo-mechanics-v2", payload["source_of_truth"])
        self.assertEqual("config/memo_mechanics.json", payload["config_ref"])
        self.assertEqual("mechanics/README.md", payload["authority_ref"])
        self.assertEqual(11, payload["counts"]["packages"])
        self.assertEqual(95, payload["counts"]["docs"])

        packages = {package["slug"]: package for package in payload["packages"]}
        self.assertEqual(
            {
                "antifragility",
                "agon",
                "titan",
                "adoption",
                "governance",
                "shape-guard",
                "consumer-handoff",
                "operational-gate",
                "recurrence-support",
                "writeback",
                "retention",
            },
            set(packages),
        )
        self.assertEqual(6, packages["antifragility"]["doc_count"])
        self.assertEqual(27, packages["agon"]["doc_count"])
        self.assertEqual(10, packages["titan"]["doc_count"])
        self.assertEqual(6, packages["adoption"]["doc_count"])
        self.assertEqual(9, packages["governance"]["doc_count"])
        self.assertEqual(1, packages["shape-guard"]["doc_count"])
        self.assertEqual(6, packages["consumer-handoff"]["doc_count"])
        self.assertEqual(4, packages["operational-gate"]["doc_count"])
        self.assertEqual(3, packages["recurrence-support"]["doc_count"])
        self.assertEqual(17, packages["writeback"]["doc_count"])
        self.assertEqual(6, packages["retention"]["doc_count"])
        for package in packages.values():
            self.assertIn("operation", package)
            self.assertIn("os_abyss_role", package)

    def test_mechanic_docs_live_under_mechanics_not_docs_root(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "memo_mechanics.json").read_text())
        for package in config["packages"]:
            slug = package["slug"]
            for filename in package["docs"]:
                self.assertFalse((REPO_ROOT / "docs" / filename).exists())
                self.assertTrue((REPO_ROOT / "mechanics" / slug / "docs" / filename).is_file())

    def test_release_check_runs_memo_mechanics_gate(self) -> None:
        text = (REPO_ROOT / "scripts" / "release_check.py").read_text(encoding="utf-8")
        for snippet in (
            "scripts/validate_memo_mechanics.py",
            "scripts/build_memo_mechanics_index.py",
            "--check",
            "scripts/validate_memo_mechanics_index.py",
        ):
            self.assertIn(snippet, text)

    def test_mechanic_subroutes_and_artifact_topology_are_present(self) -> None:
        topology = (REPO_ROOT / "mechanics" / "ARTIFACT_TOPOLOGY.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Root Technical Districts", topology)
        self.assertIn("Mechanic Artifact Lane", topology)
        self.assertIn("Move Rule", topology)

        for slug in (
            "antifragility",
            "agon",
            "titan",
            "adoption",
            "governance",
            "shape-guard",
            "consumer-handoff",
            "operational-gate",
            "recurrence-support",
            "writeback",
            "retention",
        ):
            self.assertTrue((REPO_ROOT / "mechanics" / slug / "docs" / "AGENTS.md").is_file())
            self.assertTrue((REPO_ROOT / "mechanics" / slug / "legacy" / "AGENTS.md").is_file())


if __name__ == "__main__":
    unittest.main()
