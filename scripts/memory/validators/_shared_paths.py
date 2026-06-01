from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROOT_RESOLVED = ROOT.resolve()
AOA_AGENTS_ROOT = Path(os.environ.get("AOA_AGENTS_ROOT", ROOT.parent / "aoa-agents")).expanduser().resolve()
AOA_EVALS_ROOT = Path(os.environ.get("AOA_EVALS_ROOT", ROOT.parent / "aoa-evals")).expanduser().resolve()
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples"
GENERATED = ROOT / "generated"
MECHANICS = ROOT / "mechanics"
MECHANIC_SCHEMA_DIRS = tuple(
    sorted([*MECHANICS.glob("*/schemas"), *MECHANICS.glob("*/parts/*/schemas")])
)
MECHANIC_EXAMPLE_DIRS = tuple(
    sorted([*MECHANICS.glob("*/examples"), *MECHANICS.glob("*/parts/*/examples")])
)
WRITEBACK = MECHANICS / "writeback"
WRITEBACK_RUNTIME_PART = WRITEBACK / "parts" / "runtime-and-temperature"
WRITEBACK_GROWTH_PART = WRITEBACK / "parts" / "growth-and-continuity"
CONSUMER_HANDOFF = MECHANICS / "consumer-handoff"
CONSUMER_HANDOFF_KAG_SOURCE_EXPORT_PART = (
    CONSUMER_HANDOFF / "parts" / "kag-source-export"
)
READINESS_BOUNDARY = MECHANICS / "readiness-boundary"
RUNTIME_WRITEBACK_TARGETS_PATH = WRITEBACK_RUNTIME_PART / "generated" / "runtime_writeback_targets.min.json"
RUNTIME_WRITEBACK_INTAKE_PATH = WRITEBACK_RUNTIME_PART / "generated" / "runtime_writeback_intake.min.json"
RUNTIME_WRITEBACK_GOVERNANCE_PATH = WRITEBACK_RUNTIME_PART / "generated" / "runtime_writeback_governance.min.json"
GROWTH_REFINERY_WRITEBACK_LANES_PATH = WRITEBACK_GROWTH_PART / "generated" / "growth_refinery_writeback_lanes.min.json"
LIVE_RECEIPT_LOG_PATH = ROOT / ".aoa" / "live_receipts" / "memo-writeback-receipts.jsonl"
RECALL_SURFACE_PREFIX = "repo:aoa-memo/generated/memory-objects/memory_object_catalog.min.json#"
GROWTH_LANE_REF_PREFIX = "repo:aoa-memo/mechanics/writeback/parts/growth-and-continuity/generated/growth_refinery_writeback_lanes.min.json#"
LIVE_RECEIPT_ACTOR_BY_KIND = {
    "memo_writeback_receipt": "aoa-memo:runtime-writeback",
    "memo_growth_writeback_receipt": "aoa-memo:growth-refinery-writeback",
}
PHASE_ALPHA_WRITEBACK_MAP_PATH = WRITEBACK_GROWTH_PART / "examples" / "phase_alpha_writeback_map.example.json"
PHASE_ALPHA_WRITEBACK_OUTPUT_PATH = WRITEBACK_GROWTH_PART / "generated" / "phase_alpha_writeback_map.min.json"
MEMORY_READINESS_BOUNDARY_DOC_PATH = READINESS_BOUNDARY / "docs" / "MEMORY_READINESS_BOUNDARY.md"
MEMORY_READINESS_BOUNDARY_DOC_REF = "mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md"
MEMORY_READINESS_BOUNDARY_PRESSURE_REF = (
    "mechanics/readiness-boundary/docs/MEMORY_READINESS_BOUNDARY.md#memory-pressure-map"
)
MEMORY_READINESS_BOUNDARY_CONTRACT_PATH = (
    READINESS_BOUNDARY
    / "parts"
    / "memory-readiness-boundary"
    / "examples"
    / "memory_readiness_boundary_contract.example.json"
)
MEMORY_READINESS_BOUNDARY_CONTRACT_SCHEMA = "memory_readiness_boundary_contract.schema.json"
QUESTBOOK_PATH = ROOT / "QUESTBOOK.md"
QUESTBOOK_DOC = ROOT / "mechanics" / "writeback" / "docs" / "QUEST_EVIDENCE_WRITEBACK.md"
ORCHESTRATOR_MEMORY_ALIGNMENT_DOC = (
    ROOT / "mechanics" / "consumer-handoff" / "docs" / "ORCHESTRATOR_MEMORY_ALIGNMENT.md"
)
QUEST_CATALOG_PATH = GENERATED / "quests" / "quest_catalog.min.json"
QUEST_CATALOG_EXAMPLE_PATH = GENERATED / "quests" / "quest_catalog.min.example.json"
QUEST_DISPATCH_PATH = GENERATED / "quests" / "quest_dispatch.min.json"
QUEST_DISPATCH_EXAMPLE_PATH = GENERATED / "quests" / "quest_dispatch.min.example.json"
