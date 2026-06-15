from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SPARK_ROOT = REPO_ROOT / ".agents" / "spark"
REGISTRY = SPARK_ROOT / "registry.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class SparkLaneTestCase(unittest.TestCase):
    def run_validator(self, repo_root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                ".agents/spark/scripts/validate_spark_lane.py",
                "--repo-root",
                str(repo_root),
            ],
            cwd=repo_root,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

    def copy_spark_lane(self, temp_root: Path) -> None:
        temp_spark_root = temp_root / ".agents" / "spark"
        temp_spark_root.parent.mkdir()
        shutil.copytree(
            SPARK_ROOT,
            temp_spark_root,
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        (temp_root / "scripts" / "release").mkdir(parents=True)
        (temp_root / "scripts/release/release_check.py").write_text(
            ".agents/spark/scripts/validate_spark_lane.py\n",
            encoding="utf-8",
        )

    def test_spark_lane_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, ".agents/spark/scripts/validate_spark_lane.py"],
            cwd=REPO_ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_every_scenario_is_registered(self) -> None:
        registry = load_json(REGISTRY)
        registered = {scenario["path"] for scenario in registry["scenarios"]}
        discovered = {
            path.relative_to(REPO_ROOT).as_posix()
            for path in (SPARK_ROOT / "scenarios").iterdir()
            if path.is_dir()
        }
        self.assertEqual(registered, discovered)

    def test_unregistered_scenario_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            self.copy_spark_lane(temp_root)
            extra = temp_root / ".agents/spark/scenarios/unregistered"
            (extra / "templates").mkdir(parents=True)
            (extra / "examples").mkdir(parents=True)
            (extra / "README.md").write_text("# Extra\n", encoding="utf-8")
            result = self.run_validator(temp_root)

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("Spark scenarios missing from registry", result.stdout)
        self.assertIn(".agents/spark/scenarios/unregistered", result.stdout)

    def test_registry_schema_rejects_extra_scenario_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            self.copy_spark_lane(temp_root)
            registry = temp_root / ".agents/spark/registry.json"
            payload = load_json(registry)
            payload["scenarios"][0]["unexpected"] = "schema drift"
            registry.write_text(json.dumps(payload), encoding="utf-8")
            result = self.run_validator(temp_root)

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(".agents/spark/registry.json:scenarios.0", result.stdout)
        self.assertIn("Additional properties are not allowed", result.stdout)

    def test_invalid_registry_schema_reports_schema_problem(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            self.copy_spark_lane(temp_root)
            schema_path = temp_root / ".agents/spark/schemas/spark-registry.schema.json"
            schema = load_json(schema_path)
            schema["properties"]["scenarios"]["type"] = 7
            schema_path.write_text(json.dumps(schema), encoding="utf-8")
            result = self.run_validator(temp_root)

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(
            ".agents/spark/schemas/spark-registry.schema.json is not a valid Draft 2020-12 schema",
            result.stdout,
        )
        self.assertNotIn("Traceback", result.stdout)

    def test_prompt_without_done_or_handoff_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_root = Path(temp)
            self.copy_spark_lane(temp_root)
            prompt = temp_root / ".agents/spark/scenarios/memory-audit/PROMPT.md"
            prompt.write_text(
                prompt.read_text(encoding="utf-8").replace(
                    "done-or-handoff",
                    "done or handoff",
                ),
                encoding="utf-8",
            )
            result = self.run_validator(temp_root)

        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("must mention done-or-handoff", result.stdout)

    def test_templates_have_done_or_handoff_shape(self) -> None:
        registry = load_json(REGISTRY)
        for scenario in registry["scenarios"]:
            result_template = REPO_ROOT / scenario["result_template_ref"]
            handoff_template = REPO_ROOT / scenario["handoff_template_ref"]
            self.assertIn("Status: done", result_template.read_text(encoding="utf-8"))
            self.assertIn("Status: handoff", handoff_template.read_text(encoding="utf-8"))

    def test_memo_specific_stop_lines_are_visible(self) -> None:
        agents_text = (SPARK_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("memory-is-not-proof", agents_text)
        self.assertIn("runtime state", agents_text)
        self.assertIn("private traces", agents_text)
        self.assertIn("generated surfaces as source truth", agents_text)


if __name__ == "__main__":
    unittest.main()
