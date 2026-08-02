from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

from validate_local_memo_port import schema_errors as local_port_schema_errors
from validate_memo import validator_for


ROOT = Path(__file__).resolve().parents[2]
MEMO = ROOT / "memo"
KIND_DIRS = {
    "anchor": "anchors",
    "state_capsule": "state-capsules",
    "episode": "episodes",
    "claim": "claims",
    "decision": "decisions",
    "pattern": "patterns",
    "bridge": "bridges",
    "audit_event": "audit-events",
}
ID_PREFIX_BY_KIND = {
    "anchor": "anchor",
    "state_capsule": "state",
    "episode": "episode",
    "claim": "claim",
    "decision": "decision",
    "pattern": "pattern",
    "bridge": "bridge",
    "audit_event": "audit",
}
LOCAL_KIND_TO_OBJECT_KIND = {
    "decision": "decision",
    "route": "decision",
    "constraint": "decision",
    "preference": "decision",
    "pattern": "pattern",
    "lesson": "pattern",
    "handoff": "bridge",
    "incident": "audit_event",
    "checkpoint": "audit_event",
}
SYMBOLIC_REF_PREFIXES = (
    "repo:",
    "aoa-kag://",
    "http://",
    "https://",
    "web:",
    "operator:",
    "state_capsule:",
    "audit_event:",
    "claim:",
    "bridge:",
    "episode:",
    "memory:",
    "candidate:",
    "receipt:",
    "export:",
    "landing-receipt:",
)
RFC3339_Z = re.compile(r"Z$")
SLUG_CHARS = re.compile(r"[^a-z0-9-]+")


class LandingError(ValueError):
    """Raised when an intake packet cannot land as reviewed corpus memory."""


JsonDict = dict[str, Any]


@dataclass(frozen=True)
class LandingInputs:
    port_path: Path
    export_path: Path
    port_payload: JsonDict
    export_payload: JsonDict
    candidate_paths: list[Path]
    candidate_payloads: list[JsonDict]
    receipt_paths: list[Path]
    receipt_payloads: list[JsonDict]


@dataclass(frozen=True)
class LandingPlan:
    repo: str
    slug: str
    object_id: str
    object_kind: str
    reviewed_at: str
    object_rel_path: str
    memo_rel_path: str
    copied_intake_rel_path: str
    receipt_rel_path: str
    export_payload: JsonDict
    object_payload: JsonDict
    memo_markdown: str
    receipt_payload: JsonDict


def write_json(path: Path, payload: JsonDict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rfc3339_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_rfc3339(value: str) -> datetime:
    normalized = RFC3339_Z.sub("+00:00", value)
    return datetime.fromisoformat(normalized).astimezone(timezone.utc)


def stamp_from_rfc3339(value: str) -> str:
    return parse_rfc3339(value).strftime("%Y%m%dT%H%M%SZ")


def date_from_rfc3339(value: str) -> str:
    return parse_rfc3339(value).date().isoformat()


def year_from_rfc3339(value: str) -> str:
    return str(parse_rfc3339(value).year)


def slugify(value: str) -> str:
    lowered = value.strip().lower().replace("_", "-").replace(".", "-")
    slug = SLUG_CHARS.sub("-", lowered).strip("-")
    if not slug:
        raise LandingError("slug cannot be empty")
    return slug


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def relative_to_output(output_root: Path, path: Path) -> str:
    return path.relative_to(output_root).as_posix()


def assert_under(base: Path, path: Path, label: str) -> Path:
    base_resolved = base.resolve()
    path_resolved = path.resolve()
    try:
        path_resolved.relative_to(base_resolved)
    except ValueError as exc:
        raise LandingError(f"{label} must stay under {base_resolved}") from exc
    return path_resolved


def packet_ref_path(port_path: Path, ref: str, label: str) -> Path:
    if ref.startswith(SYMBOLIC_REF_PREFIXES):
        raise LandingError(f"{label} must be a local packet ref, got {ref!r}")
    text = ref.split("#", 1)[0]
    if not text:
        raise LandingError(f"{label} must not be empty")
    path = Path(text)
    if path.is_absolute():
        raise LandingError(f"{label} must be relative to the memo port")
    resolved = (port_path / path).resolve()
    assert_under(port_path, resolved, label)
    if not resolved.is_file():
        raise LandingError(f"{label} points to missing packet {ref}")
    return resolved


def export_ref_path(port_path: Path, export_ref: str, export_dir: str) -> Path:
    path = Path(export_ref)
    if path.is_absolute():
        resolved = path.expanduser().resolve()
    else:
        parts = path.parts
        if parts and parts[0] == export_dir:
            resolved = (port_path / path).resolve()
        else:
            resolved = (port_path / export_dir / path).resolve()
    assert_under(port_path / export_dir, resolved, "export")
    if not resolved.is_file():
        raise LandingError(f"export points to missing packet {export_ref}")
    return resolved


def schema_errors(schema_name: str, payload: JsonDict, path: Path) -> list[str]:
    return local_port_schema_errors(schema_name, payload, path)


def object_schema_errors(payload: JsonDict, schema_name: str) -> list[str]:
    validator = validator_for(schema_name)
    return [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(payload), key=lambda err: list(err.absolute_path))
    ]


def support_schema_errors(payload: JsonDict, schema_name: str) -> list[str]:
    validator = validator_for(schema_name)
    return [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(payload), key=lambda err: list(err.absolute_path))
    ]
