from __future__ import annotations

import sys
from pathlib import Path

TEST_DIR = Path(__file__).resolve().parent
if str(TEST_DIR) not in sys.path:
    sys.path.insert(0, str(TEST_DIR))

from memo_validator_test_support import *  # noqa: F403


class MemoQuestbookBoundaryTestCase(MemoValidatorTestCase):
    def test_questbook_surface_validates(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_questbook_surface()
    def test_questbook_surface_flags_duplicate_quest_ids(self) -> None:
        paths = [
            validate_memo.ROOT / "quests" / "memo" / "active" / "AOA-MEM-Q-9999.yaml",
            validate_memo.ROOT / "quests" / "memo" / "done" / "AOA-MEM-Q-9999.yaml",
        ]

        issues = validate_memo.duplicate_questbook_file_issues(paths)

        self.assertEqual(len(issues), 1)
        self.assertIn("duplicate quest id AOA-MEM-Q-9999", issues[0])
    def test_quest_surface_builder_check_validates(self) -> None:
        argv = ["build_quest_surfaces.py", "--check"]
        with patch.object(sys, "argv", argv):
            with io.StringIO() as stdout, io.StringIO() as stderr:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    self.assertEqual(build_quest_surfaces.main(), 0)
    def test_questbook_surface_skips_missing_external_eval_schemas(self) -> None:
        missing_evals_root = REPO_ROOT / ".tmp" / "missing-aoa-evals"

        validate_memo.external_quest_schema_validator.cache_clear()
        self.addCleanup(validate_memo.external_quest_schema_validator.cache_clear)
        with patch.object(validate_memo, "AOA_EVALS_ROOT", missing_evals_root):
            with io.StringIO() as stdout, io.StringIO() as stderr:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    validate_memo.validate_questbook_surface()
    def test_questbook_surface_skips_missing_external_orchestrator_catalog(self) -> None:
        missing_agents_root = REPO_ROOT / ".tmp" / "missing-aoa-agents"

        validate_memo.load_live_orchestrator_class_ids.cache_clear()
        self.addCleanup(validate_memo.load_live_orchestrator_class_ids.cache_clear)
        with patch.object(validate_memo, "AOA_AGENTS_ROOT", missing_agents_root):
            with io.StringIO() as stdout, io.StringIO() as stderr:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    validate_memo.validate_questbook_surface()
    def test_questbook_surface_rejects_missing_tracked_reference(self) -> None:
        questbook_path = validate_memo.QUESTBOOK_PATH
        original_load_text = validate_memo.load_text

        def side_effect(path: Path) -> str:
            text = original_load_text(path)
            if Path(path) == questbook_path:
                return text.replace("AOA-MEM-Q-0003", "AOA-MEM-Q-9999")
            return text

        with patch.object(validate_memo, "load_text", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)
    def test_questbook_surface_rejects_source_owned_boundary_phrase_loss(self) -> None:
        doc_path = validate_memo.QUESTBOOK_DOC
        original_load_text = validate_memo.load_text

        def side_effect(path: Path) -> str:
            text = original_load_text(path)
            if Path(path) == doc_path:
                return text.replace("quest state remains source-owned", "quest state remains external")
            return text

        with patch.object(validate_memo, "load_text", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)
    def test_questbook_surface_rejects_quest_id_mismatch(self) -> None:
        quest_path = validate_memo.discover_questbook_files()["AOA-MEM-Q-0002"]
        original_load_yaml = validate_memo.load_yaml

        def side_effect(path: Path) -> object:
            payload = original_load_yaml(path)
            if Path(path) == quest_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload["id"] = "AOA-MEM-Q-9999"
            return payload

        with patch.object(validate_memo, "load_yaml", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)
    def test_questbook_surface_rejects_stale_foundation_owner_route(self) -> None:
        quest_path = validate_memo.discover_questbook_files()["AOA-MEM-Q-0002"]
        original_load_yaml = validate_memo.load_yaml

        def side_effect(path: Path) -> object:
            payload = original_load_yaml(path)
            if Path(path) == quest_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload["owner_surface"] = "mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md"
            return payload

        with patch.object(validate_memo, "load_yaml", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)
    def test_questbook_surface_rejects_stale_chronicle_owner_route(self) -> None:
        quest_path = validate_memo.discover_questbook_files()["AOA-MEM-Q-0003"]
        original_load_yaml = validate_memo.load_yaml

        def side_effect(path: Path) -> object:
            payload = original_load_yaml(path)
            if Path(path) == quest_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload["owner_surface"] = "memo/quest-chronicle"
            return payload

        with patch.object(validate_memo, "load_yaml", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)
    def test_questbook_surface_accepts_additive_chronicle_quest(self) -> None:
        with io.StringIO() as stdout, io.StringIO() as stderr:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                validate_memo.validate_questbook_surface()
    def test_questbook_surface_rejects_missing_additive_anchor_doc(self) -> None:
        quest_path = validate_memo.discover_questbook_files()["AOA-MEM-Q-0003"]
        original_load_yaml = validate_memo.load_yaml

        def side_effect(path: Path) -> object:
            payload = original_load_yaml(path)
            if Path(path) == quest_path:
                assert isinstance(payload, dict)
                payload = copy.deepcopy(payload)
                payload["anchor_ref"] = {
                    "artifact": "quest_chronicle_writeback",
                    "ref": "docs/DOES_NOT_EXIST.md",
                }
            return payload

        with patch.object(validate_memo, "load_yaml", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)
    def test_questbook_surface_rejects_listed_additive_quest_without_file(self) -> None:
        questbook_path = validate_memo.QUESTBOOK_PATH
        original_load_text = validate_memo.load_text

        def side_effect(path: Path) -> str:
            text = original_load_text(path)
            if Path(path) == questbook_path:
                return text + "\n- `AOA-MEM-Q-9999` - stale additive quest reference\n"
            return text

        with patch.object(validate_memo, "load_text", side_effect=side_effect):
            self.assert_system_exit_quietly(validate_memo.validate_questbook_surface)
