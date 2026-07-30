from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys

from jsonschema import Draft202012Validator


PART_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PART_ROOT / "scripts" / "aoa_memo_participation_hook.py"
FRAGMENT_SCHEMA_PATH = (
    PART_ROOT
    / "schemas"
    / "aoa_memo_participation_hook_fragment_v0.schema.json"
)
FRAGMENT_PATH = (
    PART_ROOT
    / "config"
    / "codex-hooks.aoa-memo-participation-shadow.fragment.json"
)

SPEC = importlib.util.spec_from_file_location("aoa_memo_participation_contract", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
HOOK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOOK)


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def run_prompt_hook(state_root: Path) -> subprocess.CompletedProcess:
    event = {
        "session_id": "session-private-id",
        "transcript_path": "/private/raw/transcript.jsonl",
        "cwd": "/srv/AbyssOS/aoa-memo",
        "hook_event_name": "UserPromptSubmit",
        "model": "gpt-5.6-sol",
        "permission_mode": "dontAsk",
        "turn_id": "turn-private-id",
        "prompt": "Continue prior AoA decision.",
    }
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "observe",
            "--state-root",
            str(state_root),
        ],
        input=json.dumps(event),
        text=True,
        capture_output=True,
        check=False,
    )


def test_summary_refuses_to_claim_use_or_benefit(tmp_path: Path) -> None:
    state_root = tmp_path / "state"
    assert run_prompt_hook(state_root).returncode == 0

    summary = HOOK.build_summary(state_root)
    assert summary["receipt_logs_valid"] is True
    assert summary["counts"]["routes"]["aoa-memo-orient"] == 1
    assert summary["claims"] == {
        "noticed": "unknown",
        "used_or_rejected": "unknown",
        "action_change": "unknown",
        "outcome": "unknown",
        "benefit_claim_allowed": False,
        "reason": (
            "shadow receipts prove only opportunity classification and "
            "observed aoa_memo tool-result stages"
        ),
    }


def test_hook_fragment_is_exact_shadow_only_and_compositor_bound() -> None:
    schema = load_json(FRAGMENT_SCHEMA_PATH)
    fragment = load_json(FRAGMENT_PATH)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(fragment)

    assert set(fragment["hooks"]) == HOOK.SUPPORTED_EVENTS
    assert "PermissionRequest" not in fragment["hooks"]
    assert "PreToolUse" not in fragment["hooks"]
    assert fragment["mode"] == "shadow"
    assert fragment["bindings"] == [
        "AOA_MEMO_HOOK_SCRIPT",
        "AOA_MEMO_STATE_ROOT",
    ]
    serialized = json.dumps(fragment)
    for forbidden_field in (
        "additionalContext",
        "systemMessage",
        '"continue"',
        '"decision"',
        "updatedInput",
        "stopReason",
    ):
        assert forbidden_field not in serialized
    for groups in fragment["hooks"].values():
        for group in groups:
            for handler in group["hooks"]:
                assert handler["type"] == "command"
                assert handler["timeout"] <= 2
                assert "{{AOA_MEMO_HOOK_SCRIPT}}" in handler["command"]
                assert "{{AOA_MEMO_STATE_ROOT}}" in handler["command"]
