"""Profile dispatcher for memo validation lanes."""

from __future__ import annotations

from collections.abc import Callable

from . import eval_boundary, handoff_boundary, memory_context, runtime_boundary, schema

PROFILE_NAMES = (
    "all",
    "schema",
    "memory-context",
    "runtime-boundary",
    "handoff-boundary",
    "eval-boundary",
)

_PROFILE_RUNNERS: dict[str, Callable[[], None]] = {
    "schema": schema.run,
    "memory-context": memory_context.run,
    "runtime-boundary": runtime_boundary.run,
    "handoff-boundary": handoff_boundary.run,
    "eval-boundary": eval_boundary.run,
}


def run_profile(profile: str) -> None:
    if profile == "all":
        for child_profile in PROFILE_NAMES:
            if child_profile != "all":
                run_profile(child_profile)
        return
    try:
        runner = _PROFILE_RUNNERS[profile]
    except KeyError as exc:
        raise ValueError(f"unknown validation profile: {profile}") from exc
    runner()
