from __future__ import annotations

from ._shared_paths import ROOT

FOUNDATION_QUESTBOOK_FILES = {
    "AOA-MEM-Q-0001": ROOT / "quests" / "memo" / "done" / "AOA-MEM-Q-0001.yaml",
    "AOA-MEM-Q-0002": ROOT / "quests" / "memo" / "done" / "AOA-MEM-Q-0002.yaml",
}
QUESTBOOK_FILES = FOUNDATION_QUESTBOOK_FILES
CLOSED_QUEST_STATES = {"done", "dropped"}
QUEST_LIFECYCLE_STATES = {
    "captured",
    "triaged",
    "ready",
    "active",
    "blocked",
    "reanchor",
    "done",
    "dropped",
}
ALLOWED_ORCHESTRATOR_CAPABILITY_TARGETS = {
    "repo_layer_selection",
    "evidence_closure",
    "bounded_next_step",
}
ORCHESTRATOR_MEMORY_QUESTS = {
    "AOA-MEM-Q-0004": ("aoa-agents:router", "repo_layer_selection"),
    "AOA-MEM-Q-0005": ("aoa-agents:review", "evidence_closure"),
    "AOA-MEM-Q-0006": ("aoa-agents:bounded_execution", "bounded_next_step"),
}
EXPECTED_QUEST_OWNER_SURFACES = {
    "AOA-MEM-Q-0001": "mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md",
    "AOA-MEM-Q-0002": "mechanics/recurrence-support/docs/WITNESS_TRACE_CONTRACT.md",
    "AOA-MEM-Q-0003": "mechanics/writeback/docs/QUEST_CHRONICLE_WRITEBACK.md",
    "AOA-MEM-Q-0004": "mechanics/consumer-handoff/docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md",
    "AOA-MEM-Q-0005": "mechanics/consumer-handoff/docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md",
    "AOA-MEM-Q-0006": "mechanics/consumer-handoff/docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md",
    "AOA-MEM-Q-0007": "mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md",
    "AOA-MEM-Q-0008": "mechanics/writeback/docs/QUEST_EVIDENCE_WRITEBACK.md",
    "AOA-MEM-Q-0009": "mechanics/recurrence-support/docs/REVIEWED_CLOSEOUT_RECALL_LANDING.md",
}
QUEST_LOCAL_DOC_PREFIXES = (
    "docs/",
    "mechanics/antifragility/docs/",
    "mechanics/agon/docs/",
    "mechanics/adoption/docs/",
    "mechanics/checkpoint/docs/",
    "mechanics/consumer-handoff/docs/",
    "mechanics/governance/docs/",
    "mechanics/lineage-harvest/docs/",
    "mechanics/operational-gate/docs/",
    "mechanics/readiness-boundary/docs/",
    "mechanics/recurrence-support/docs/",
    "mechanics/retention/docs/",
    "mechanics/shape-guard/docs/",
    "mechanics/titan/docs/",
    "mechanics/writeback/docs/",
)
ORCHESTRATOR_MEMORY_REQUIRED_TOKENS = (
    "## Router",
    "## Review",
    "## Bounded execution",
    "## Boundary rule",
    "must not redefine orchestrator identity or make memo the owner of active quest state",
)
