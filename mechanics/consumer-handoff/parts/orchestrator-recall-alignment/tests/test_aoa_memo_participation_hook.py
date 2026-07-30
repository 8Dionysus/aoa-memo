from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

from jsonschema import Draft202012Validator, FormatChecker
import pytest


PART_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PART_ROOT / "scripts" / "aoa_memo_participation_hook.py"
RECEIPT_SCHEMA_PATH = (
    PART_ROOT / "schemas" / "aoa_memo_participation_receipt_v0.schema.json"
)
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

SPEC = importlib.util.spec_from_file_location("aoa_memo_participation_hook", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
HOOK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOOK)


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def base_event(event_name: str, *, session_id: str = "session-private-id") -> dict:
    return {
        "session_id": session_id,
        "transcript_path": "/private/raw/transcript.jsonl",
        "cwd": "/srv/AbyssOS/aoa-memo",
        "hook_event_name": event_name,
        "model": "gpt-5.6-sol",
        "permission_mode": "dontAsk",
        "turn_id": "turn-private-id",
    }


def run_hook(state_root: Path, payload: object, *, strict: bool = False) -> subprocess.CompletedProcess:
    command = [
        sys.executable,
        str(SCRIPT_PATH),
        "observe",
        "--state-root",
        str(state_root),
    ]
    if strict:
        command.append("--strict")
    return subprocess.run(
        command,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )


def receipt_logs(state_root: Path) -> list[Path]:
    return sorted((state_root / "sessions").glob("*.jsonl"))


def receipts(state_root: Path) -> list[dict]:
    logs = receipt_logs(state_root)
    assert len(logs) == 1
    return [
        json.loads(line)
        for line in logs[0].read_text(encoding="utf-8").splitlines()
        if line
    ]


@pytest.mark.parametrize(
    ("prompt", "workspace", "route", "opportunity", "state"),
    [
        (
            "Продолжай работу в aoa-sdk и сначала проверь прежнее решение об owner boundary.",
            "aoa-sdk",
            "aoa-memo-orient",
            "reviewed_context_orientation",
            "eligible",
        ),
        (
            "Why did we choose the federated owner boundary in Abyss?",
            "other",
            "aoa-memo-orient",
            "reviewed_context_orientation",
            "eligible",
        ),
        (
            "Проверь lifecycle объекта памяти memo:decision:42 и его superseded ref.",
            "other",
            "aoa-memo-deep",
            "existing_memory_deep",
            "eligible",
        ),
        (
            "Сохрани повторяемый урок из этого PR как кандидат памяти.",
            "other",
            "aoa-memo-writeback",
            "first_writeback_handoff",
            "handoff",
        ),
        (
            "Подними прошлую .aoa сессию и найди сырой transcript.",
            "other",
            "aoa-session-memory",
            "raw_session_handoff",
            "handoff",
        ),
        (
            "Исправь опечатку в текущем README.",
            "aoa-memo",
            "none",
            "none",
            "not_applicable",
        ),
        (
            "Запиши обычную заметку о покупке кофе.",
            "other",
            "none",
            "none",
            "not_applicable",
        ),
    ],
)
def test_trigger_classifier_is_bounded(
    prompt: str,
    workspace: str,
    route: str,
    opportunity: str,
    state: str,
) -> None:
    result = HOOK.classify_prompt(prompt, workspace)
    assert result["route_class"] == route
    assert result["opportunity_class"] == opportunity
    assert result["opportunity_state"] == state


def test_internal_goal_continuation_is_excluded() -> None:
    result = HOOK.classify_prompt(
        '<codex_internal_context source="goal">continue AoA prior decision</codex_internal_context>',
        "aoa-memo",
    )
    assert result == {
        "route_class": "none",
        "opportunity_class": "synthetic_continuation",
        "opportunity_state": "excluded",
        "prompt_length_bucket": "short",
        "synthetic_continuation_excluded": True,
    }


def test_receipts_validate_and_persist_no_prompt_tool_or_transcript_content(
    tmp_path: Path,
) -> None:
    state_root = tmp_path / "state"
    prompt = "SECRET-PROMPT continue prior AoA owner decision"
    prompt_event = base_event("UserPromptSubmit")
    prompt_event["prompt"] = prompt
    prompt_result = run_hook(state_root, prompt_event)

    tool_event = base_event("PostToolUse")
    tool_event.update(
        {
            "tool_name": "mcp__aoa_memo__aoa_memo_brief",
            "tool_use_id": "tool-private-id",
            "tool_input": {"query": "SECRET-TOOL-INPUT"},
            "tool_response": {
                "content": [{"type": "text", "text": "SECRET-MEMORY-PAYLOAD"}]
            },
        }
    )
    tool_result = run_hook(state_root, tool_event)

    assert prompt_result.returncode == 0
    assert prompt_result.stdout == ""
    assert prompt_result.stderr == ""
    assert tool_result.returncode == 0
    assert tool_result.stdout == ""
    assert tool_result.stderr == ""

    payloads = receipts(state_root)
    schema = load_json(RECEIPT_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for payload in payloads:
        validator.validate(payload)
    assert HOOK.verify_chain(payloads) == []

    persisted = canonical_persisted = "\n".join(
        json.dumps(item, ensure_ascii=False, sort_keys=True) for item in payloads
    )
    assert persisted == canonical_persisted
    for forbidden in (
        prompt,
        "SECRET-TOOL-INPUT",
        "SECRET-MEMORY-PAYLOAD",
        "/private/raw/transcript.jsonl",
        "/srv/AbyssOS/aoa-memo",
        "session-private-id",
        "turn-private-id",
        "tool-private-id",
    ):
        assert forbidden not in persisted

    assert payloads[0]["evidence_ladder"]["noticed"] == "unknown"
    assert payloads[1]["evidence_ladder"]["invocation"] == "observed"
    assert payloads[1]["evidence_ladder"]["result_returned"] == "observed"
    assert payloads[1]["evidence_ladder"]["used_or_rejected"] == "unknown"
    assert payloads[1]["evidence_ladder"]["outcome"] == "unknown"
    assert not any(payloads[1]["authority"].values())


def test_all_lifecycle_events_are_silent_and_schema_valid(tmp_path: Path) -> None:
    state_root = tmp_path / "state"
    events = [
        {**base_event("SessionStart"), "source": "resume"},
        {**base_event("PreCompact"), "trigger": "auto"},
        {**base_event("PostCompact"), "trigger": "auto"},
        {**base_event("Stop"), "stop_hook_active": False, "last_assistant_message": "SECRET"},
        {**base_event("SessionEnd"), "reason": "other"},
    ]
    for event in events:
        result = run_hook(state_root, event)
        assert result.returncode == 0
        assert result.stdout == ""
        assert result.stderr == ""

    payloads = receipts(state_root)
    validator = Draft202012Validator(
        load_json(RECEIPT_SCHEMA_PATH),
        format_checker=FormatChecker(),
    )
    for payload in payloads:
        validator.validate(payload)
    assert HOOK.verify_chain(payloads) == []
    assert "SECRET" not in json.dumps(payloads)


def test_concurrent_hooks_preserve_one_hash_chain(tmp_path: Path) -> None:
    state_root = tmp_path / "state"
    event = base_event("UserPromptSubmit", session_id="concurrent-session")
    event["prompt"] = "Continue prior AoA decision."

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda _: run_hook(state_root, event), range(24)))

    assert all(result.returncode == 0 for result in results)
    assert all(result.stdout == "" and result.stderr == "" for result in results)
    payloads = receipts(state_root)
    assert len(payloads) == 24
    assert [payload["sequence"] for payload in payloads] == list(range(1, 25))
    assert HOOK.verify_chain(payloads) == []


def test_invalid_input_fails_open_without_content_output(tmp_path: Path) -> None:
    state_root = tmp_path / "state"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_PATH),
            "observe",
            "--state-root",
            str(state_root),
        ],
        input="{not-json SECRET",
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout == ""
    assert result.stderr == ""
    failure_log = (state_root / "hook-failures.jsonl").read_text(encoding="utf-8")
    assert "SECRET" not in failure_log
    assert "JSONDecodeError" in failure_log
