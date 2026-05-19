from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[5]


class OperationalGateMechanicTestCase(unittest.TestCase):
    def test_operational_gate_registers_active_docs(self) -> None:
        config = json.loads((REPO_ROOT / "config" / "memo_mechanics.json").read_text())
        packages = {package["slug"]: package for package in config["packages"]}
        operational_gate = packages["operational-gate"]

        self.assertEqual("Operational Gate Memo Mechanic", operational_gate["title"])
        self.assertIn("operation", operational_gate)
        self.assertEqual(
            [
                "DEPLOYMENT_INCIDENT_MEMORY_GATE.md",
                "OFFICE_INCIDENT_MEMORY_GATE.md",
                "POST_RELEASE_MEMORY_BOUNDARIES.md",
                "SERVICE_REVISION_LEDGER.md",
            ],
            operational_gate["docs"],
        )

        for filename in operational_gate["docs"]:
            self.assertTrue(
                (REPO_ROOT / "mechanics" / "operational-gate" / "docs" / filename).is_file()
            )
            self.assertFalse((REPO_ROOT / "docs" / filename).exists())

    def test_operational_gate_preserves_stronger_owner_boundaries(self) -> None:
        readme = (REPO_ROOT / "mechanics" / "operational-gate" / "README.md").read_text(
            encoding="utf-8"
        )
        for snippet in (
            "### Operation",
            "Agents-of-Abyss",
            "abyss-stack",
            "aoa-evals",
            "aoa-agents",
            "aoa-playbooks",
            "aoa-routing",
            "aoa-stats",
            "Tree-of-Sophia",
            "without turning `aoa-memo` into",
            "rollout authority",
        ):
            self.assertIn(snippet, readme)

    def test_operational_gate_keeps_technical_contracts_mechanic_owned(self) -> None:
        parts = (REPO_ROOT / "mechanics" / "operational-gate" / "PARTS.md").read_text(
            encoding="utf-8"
        )
        for path in (
            "mechanics/operational-gate/parts/deployment-incident-gate/schemas/deployment_incident_memory_gate_v1.json",
            "mechanics/operational-gate/parts/deployment-incident-gate/examples/deployment_incident_memory_gate.example.json",
            "mechanics/operational-gate/parts/office-incident-gate/schemas/service_incident_memory_entry_v1.json",
            "mechanics/operational-gate/parts/office-incident-gate/examples/service_incident_memory_entry_v1.example.json",
            "mechanics/operational-gate/parts/service-revision-ledger/schemas/service_revision_ledger_entry_v1.json",
            "mechanics/operational-gate/parts/service-revision-ledger/examples/service_revision_ledger_entry_v1.example.json",
            "mechanics/operational-gate/parts/post-release-boundaries/schemas/train_release_memory_entry_v1.json",
            "mechanics/operational-gate/parts/post-release-boundaries/examples/train_release_memory_entry_v1.example.json",
        ):
            self.assertIn(path, parts)
            self.assertTrue((REPO_ROOT / path).is_file())

    def test_deployment_gate_schema_requires_admission_fields(self) -> None:
        schema = json.loads(
            (
                REPO_ROOT
                / "mechanics"
                / "operational-gate"
                / "parts"
                / "deployment-incident-gate"
                / "schemas"
                / "deployment_incident_memory_gate_v1.json"
            ).read_text()
        )
        example = json.loads(
            (
                REPO_ROOT
                / "mechanics"
                / "operational-gate"
                / "parts"
                / "deployment-incident-gate"
                / "examples"
                / "deployment_incident_memory_gate.example.json"
            ).read_text()
        )

        errors = list(Draft202012Validator(schema).iter_errors(example))
        self.assertFalse(errors, errors[0].message if errors else "")

        for field in (
            "evidence_refs",
            "owner_route",
            "review_posture",
            "future_effect",
            "expiry_or_recheck",
        ):
            with self.subTest(field=field):
                mutated = dict(example)
                mutated.pop(field)
                self.assertTrue(list(Draft202012Validator(schema).iter_errors(mutated)))

    def test_operational_gate_docs_are_not_placeholders(self) -> None:
        docs_dir = REPO_ROOT / "mechanics" / "operational-gate" / "docs"
        for filename in (
            "DEPLOYMENT_INCIDENT_MEMORY_GATE.md",
            "OFFICE_INCIDENT_MEMORY_GATE.md",
            "POST_RELEASE_MEMORY_BOUNDARIES.md",
            "SERVICE_REVISION_LEDGER.md",
        ):
            text = (docs_dir / filename).read_text(encoding="utf-8")
            self.assertIn("owner", text.lower())
            self.assertIn("evidence", text.lower())
            self.assertIn("Memo", text)
            self.assertGreaterEqual(len(text.splitlines()), 20)


if __name__ == "__main__":
    unittest.main()
