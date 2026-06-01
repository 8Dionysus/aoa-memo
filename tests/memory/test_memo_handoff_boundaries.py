from __future__ import annotations

import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import *  # noqa: F403


class MemoHandoffBoundaryTestCase(MemoValidatorTestCase):
    def test_routing_memory_adoption_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_routing_memory_adoption_surface()
    def test_routing_memory_adoption_surface_rejects_router_contract_without_capsule_step(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall" / "recall_contract.router.semantic.json"
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> object:
            payload = original_load_json(path)
            if Path(path) == recall_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload.pop("capsule_surface", None)
            return payload

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_routing_memory_adoption_surface)
    def test_playbook_memory_scope_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_playbook_memory_scope_surface()
    def test_playbook_memory_scope_surface_rejects_widened_working_scope(self) -> None:
        recall_path = validate_memo.EXAMPLES / "recall" / "recall_contract.working.json"
        original_load_json = validate_memo.load_json

        def side_effect(path: Path) -> object:
            payload = original_load_json(path)
            if Path(path) == recall_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload["allowed_scopes"] = ["thread", "session", "project", "ecosystem"]
            return payload

        with patch.object(validate_memo, "load_json", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_playbook_memory_scope_surface)
    def test_kag_export_validator_rejects_wrong_owner_repo(self) -> None:
        payload = self.kag_export_payload()
        payload["owner_repo"] = "aoa-kag"
        self.assert_kag_export_payload_fails(payload)
    def test_kag_export_validator_rejects_wrong_entry_surface(self) -> None:
        payload = self.kag_export_payload()
        payload["entry_surface"]["path"] = "generated/memory-objects/memory_object_sections.full.json"
        self.assert_kag_export_payload_fails(payload)
    def test_kag_export_validator_rejects_missing_tos_supporting_input(self) -> None:
        payload = self.kag_export_payload()
        payload["source_inputs"] = [payload["source_inputs"][0]]
        self.assert_kag_export_payload_fails(payload)
    def test_kag_export_validator_rejects_wrong_section_handles(self) -> None:
        payload = self.kag_export_payload()
        payload["section_handles"] = [
            "identity-and-recall",
            "bridges-and-access",
        ]
        self.assert_kag_export_payload_fails(payload)
    def test_kag_export_validator_rejects_missing_required_direct_relation(self) -> None:
        payload = self.kag_export_payload()
        payload["direct_relations"] = payload["direct_relations"][:-1]
        self.assert_kag_export_payload_fails(payload)
    def test_kag_export_validator_rejects_missing_source_memory_object_relation(self) -> None:
        payload = self.kag_export_payload()
        payload["direct_relations"] = [
            relation
            for relation in payload["direct_relations"]
            if relation["relation_type"] != "source_memory_object"
        ]
        self.assert_kag_export_payload_fails(payload)
    def test_kag_export_validator_rejects_missing_provenance_thread_relation(self) -> None:
        payload = self.kag_export_payload()
        payload["direct_relations"] = [
            relation
            for relation in payload["direct_relations"]
            if relation["relation_type"] != "provenance_thread"
        ]
        self.assert_kag_export_payload_fails(payload)
