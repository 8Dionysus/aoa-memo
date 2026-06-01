from __future__ import annotations

import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import *  # noqa: F403


class MemoRuntimeWritebackBoundaryTestCase(MemoValidatorTestCase):
    def assert_runtime_targets_payload_fails(self, payload: dict) -> None:
        target_path = validate_memo.RUNTIME_WRITEBACK_TARGETS_PATH
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> dict:
            if Path(path) == target_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_targets)

    def assert_runtime_intake_payload_fails(self, payload: dict) -> None:
        intake_path = validate_memo.RUNTIME_WRITEBACK_INTAKE_PATH
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> dict:
            if Path(path) == intake_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_runtime_writeback_intake)

    def test_runtime_writeback_targets_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_runtime_writeback_targets()

    def test_runtime_writeback_targets_surface_rejects_review_state_drift(self) -> None:
        payload = copy.deepcopy(load_json(validate_memo.RUNTIME_WRITEBACK_TARGETS_PATH))
        assert isinstance(payload, dict)
        for item in payload["targets"]:
            if item["runtime_surface"] == "distillation_claim_candidate":
                item["review_state_default"] = "captured"
                break

        self.assert_runtime_targets_payload_fails(payload)

    def test_runtime_writeback_targets_surface_rejects_duplicate_runtime_surface(self) -> None:
        payload = copy.deepcopy(load_json(validate_memo.RUNTIME_WRITEBACK_TARGETS_PATH))
        assert isinstance(payload, dict)
        payload["targets"][1]["runtime_surface"] = "checkpoint_export"

        self.assert_runtime_targets_payload_fails(payload)

    def test_runtime_writeback_targets_surface_rejects_incomplete_runtime_boundary(self) -> None:
        payload = copy.deepcopy(load_json(validate_memo.RUNTIME_WRITEBACK_TARGETS_PATH))
        assert isinstance(payload, dict)
        payload["runtime_boundary"] = {}

        self.assert_runtime_targets_payload_fails(payload)

    def test_runtime_writeback_intake_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_runtime_writeback_intake()

    def test_runtime_writeback_intake_surface_rejects_owner_review_ref_drift(self) -> None:
        payload = copy.deepcopy(load_json(validate_memo.RUNTIME_WRITEBACK_INTAKE_PATH))
        assert isinstance(payload, dict)
        payload["targets"][0]["owner_review_refs"] = ["mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md"]

        self.assert_runtime_intake_payload_fails(payload)

    def test_runtime_writeback_intake_surface_rejects_reviewed_candidate_posture_drift(self) -> None:
        payload = copy.deepcopy(load_json(validate_memo.RUNTIME_WRITEBACK_INTAKE_PATH))
        assert isinstance(payload, dict)
        for item in payload["targets"]:
            if item["runtime_surface"] == "distillation_claim_candidate":
                item["intake_posture"] = "capturable_runtime_export"
                break

        self.assert_runtime_intake_payload_fails(payload)

    def test_self_agency_continuity_writeback_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_self_agency_continuity_writeback_surface()

    def test_self_agency_continuity_writeback_rejects_unhydrated_memory_object_id(self) -> None:
        thread_path = validate_memo.example_path_for(
            "provenance_thread.self-agency-continuity.example.json"
        )
        original_load_json = validate_memo.load_json
        payload = copy.deepcopy(load_json(thread_path))
        assert isinstance(payload, dict)
        payload["memory_object_ids"].append("memo.state.2099-01-01.missing-continuity-relay")

        def side_effect(path: Path) -> object:
            if Path(path) == thread_path:
                return copy.deepcopy(payload)
            return original_load_json(path)

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(
                validate_memo.validate_self_agency_continuity_writeback_surface
            )
