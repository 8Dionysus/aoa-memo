from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "agents" / "validate_semantic_agents.py"
sys.path.insert(0, str(REPO_ROOT / "scripts" / "agents"))


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_semantic_agents", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_required_docs(module, root: Path) -> None:
    for spec in module.REQUIRED_DOCS:
        path = root / spec.path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# AGENTS.md\n" + "\n".join(spec.required_snippets) + "\n", encoding="utf-8")
    for spec in module.REQUIRED_VALIDATION_DOCS:
        path = root / spec.path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "# Owner Skill Validation\n" + "\n".join(spec.required_snippets) + "\n",
            encoding="utf-8",
        )


class ValidateSemanticAgentsTests(unittest.TestCase):
    def test_repository_semantic_docs_validate(self) -> None:
        module = load_validator()
        self.assertEqual(module.validate(REPO_ROOT), [])

    def test_missing_required_doc_fails(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_required_docs(module, root)
            missing = root / module.REQUIRED_DOCS[0].path
            missing.unlink()
            issues = module.validate(root)
        self.assertTrue(any("file is missing" in issue for issue in issues))

    def test_missing_required_snippet_fails(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_required_docs(module, root)
            target_spec = module.REQUIRED_DOCS[0]
            target = root / target_spec.path
            first_snippet = target_spec.required_snippets[0]
            target.write_text("# AGENTS.md\n" + "\n".join(target_spec.required_snippets[1:]) + "\n", encoding="utf-8")
            issues = module.validate(root)
        self.assertTrue(any(first_snippet in issue for issue in issues))

    def test_route_residue_guard_rejects_empty_section_and_dangling_leadin(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "AGENTS.md"
            target.write_text(
                "# AGENTS.md\n\n## Validation\n\n## Closeout\n",
                encoding="utf-8",
            )
            issues = module.route_residue_issues(root)
            self.assertEqual(1, len(issues))

            target.write_text(
                "# AGENTS.md\n\n## Validation\nRun checks:\n\n## Closeout\n",
                encoding="utf-8",
            )
            issues = module.route_residue_issues(root)
            self.assertEqual(1, len(issues))

    def test_validate_reports_one_finding_per_residue(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_required_docs(module, root)
            target = root / module.REQUIRED_DOCS[0].path
            target.write_text(target.read_text(encoding="utf-8") + "\n## Validation\nRun checks:\n\n## Closeout\n", encoding="utf-8")
            issues = module.validate(root)
        residue_issues = [issue for issue in issues if "dangling validation lead-in" in issue]
        self.assertEqual(1, len(residue_issues))

    def test_skill_command_is_owned_by_validation_surface(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_required_docs(module, root)
            validation = root / module.REQUIRED_VALIDATION_DOCS[0].path
            validation.write_text("# Owner Skill Validation\n", encoding="utf-8")
            issues = module.validate(root)
        self.assertTrue(any("skills-ref validate" in issue for issue in issues))

    def test_route_residue_guard_ignores_fenced_design_example(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "DESIGN.AGENTS.md"
            target.write_text(
                "# DESIGN.AGENTS.md\n\n```markdown\n## Validation\nRun checks:\n```\n",
                encoding="utf-8",
            )
            self.assertEqual([], module.route_residue_issues(root))

    def test_route_residue_guard_rejects_stacked_and_same_level_leadins(self) -> None:
        module = load_validator()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "AGENTS.md"
            target.write_text(
                "# AGENTS.md\n\n## Validation\nFirst checks:\nSecond checks:\n\n## Closeout\n",
                encoding="utf-8",
            )
            issues = module.route_residue_issues(root)
            self.assertEqual(2, len(issues))

            target.write_text(
                "# AGENTS.md\n\n## Boundaries\n- First route:\n- Second route.\n",
                encoding="utf-8",
            )
            issues = module.route_residue_issues(root)
            self.assertEqual(1, len(issues))


if __name__ == "__main__":
    unittest.main()
