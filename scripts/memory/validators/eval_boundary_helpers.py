"""Trace/eval guardrail validation profile for memo contracts."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def _guardrail_case_input_refs(case: dict[str, object]) -> set[str]:
    values = case.get("input_refs", [])
    if not isinstance(values, list):
        return set()
    return {value for value in values if isinstance(value, str)}

def _has_ref_with_prefix(refs: set[str], prefixes: tuple[str, ...]) -> bool:
    return any(ref.startswith(prefix) for ref in refs for prefix in prefixes)
