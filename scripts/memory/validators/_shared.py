"""Shared paths, constants, schema helpers, and local-ref utilities for memo validators."""

from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timedelta
from functools import lru_cache
import os
from pathlib import Path
import re
import sys

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: jsonschema. Install it with: pip install jsonschema")
    raise SystemExit(2) from exc

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: PyYAML. Install it with: pip install PyYAML")
    raise SystemExit(2) from exc

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



def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def load_yaml(path: Path) -> object:
    return yaml.safe_load(load_text(path))

def format_schema_path(path_parts: list[object]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        else:
            if parts:
                parts.append(f".{part}")
            else:
                parts.append(str(part))
    return "".join(parts)

def is_rfc3339_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def is_rfc3339_date(year: int, month: int, day: int) -> bool:
    month_lengths = [
        31,
        29 if is_rfc3339_leap_year(year) else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    return 1 <= month <= 12 and 1 <= day <= month_lengths[month - 1]

def is_rfc3339_leap_second(
    match: re.Match[str], year: int, month: int, day: int, hour: int, minute: int
) -> bool:
    if match["zone"] in ("Z", "z"):
        return hour == 23 and minute == 59 and (year, month, day) in RFC3339_UTC_LEAP_SECOND_DATES
    if year == 0:
        return False
    offset_minutes = int(match["offset_hour"]) * 60 + int(match["offset_minute"])
    if match["offset_sign"] == "-":
        offset_minutes = -offset_minutes
    try:
        local_second = datetime(year, month, day, hour, minute, 59)
        utc_second = local_second - timedelta(minutes=offset_minutes)
    except (OverflowError, ValueError):
        return False
    return (
        utc_second.hour == 23
        and utc_second.minute == 59
        and (utc_second.year, utc_second.month, utc_second.day) in RFC3339_UTC_LEAP_SECOND_DATES
    )

@FORMAT_CHECKER.checks("date-time")
def is_rfc3339_datetime(value: object) -> bool:
    if not isinstance(value, str):
        return True
    match = RFC3339_DATETIME.fullmatch(value)
    if not match:
        return False
    year = int(match["year"])
    month = int(match["month"])
    day = int(match["day"])
    if not is_rfc3339_date(year, month, day):
        return False
    hour = int(match["hour"])
    minute = int(match["minute"])
    second = int(match["second"])
    if hour > 23 or minute > 59 or second > 60:
        return False
    if second == 60 and not is_rfc3339_leap_second(match, year, month, day, hour, minute):
        return False
    if match["offset_hour"] is not None:
        if int(match["offset_hour"]) > 23 or int(match["offset_minute"]) > 59:
            return False
    return True

def markdown_anchor(text: str) -> str:
    anchor = text.strip().lower()
    anchor = re.sub(r"[^\w\s-]", "", anchor)
    anchor = re.sub(r"\s+", "-", anchor)
    anchor = re.sub(r"-+", "-", anchor)
    return anchor.strip("-")

@lru_cache(maxsize=None)
def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = MARKDOWN_HEADING.match(line)
        if not match:
            continue
        base = markdown_anchor(match.group(2))
        if not base:
            continue
        suffix = seen.get(base, 0)
        seen[base] = suffix + 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors

def local_ref_error(ref_value: object, label: str) -> str | None:
    if not isinstance(ref_value, str) or not ref_value:
        return None
    if ref_value.startswith(("http://", "https://", "repo:")):
        return None
    if SYMBOLIC_REF.match(ref_value) and not WINDOWS_ABSOLUTE_PATH.match(ref_value):
        return None

    path_text, _, anchor = ref_value.partition("#")
    target = ROOT / path_text

    if not target.exists():
        return f"{label}: referenced path does not exist: {ref_value}"
    if anchor and target.suffix.lower() == ".md" and anchor not in markdown_anchors(target):
        return f"{label}: referenced markdown anchor does not exist: {ref_value}"
    return None

def append_ref_errors(errors: list[str], ref_checks: list[tuple[str, object]]) -> None:
    errors.extend(filter(None, (local_ref_error(value, label) for label, value in ref_checks)))


LINEAGE_REF_CHAIN = ("cluster_ref", "candidate_ref", "source_ref", "object_ref")


def append_lineage_chain_errors(errors: list[str], lineage_refs: object) -> None:
    if not isinstance(lineage_refs, dict):
        return

    for index, field_name in enumerate(LINEAGE_REF_CHAIN):
        value = lineage_refs.get(field_name)
        if value is None:
            continue
        for required_name in LINEAGE_REF_CHAIN[:index]:
            if lineage_refs.get(required_name) is None:
                errors.append(
                    f"lineage_refs.{field_name} requires lineage_refs.{required_name} when later chain links are present"
                )
                break

@lru_cache(maxsize=None)
def schema_registry() -> Registry:
    resources: list[tuple[str, Resource]] = []
    for path in iter_schema_paths():
        schema = load_json(path)
        schema_id = schema.get("$id")
        if isinstance(schema_id, str):
            resources.append((schema_id, Resource.from_contents(schema)))
    return Registry().with_resources(resources)

def iter_schema_paths() -> tuple[Path, ...]:
    paths: list[Path] = []
    for schema_dir in (*root_schema_dirs(), *MECHANIC_SCHEMA_DIRS):
        paths.extend(sorted(schema_dir.glob("*.json")))
    return tuple(paths)

def root_schema_dirs() -> tuple[Path, ...]:
    return (SCHEMAS, *tuple(sorted(path for path in SCHEMAS.iterdir() if path.is_dir())))

def root_example_dirs() -> tuple[Path, ...]:
    return (EXAMPLES, *tuple(sorted(path for path in EXAMPLES.iterdir() if path.is_dir())))

def _find_unique_by_name(name: str, dirs: tuple[Path, ...], label: str) -> Path:
    primary = dirs[0] / name
    if primary.is_file():
        return primary
    matches = [directory / name for directory in dirs[1:] if (directory / name).is_file()]
    if not matches:
        raise FileNotFoundError(f"missing {label}: {name}")
    if len(matches) > 1:
        rendered = ", ".join(
            path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix()
            for path in matches
        )
        raise ValueError(f"ambiguous {label} {name}: {rendered}")
    return matches[0]

def schema_path_for(schema_ref: str) -> Path:
    if "/" in schema_ref:
        return ROOT / schema_ref
    return _find_unique_by_name(schema_ref, (*root_schema_dirs(), *MECHANIC_SCHEMA_DIRS), "schema")

def example_path_for(example_ref: str) -> Path:
    if "/" in example_ref:
        return ROOT / example_ref
    return _find_unique_by_name(example_ref, (*root_example_dirs(), *MECHANIC_EXAMPLE_DIRS), "example")

def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(schema_path_for(schema_name))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FORMAT_CHECKER, registry=schema_registry())

def validate_example(validator: Draft202012Validator, example_name: str) -> None:
    data = load_json(example_path_for(example_name))
    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]
    lineage_refs = data.get("lineage_refs")
    if not isinstance(lineage_refs, dict):
        lineage_refs = {}
    lineage_context = data.get("lineage_context")
    if not isinstance(lineage_context, dict):
        lineage_context = {}

    ref_checks = [
        ("payload_ref", data.get("payload_ref")),
        ("bridges.route_capsule_ref", data.get("bridges", {}).get("route_capsule_ref")),
        ("inspect_surface", data.get("inspect_surface")),
        ("capsule_surface", data.get("capsule_surface")),
        ("expand_surface", data.get("expand_surface")),
        ("lineage_refs.cluster_ref", lineage_refs.get("cluster_ref")),
        ("lineage_refs.candidate_ref", lineage_refs.get("candidate_ref")),
        ("lineage_refs.source_ref", lineage_refs.get("source_ref")),
        ("lineage_refs.object_ref", lineage_refs.get("object_ref")),
        ("lineage_context.merged_into", lineage_context.get("merged_into")),
    ]
    for list_name in (
        "evidence_pack_refs",
        "contradiction_pack_refs",
        "witness_refs",
        "memory_delta_refs",
        "canon_delta_refs",
    ):
        values = data.get(list_name)
        if not isinstance(values, list):
            continue
        for index, value in enumerate(values):
            ref_checks.append((f"{list_name}[{index}]", value))
    return_pack = data.get("return_pack")
    if isinstance(return_pack, dict):
        for list_name in ("anchor_refs", "reentry_refs"):
            values = return_pack.get(list_name)
            if not isinstance(values, list):
                continue
            for index, value in enumerate(values):
                ref_checks.append((f"return_pack.{list_name}[{index}]", value))
    errors.extend(filter(None, (local_ref_error(value, label) for label, value in ref_checks)))
    append_lineage_chain_errors(errors, lineage_refs)

    if errors:
        print(f"[FAIL] {example_name}")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print(f"[OK]   {example_name}")
