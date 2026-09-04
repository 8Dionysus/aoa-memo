from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DECISIONS_DIR = Path("docs/decisions")
INDEXES_DIR = DECISIONS_DIR / "indexes"
INDEX_CONTRACT_PATH = INDEXES_DIR / "index_contract.yaml"
DECISION_ID_RE = re.compile(r"^- Decision ID: (AOA-MEM-D-(\d{4}))$", re.MULTILINE)
DATE_VALUE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FULL_ID_FILENAME_RE = re.compile(r"^(AOA-MEM-D-(\d{4}))-.+\.md$")
DECISION_LANE_CONTROL_FILES = (
    "AGENTS.md",
    "README.md",
    "TEMPLATE.md",
    "VALIDATION.md",
)

SURFACE_CLASS_ORDER = (
    "root/topology",
    "memory doctrine",
    "reviewed corpus",
    "generated/readout",
    "local port/writeback",
    "lifecycle/retention",
    "consumer handoff",
    "mechanic package",
    "mechanic part",
    "validation guard",
    "agents/mesh",
    "skills/home",
    "quest/lane",
    "boundary/runtime/sibling",
    "release/tooling",
    "legacy/provenance",
)
MECHANIC_PARENT_ORDER = (
    "adoption",
    "agon",
    "antifragility",
    "checkpoint",
    "consumer-handoff",
    "governance",
    "lineage-harvest",
    "operational-gate",
    "questbook",
    "readiness-boundary",
    "recurrence-support",
    "retention",
    "shape-guard",
    "titan",
    "writeback",
    "cross-parent",
)
GUARD_FAMILY_ORDER = (
    "decision index/read-model",
    "root technical district",
    "docs route",
    "mechanic topology",
    "part and payload",
    "generated/read-model",
    "reviewed corpus/intake",
    "local port/writeback",
    "memory surface",
    "skill admission",
    "source/projection parity",
    "lifecycle/retention",
    "AGENTS/mesh",
    "quest/read-model",
    "release/tooling",
    "sibling and boundary",
)
MEMORY_OBJECT_CLASS_ORDER = (
    "decision",
    "episode",
    "claim",
    "pattern",
    "state_capsule",
    "audit_event",
    "provenance_thread",
    "support_object",
    "recall_contract",
    "reviewed_intake",
    "local_candidate",
)

GENERATED_INDEX_PATHS = (
    INDEXES_DIR / "README.md",
    INDEXES_DIR / "by-number.md",
    INDEXES_DIR / "by-date.md",
    INDEXES_DIR / "by-surface.md",
    INDEXES_DIR / "by-mechanic.md",
    INDEXES_DIR / "by-guard.md",
    INDEXES_DIR / "by-memory-object-class.md",
)
