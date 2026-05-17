from __future__ import annotations

import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script(relative_path: str):
    path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_safe_infra_change_keeps_hold_state_for_required_field_errors() -> None:
    module = load_script(".agents/skills/aoa-safe-infra-change/scripts/infra_change_contract.py")

    report = module.build_report(
        {
            "change_summary": "Regression check",
            "verification_steps": ["python -m pytest"],
            "rollback_steps": [],
        }
    )

    assert report["errors"]
    assert report["report_state"] == "hold"
