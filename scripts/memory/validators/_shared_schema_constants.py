from __future__ import annotations

import re

from jsonschema import FormatChecker

FORMAT_CHECKER = FormatChecker()
RFC3339_DATETIME = re.compile(
    r"^(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})"
    r"[Tt](?P<hour>[0-9]{2}):(?P<minute>[0-9]{2}):(?P<second>[0-9]{2})"
    r"(?:\.[0-9]+)?(?P<zone>[Zz]|(?P<offset_sign>[+-])(?P<offset_hour>[0-9]{2}):(?P<offset_minute>[0-9]{2}))$"
)
RFC3339_UTC_LEAP_SECOND_DATES = frozenset(
    (
        (1972, 6, 30),
        (1972, 12, 31),
        (1973, 12, 31),
        (1974, 12, 31),
        (1975, 12, 31),
        (1976, 12, 31),
        (1977, 12, 31),
        (1978, 12, 31),
        (1979, 12, 31),
        (1981, 6, 30),
        (1982, 6, 30),
        (1983, 6, 30),
        (1985, 6, 30),
        (1987, 12, 31),
        (1989, 12, 31),
        (1990, 12, 31),
        (1992, 6, 30),
        (1993, 6, 30),
        (1994, 6, 30),
        (1995, 12, 31),
        (1997, 6, 30),
        (1998, 12, 31),
        (2005, 12, 31),
        (2008, 12, 31),
        (2012, 6, 30),
        (2015, 6, 30),
        (2016, 12, 31),
    )
)
MARKDOWN_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
README_CURRENT_RELEASE = re.compile(r"Current release:\s+`v(?P<version>\d+\.\d+\.\d+)`")
CHANGELOG_RELEASE_HEADING = re.compile(r"^## \[(?P<version>\d+\.\d+\.\d+)\]", re.MULTILINE)
SYMBOLIC_REF = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*:")
WINDOWS_ABSOLUTE_PATH = re.compile(r"^[A-Za-z]:[\\\\/]")
QUEST_ID_PATTERN = re.compile(r"\bAOA-MEM-Q-\d{4}\b")
CORE_KIND_SCHEMA_MAP = {
    "anchor": "schemas/memory-objects/anchor.schema.json",
    "state_capsule": "schemas/memory-objects/state_capsule.schema.json",
    "episode": "schemas/memory-objects/episode.schema.json",
    "claim": "schemas/memory-objects/claim.schema.json",
    "decision": "schemas/memory-objects/decision.schema.json",
    "pattern": "schemas/memory-objects/pattern.schema.json",
    "bridge": "schemas/memory-objects/bridge.schema.json",
    "audit_event": "schemas/memory-objects/audit_event.schema.json",
}
CORE_KIND_EXAMPLE_MAP = {
    "anchor": "anchor.example.json",
    "state_capsule": "state_capsule.example.json",
    "episode": "episode.example.json",
    "claim": "claim.example.json",
    "decision": "checkpoint_approval_record.example.json",
    "pattern": "pattern.example.json",
    "bridge": "bridge.kag-lift.example.json",
    "audit_event": "audit_event.supersession.example.json",
}
PHASE_ALPHA_OBJECT_EXAMPLES_BY_KIND = {
    "state_capsule": [
        "state_capsule.phase-alpha-local-stack.example.json",
        "state_capsule.phase-alpha-long-horizon.example.json",
        "state_capsule.phase-alpha-restartable-inquiry.example.json",
    ],
    "episode": [
        "episode.phase-alpha-local-stack.example.json",
        "episode.phase-alpha-validation-remediation.example.json",
        "episode.phase-alpha-validation-remediation-rerun.example.json",
        "episode.phase-alpha-long-horizon.example.json",
    ],
    "decision": [
        "decision.phase-alpha-local-stack.example.json",
        "decision.phase-alpha-self-agent-checkpoint.example.json",
        "decision.phase-alpha-validation-remediation.example.json",
        "decision.phase-alpha-validation-remediation-rerun.example.json",
        "decision.phase-alpha-long-horizon.example.json",
        "decision.phase-alpha-restartable-inquiry.example.json",
    ],
    "claim": [
        "claim.phase-alpha-closure-with-residual-runtime-history.example.json",
        "claim.phase-alpha-rerun-pending-handoff.example.json",
        "claim.phase-alpha-runtime-history-fully-retired.example.json",
        "claim.phase-alpha-runtime-history-later-infra-track.example.json",
    ],
    "pattern": [
        "pattern.phase-alpha-remediation-recurrence.example.json",
    ],
    "audit_event": [
        "audit_event.phase-alpha-self-agent-checkpoint.example.json",
        "audit_event.phase-alpha-validation-remediation.example.json",
        "audit_event.phase-alpha-validation-remediation-rerun.example.json",
        "audit_event.phase-alpha-rerun-pending-supersession.example.json",
        "audit_event.phase-alpha-runtime-history-overread-retraction.example.json",
    ],
}
PHASE_ALPHA_OBJECT_EXAMPLE_NAMES = tuple(
    example_name
    for example_names in PHASE_ALPHA_OBJECT_EXAMPLES_BY_KIND.values()
    for example_name in example_names
)
PHASE_ALPHA_PROVENANCE_THREAD_EXAMPLE = "provenance_thread.phase-alpha-curated.example.json"
SELF_AGENCY_CONTINUITY_PROVENANCE_THREAD_EXAMPLE = "provenance_thread.self-agency-continuity.example.json"
SELF_AGENCY_CONTINUITY_OBJECT_EXAMPLES_BY_KIND = {
    "decision": [
        "decision.self-agency-reanchor-window.example.json",
    ],
    "state_capsule": [
        "state_capsule.self-agency-continuity-relay.example.json",
    ],
}
SELF_AGENCY_CONTINUITY_OBJECT_EXAMPLE_NAMES = tuple(
    example_name
    for example_names in SELF_AGENCY_CONTINUITY_OBJECT_EXAMPLES_BY_KIND.values()
    for example_name in example_names
)
SELF_AGENCY_CONTINUITY_EXPECTED_OBJECT_PATHS = {
    "memo.decision.2026-04-12.self-agency-reanchor-window": (
        "mechanics/writeback/parts/growth-and-continuity/examples/decision.self-agency-reanchor-window.example.json"
    ),
    "memo.state.2026-04-12.self-agency-continuity-relay": (
        "mechanics/writeback/parts/growth-and-continuity/examples/state_capsule.self-agency-continuity-relay.example.json"
    ),
}
SELF_AGENCY_CONTINUITY_REQUIRED_SOURCE_REFS = [
    "repo:aoa-agents/examples/self_agent_checkpoint/self_agency_continuity_window.example.json",
    "repo:aoa-sdk/examples/closeout_continuity_window.example.json",
    "repo:aoa-playbooks/playbooks/self-agency-continuity-cycle/PLAYBOOK.md",
    "repo:aoa-evals/bundles/aoa-continuity-anchor-integrity/EVAL.md",
    "repo:aoa-evals/bundles/aoa-self-reanchor-correctness/EVAL.md",
]
KAG_EXPORT_REQUIRED_FIELDS = {
    "owner_repo",
    "kind",
    "object_id",
    "primary_question",
    "summary_50",
    "summary_200",
    "source_inputs",
    "entry_surface",
    "section_handles",
    "direct_relations",
    "provenance_note",
    "non_identity_boundary",
}
