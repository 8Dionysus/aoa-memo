from __future__ import annotations

import copy
import io
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import (  # noqa: E402
    REPO_ROOT,
    MemoValidatorTestCase,
    load_json,
    validate_memo,
)

SUITE_PATH = (
    REPO_ROOT
    / "examples"
    / "support-objects"
    / "active_organ_memo_contracts_v1.examples.json"
)


def payload_for(case_id: str) -> dict:
    suite = load_json(SUITE_PATH)
    case = next(case for case in suite["valid_cases"] if case["case_id"] == case_id)
    return {**copy.deepcopy(suite["header_template"]), **copy.deepcopy(case["payload"])}


class ActiveOrganMemoContractTestCase(MemoValidatorTestCase):
    def test_contract_suite_is_valid_and_fail_closed(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_active_organ_contract_suite()

    def test_schema_rejects_unknown_version(self) -> None:
        payload = payload_for("C01-memory-evidence-envelope")
        payload["schema_version"] = "2.0.0"
        validator = validate_memo.validator_for("active_organ_memo_contracts_v1.schema.json")

        errors = list(validator.iter_errors(payload))

        self.assertNotEqual(errors, [])

    def test_transition_rejects_nonadvancing_version(self) -> None:
        payload = payload_for("C06-memory-lifecycle-transition")
        payload["expected_prior_version"] = payload["next_version"]

        errors = validate_memo._active_organ_contract_errors(payload)

        self.assertIn("next_version must equal expected_prior_version + 1", errors)

    def test_complete_erase_requires_exact_owner_coverage(self) -> None:
        payload = payload_for("C15-distributed-memory-erase-manifest")
        payload["owner_results"].pop()

        errors = validate_memo._active_organ_contract_errors(payload)

        self.assertIn("owner_results must cover owner_set exactly once", errors)

    def test_machine_erase_cannot_target_project_root(self) -> None:
        payload = payload_for("C16-per-owner-erase-work-item")
        payload["target_root"] = "/srv/AbyssOS/abyss-stack"
        validator = validate_memo.validator_for("active_organ_memo_contracts_v1.schema.json")

        errors = list(validator.iter_errors(payload))

        self.assertNotEqual(errors, [])

    def test_prohibited_data_cannot_enter_candidate_memory(self) -> None:
        payload = payload_for("C02-memory-candidate-packet")
        payload["data_class"] = "D4"

        errors = validate_memo._active_organ_contract_errors(payload)

        self.assertIn("D4 prohibited material cannot enter a memory candidate", errors)

    def test_tainted_recall_must_resolve_to_silence(self) -> None:
        payload = payload_for("C08-recall-packet")
        payload["taint"]["tainted"] = True
        payload["taint"]["labels"] = ["untrusted-input"]
        payload["taint"]["quarantine_required"] = True
        payload["result_mode"] = "bounded_memory"

        errors = validate_memo._active_organ_contract_errors(payload)

        self.assertIn("tainted recall packet must resolve to silence", errors)

    def test_active_projection_requires_exact_current_generation(self) -> None:
        payload = payload_for("C12-memory-projection-manifest")
        payload["projected_generation"] = payload["source_generation"] - 1

        errors = validate_memo._active_organ_contract_errors(payload)

        self.assertTrue(
            any(
                error.startswith(
                    "active projection requires exact current source generation"
                )
                for error in errors
            )
        )

    def test_invalidated_projection_cannot_return_to_recall_without_receipt(
        self,
    ) -> None:
        payload = payload_for("C12-memory-projection-manifest")
        payload["projection_state"] = "invalidated"
        payload["recall_eligible"] = False
        payload["rebuild_required"] = True

        errors = validate_memo._active_organ_contract_errors(payload)

        self.assertIn(
            "invalidated projection must cite its invalidation receipt",
            errors,
        )

    def test_erase_surface_id_must_match_its_class(self) -> None:
        payload = payload_for("C15-distributed-memory-erase-manifest")
        payload["erase_surfaces"][0]["surface_class"] = "runtime"

        errors = validate_memo._active_organ_contract_errors(payload)

        self.assertIn("ER0 must use surface_class canonical_object", errors)

    def test_machine_work_item_must_remain_er6(self) -> None:
        payload = payload_for("C16-per-owner-erase-work-item")
        payload["erase_surface_id"] = "ER4"

        errors = validate_memo._active_organ_contract_errors(payload)

        self.assertIn("abyss-machine erase work must remain host-owned ER6", errors)
