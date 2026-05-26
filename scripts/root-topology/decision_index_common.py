from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
DECISIONS_DIR = Path("docs/decisions")
INDEXES_DIR = DECISIONS_DIR / "indexes"
INDEX_CONTRACT_PATH = INDEXES_DIR / "index_contract.yaml"
DECISION_ID_RE = re.compile(r"^- Decision ID: (AOA-MEM-D-(\d{4}))$", re.MULTILINE)
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")

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
    INDEXES_DIR / "alias-map.md",
    INDEXES_DIR / "alias-map.min.json",
)


@dataclass(frozen=True)
class DecisionRecord:
    decision_id: str
    number: int
    title: str
    path: Path
    date: str
    surface_classes: tuple[str, ...]
    mechanic_parents: tuple[str, ...]
    guard_families: tuple[str, ...]
    memory_object_classes: tuple[str, ...]
    posture: str

    @property
    def repo_path(self) -> str:
        return self.path.as_posix()

    @property
    def index_link(self) -> str:
        return f"../{self.path.name}"

    @property
    def planned_numbered_path(self) -> str:
        name = self.path.name
        date_match = DATE_RE.match(name)
        slug = name[11:] if date_match else name
        return f"{DECISIONS_DIR.as_posix()}/{self.number:04d}-{slug}"


def split_metadata_value(value: str) -> tuple[str, ...]:
    value = value.strip()
    if not value or value == "none":
        return ()
    return tuple(item.strip() for item in value.split(",") if item.strip())


def parse_title(text: str, *, path: Path) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError(f"{path.as_posix()} is missing a level-one title")


def parse_decision_id(text: str, *, path: Path) -> tuple[str, int]:
    match = DECISION_ID_RE.search(text)
    if not match:
        raise ValueError(f"{path.as_posix()} is missing '- Decision ID: AOA-MEM-D-####'")
    return match.group(1), int(match.group(2))


def parse_date(path: Path) -> str:
    match = DATE_RE.match(path.name)
    return match.group(1) if match else "undated"


def parse_index_metadata(text: str, *, path: Path) -> dict[str, str]:
    marker = "\n## Index Metadata\n"
    if marker not in text:
        raise ValueError(f"{path.as_posix()} is missing ## Index Metadata")
    section = text.split(marker, 1)[1]
    next_heading = section.find("\n## ")
    if next_heading != -1:
        section = section[:next_heading]
    metadata: dict[str, str] = {}
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line.startswith("- ") or ":" not in line:
            continue
        key, value = line[2:].split(":", 1)
        metadata[key.strip().lower()] = value.strip()
    required = {
        "surface classes",
        "mechanic parents",
        "guard families",
        "memory object classes",
        "posture",
    }
    missing = sorted(required - set(metadata))
    if missing:
        raise ValueError(
            f"{path.as_posix()} index metadata is missing: {', '.join(missing)}"
        )
    return metadata


def validate_values(
    values: Iterable[str],
    *,
    allowed: Sequence[str],
    field: str,
    path: Path,
) -> list[tuple[str, str]]:
    allowed_set = set(allowed)
    issues: list[tuple[str, str]] = []
    for value in values:
        if value not in allowed_set:
            issues.append((path.as_posix(), f"{field} contains unknown value: {value}"))
    return issues


def load_decision_record(path: Path, *, repo_root: Path) -> DecisionRecord:
    text = path.read_text(encoding="utf-8")
    relative_path = path.relative_to(repo_root)
    decision_id, number = parse_decision_id(text, path=relative_path)
    title = parse_title(text, path=relative_path)
    metadata = parse_index_metadata(text, path=relative_path)
    return DecisionRecord(
        decision_id=decision_id,
        number=number,
        title=title,
        path=relative_path,
        date=parse_date(relative_path),
        surface_classes=split_metadata_value(metadata["surface classes"]),
        mechanic_parents=split_metadata_value(metadata["mechanic parents"]),
        guard_families=split_metadata_value(metadata["guard families"]),
        memory_object_classes=split_metadata_value(metadata["memory object classes"]),
        posture=metadata["posture"].strip(),
    )


def collect_decision_records(repo_root: Path) -> tuple[list[DecisionRecord], list[tuple[str, str]]]:
    records: list[DecisionRecord] = []
    issues: list[tuple[str, str]] = []
    decisions_root = repo_root / DECISIONS_DIR
    if not decisions_root.is_dir():
        return records, [(DECISIONS_DIR.as_posix(), "decision directory is missing")]

    for path in sorted(
        item
        for item in decisions_root.glob("*.md")
        if item.name not in {"AGENTS.md", "README.md", "TEMPLATE.md"}
    ):
        try:
            record = load_decision_record(path, repo_root=repo_root)
        except ValueError as exc:
            issues.append((path.relative_to(repo_root).as_posix(), str(exc)))
            continue
        issues.extend(
            validate_values(
                record.surface_classes,
                allowed=SURFACE_CLASS_ORDER,
                field="surface classes",
                path=record.path,
            )
        )
        issues.extend(
            validate_values(
                record.mechanic_parents,
                allowed=MECHANIC_PARENT_ORDER,
                field="mechanic parents",
                path=record.path,
            )
        )
        issues.extend(
            validate_values(
                record.guard_families,
                allowed=GUARD_FAMILY_ORDER,
                field="guard families",
                path=record.path,
            )
        )
        issues.extend(
            validate_values(
                record.memory_object_classes,
                allowed=MEMORY_OBJECT_CLASS_ORDER,
                field="memory object classes",
                path=record.path,
            )
        )
        records.append(record)

    ids = [record.decision_id for record in records]
    if len(ids) != len(set(ids)):
        issues.append((DECISIONS_DIR.as_posix(), "decision IDs must be unique"))
    numbers = sorted(record.number for record in records)
    if numbers and numbers != list(range(numbers[0], numbers[-1] + 1)):
        issues.append((DECISIONS_DIR.as_posix(), "decision ID numbers must be contiguous"))
    return sorted(records, key=lambda record: record.number), issues


def load_index_contract(repo_root: Path) -> tuple[dict[str, object] | None, list[tuple[str, str]]]:
    path = repo_root / INDEX_CONTRACT_PATH
    if not path.is_file():
        return None, [(INDEX_CONTRACT_PATH.as_posix(), "decision index contract is missing")]
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return None, [(INDEX_CONTRACT_PATH.as_posix(), "decision index contract must be a mapping")]
    return payload, []


def ordered_values(values: Iterable[str], preferred_order: Sequence[str]) -> list[str]:
    seen = set(values)
    ordered = [value for value in preferred_order if value in seen]
    ordered.extend(sorted(seen - set(ordered)))
    return ordered


def render_generated_notice() -> str:
    return "<!-- Generated by scripts/root-topology/build_decision_indexes.py; do not edit by hand. -->\n\n"


def display_title(record: DecisionRecord) -> str:
    if record.title.startswith(record.decision_id):
        return record.title
    return f"{record.decision_id} {record.title}"


def bullet_line(record: DecisionRecord) -> str:
    return f"- [{display_title(record)}]({record.index_link}) (`{record.repo_path}`)"


def render_indexes_readme() -> str:
    return (
        "# Decision Lookup Indexes\n\n"
        + render_generated_notice()
        + "These files are generated read models from decision-note `Decision ID` and `Index Metadata`.\n"
        + "Decision notes own rationale; these indexes only make lookup cheaper for agents.\n\n"
        + "## Indexes\n\n"
        + "- [By canonical ID and number](by-number.md)\n"
        + "- [By date](by-date.md)\n"
        + "- [By surface class](by-surface.md)\n"
        + "- [By mechanic parent](by-mechanic.md)\n"
        + "- [By validation or guard family](by-guard.md)\n"
        + "- [By memory-object class](by-memory-object-class.md)\n"
        + "- [Alias map](alias-map.md)\n"
        + "- [Machine alias map](alias-map.min.json)\n"
    )


def render_by_number(records: Sequence[DecisionRecord]) -> str:
    lines = [
        "# Decisions By Canonical ID And Number",
        "",
        render_generated_notice().rstrip(),
        "",
        "| ID | Date | Decision | Current path | Planned numbered path | Surface classes | Mechanic parents | Guard families | Memory object classes | Posture |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in records:
        lines.append(
            "| {id} | {date} | [{title}]({link}) | `{path}` | `{planned}` | {surfaces} | {parents} | {guards} | {classes} | {posture} |".format(
                id=record.decision_id,
                date=record.date,
                title=display_title(record),
                link=record.index_link,
                path=record.repo_path,
                planned=record.planned_numbered_path,
                surfaces=", ".join(record.surface_classes) or "none",
                parents=", ".join(record.mechanic_parents) or "none",
                guards=", ".join(record.guard_families) or "none",
                classes=", ".join(record.memory_object_classes) or "none",
                posture=record.posture,
            )
        )
    return "\n".join(lines) + "\n"


def render_grouped_index(
    *,
    title: str,
    records: Sequence[DecisionRecord],
    attribute: str,
    preferred_order: Sequence[str],
) -> str:
    values: list[str] = []
    for record in records:
        values.extend(getattr(record, attribute))
    lines = ["# " + title, "", render_generated_notice().rstrip(), ""]
    for value in ordered_values(values, preferred_order):
        lines.extend([f"## {value}", ""])
        for record in records:
            if value in getattr(record, attribute):
                lines.append(bullet_line(record))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_by_date(records: Sequence[DecisionRecord]) -> str:
    lines = ["# Decisions By Date", "", render_generated_notice().rstrip(), ""]
    for date in ordered_values((record.date for record in records), ()):
        lines.extend([f"## {date}", ""])
        for record in records:
            if record.date == date:
                lines.append(bullet_line(record))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def alias_entries(records: Sequence[DecisionRecord]) -> list[dict[str, object]]:
    return [
        {
            "decision_id": record.decision_id,
            "date": record.date,
            "old_path": record.repo_path,
            "current_path": record.repo_path,
            "planned_numbered_path": record.planned_numbered_path,
            "canonical_path_status": "dual_addressing_not_renamed",
        }
        for record in records
    ]


def render_alias_map(records: Sequence[DecisionRecord]) -> str:
    lines = [
        "# Decision Alias Map",
        "",
        render_generated_notice().rstrip(),
        "",
        "The current date-named paths remain live during dual-addressing. The planned numbered paths are reserved handles for a later rename slice, not active files yet.",
        "",
        "| Decision ID | Old/current path | Planned numbered path | Status |",
        "| --- | --- | --- | --- |",
    ]
    for entry in alias_entries(records):
        lines.append(
            "| {decision_id} | `{current_path}` | `{planned_numbered_path}` | `{canonical_path_status}` |".format(
                **entry
            )
        )
    return "\n".join(lines) + "\n"


def render_alias_json(records: Sequence[DecisionRecord]) -> str:
    payload = {
        "schema_version": "aoa_memo_decision_alias_map_v1",
        "generated_by": "scripts/root-topology/build_decision_indexes.py",
        "authority": "decision notes own rationale; this alias map only bridges old date paths to canonical IDs",
        "entries": alias_entries(records),
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def render_index_files(records: Sequence[DecisionRecord]) -> dict[Path, str]:
    return {
        INDEXES_DIR / "README.md": render_indexes_readme(),
        INDEXES_DIR / "by-number.md": render_by_number(records),
        INDEXES_DIR / "by-date.md": render_by_date(records),
        INDEXES_DIR / "by-surface.md": render_grouped_index(
            title="Decisions By Surface Class",
            records=records,
            attribute="surface_classes",
            preferred_order=SURFACE_CLASS_ORDER,
        ),
        INDEXES_DIR / "by-mechanic.md": render_grouped_index(
            title="Decisions By Mechanic Parent",
            records=records,
            attribute="mechanic_parents",
            preferred_order=MECHANIC_PARENT_ORDER,
        ),
        INDEXES_DIR / "by-guard.md": render_grouped_index(
            title="Decisions By Validation Or Guard Family",
            records=records,
            attribute="guard_families",
            preferred_order=GUARD_FAMILY_ORDER,
        ),
        INDEXES_DIR / "by-memory-object-class.md": render_grouped_index(
            title="Decisions By Memory-Object Class",
            records=records,
            attribute="memory_object_classes",
            preferred_order=MEMORY_OBJECT_CLASS_ORDER,
        ),
        INDEXES_DIR / "alias-map.md": render_alias_map(records),
        INDEXES_DIR / "alias-map.min.json": render_alias_json(records),
    }


def validate_decision_index_surfaces(repo_root: Path) -> list[tuple[str, str]]:
    records, issues = collect_decision_records(repo_root)
    contract, contract_issues = load_index_contract(repo_root)
    issues.extend(contract_issues)
    if contract is not None:
        expected = [path.as_posix() for path in GENERATED_INDEX_PATHS]
        if contract.get("generated_indexes") != expected:
            issues.append(
                (
                    INDEX_CONTRACT_PATH.as_posix(),
                    "generated_indexes must match the decision index read-model set",
                )
            )
        fields = contract.get("fields")
        if not isinstance(fields, dict) or "decision_id" not in fields:
            issues.append((INDEX_CONTRACT_PATH.as_posix(), "fields must name decision_id"))
    if issues:
        return issues

    rendered = render_index_files(records)
    for relative_path, expected_text in rendered.items():
        path = repo_root / relative_path
        if not path.is_file():
            issues.append((relative_path.as_posix(), "generated decision index is missing"))
            continue
        actual_text = path.read_text(encoding="utf-8")
        if actual_text != expected_text:
            issues.append(
                (
                    relative_path.as_posix(),
                    "generated decision index is stale; run python scripts/root-topology/build_decision_indexes.py",
                )
            )
    return issues
