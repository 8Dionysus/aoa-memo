from __future__ import annotations

import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import *  # noqa: F403


class MemoEvalGuardrailTestCase(MemoValidatorTestCase):
    def test_guardrail_validator_handles_non_string_case_ids_without_type_error(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][0]["case_id"] = []
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_precision_case_without_surface_family(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][0]["input_refs"] = [
            "examples/recall/recall_contract.router.semantic.json",
            "mechanics/consumer-handoff/docs/PLAYBOOK_MEMORY_SCOPES.md",
        ]
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_precision_case_without_recall_contract_ref(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][0]["input_refs"] = [
            "generated/memory/memory_catalog.min.json",
            "generated/memory/memory_capsules.json",
            "generated/memory/memory_sections.full.json",
        ]
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_provenance_case_without_provenance_thread(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][1]["input_refs"] = [
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/claim.tos-bridge-ready.example.json",
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge.kag-lift.example.json",
        ]
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_staleness_case_without_lifecycle_examples(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][2]["input_refs"] = [
            "docs/posture/LIFECYCLE.md",
            "docs/posture/MEMORY_TRUST_POSTURE.md",
            "docs/posture/MEMORY_TEMPERATURES.md",
        ]
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_missing_recall_precision_focus(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][0]["focus"] = "precision_shadow"
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_missing_provenance_fidelity_focus(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][1]["focus"] = "provenance_shadow"
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_missing_staleness_focus(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][2]["focus"] = "staleness_shadow"
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_contradiction_case_without_active_claim(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][3]["input_refs"] = [
            "examples/lifecycle/claim.superseded.example.json",
            "examples/lifecycle/claim.retracted.example.json",
            "docs/posture/LIFECYCLE.md",
        ]
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_permission_case_without_role_boundary(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][4]["input_refs"] = [
            "docs/boundaries/BOUNDARIES.md#aoa-agents",
            "docs/boundaries/OPERATIONAL_BOUNDARY.md#consumer-contracts",
        ]
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_promotion_case_without_bridge_candidate(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][5]["input_refs"] = [
            "mechanics/writeback/docs/WRITEBACK_TEMPERATURE_POLICY.md",
            "mechanics/consumer-handoff/docs/AGENT_MEMORY_POSTURE_SEAM.md#boundary-rule",
        ]
        self.assert_guardrail_payload_fails(payload)
    def test_guardrail_validator_rejects_merge_case_without_provenance_thread(self) -> None:
        payload = self.guardrail_payload()
        payload["cases"][6]["input_refs"] = [
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/episode.tos-interpretation.example.json",
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/claim.tos-bridge-ready.example.json",
            "mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge.kag-lift.example.json",
        ]
        self.assert_guardrail_payload_fails(payload)
