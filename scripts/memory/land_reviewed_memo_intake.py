#!/usr/bin/env python3
"""Land a reviewed local memo export as an aoa-memo corpus object bundle."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil
import sys
from typing import Any

from local_memo_port_common import load_json, load_port, resolve_port_path
from validate_memo import validator_for
from validate_local_memo_port import (
    schema_errors as local_port_schema_errors,
    validate_candidate_semantics,
)


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


def validate_inputs(
    *,
    port_path: Path,
    export_path: Path,
    port_payload: JsonDict,
    export_payload: JsonDict,
    candidate_paths: list[Path],
    candidate_payloads: list[JsonDict],
    receipt_paths: list[Path],
    receipt_payloads: list[JsonDict],
) -> None:
    errors: list[str] = []
    errors.extend(schema_errors("local_memo_export.schema.json", export_payload, export_path))
    repo = str(port_payload.get("repo") or "")
    if export_payload.get("repo") != repo:
        errors.append(f"{export_path}: repo must match PORT.yaml repo")
    if export_payload.get("allowed_result") != "reviewed_write":
        errors.append(f"{export_path}: allowed_result must be 'reviewed_write' for corpus landing")
    if not receipt_payloads:
        errors.append(f"{export_path}: reviewed_write landing requires at least one receipt_ref")

    for candidate_path, candidate in zip(candidate_paths, candidate_payloads, strict=True):
        errors.extend(schema_errors("local_memo_candidate.schema.json", candidate, candidate_path))
        if candidate.get("repo") != repo:
            errors.append(f"{candidate_path}: repo must match PORT.yaml repo")
        if candidate.get("route") != "reviewed_intake":
            errors.append(f"{candidate_path}: route must be reviewed_intake for corpus landing")
        if candidate.get("review_state") in {"rejected", "superseded", "archived"}:
            errors.append(f"{candidate_path}: review_state blocks corpus landing")
        if candidate.get("source_trust") in {"untrusted", "unknown"}:
            errors.append(f"{candidate_path}: source_trust {candidate.get('source_trust')!r} blocks corpus landing")
        validate_candidate_semantics(errors, candidate_path, candidate)

    for receipt_path, receipt in zip(receipt_paths, receipt_payloads, strict=True):
        errors.extend(schema_errors("local_memo_receipt.schema.json", receipt, receipt_path))
        if receipt.get("repo") != repo:
            errors.append(f"{receipt_path}: repo must match PORT.yaml repo")
        if receipt.get("route") != "reviewed_intake":
            errors.append(f"{receipt_path}: route must be reviewed_intake for corpus landing")
        if receipt.get("result") not in {"validated", "forwarded", "landed"}:
            errors.append(f"{receipt_path}: result must be validated, forwarded, or landed before corpus landing")
        if receipt.get("errors"):
            errors.append(f"{receipt_path}: receipt with errors cannot support corpus landing")

    if errors:
        rendered = "\n".join(f"- {error}" for error in errors)
        raise LandingError(f"reviewed intake landing input validation failed:\n{rendered}")


def load_landing_inputs(port: str | Path, export_ref: str | Path) -> LandingInputs:
    port_path = resolve_port_path(port)
    port_payload = load_port(port_path)
    export_dir = str(port_payload.get("export_dir", "exports"))
    export_path = export_ref_path(port_path, str(export_ref), export_dir)
    export_payload = load_json(export_path)
    if not isinstance(export_payload, dict):
        raise LandingError(f"{export_path}: export packet must be a JSON object")

    candidate_refs = export_payload.get("candidate_refs", [])
    receipt_refs = export_payload.get("receipt_refs", [])
    if not isinstance(candidate_refs, list):
        candidate_refs = []
    if not isinstance(receipt_refs, list):
        receipt_refs = []
    candidate_paths = [
        packet_ref_path(port_path, ref, "candidate_ref")
        for ref in candidate_refs
        if isinstance(ref, str)
    ]
    receipt_paths = [
        packet_ref_path(port_path, ref, "receipt_ref")
        for ref in receipt_refs
        if isinstance(ref, str)
    ]
    candidate_payloads = [load_json(path) for path in candidate_paths]
    receipt_payloads = [load_json(path) for path in receipt_paths]
    if not all(isinstance(payload, dict) for payload in candidate_payloads + receipt_payloads):
        raise LandingError("candidate and receipt packets must be JSON objects")

    validate_inputs(
        port_path=port_path,
        export_path=export_path,
        port_payload=port_payload,
        export_payload=export_payload,
        candidate_paths=candidate_paths,
        candidate_payloads=candidate_payloads,
        receipt_paths=receipt_paths,
        receipt_payloads=receipt_payloads,
    )
    return LandingInputs(
        port_path=port_path,
        export_path=export_path,
        port_payload=port_payload,
        export_payload=export_payload,
        candidate_paths=candidate_paths,
        candidate_payloads=candidate_payloads,
        receipt_paths=receipt_paths,
        receipt_payloads=receipt_payloads,
    )


def normalize_origin_ref(repo: str, ref: str) -> str:
    if ref.startswith(SYMBOLIC_REF_PREFIXES):
        return ref
    text = ref.split("#", 1)[0]
    fragment = f"#{ref.split('#', 1)[1]}" if "#" in ref else ""
    if text.startswith("memo/"):
        return f"repo:{repo}/{text}{fragment}"
    return f"repo:{repo}/{text}{fragment}"


def normalize_packet_ref(repo: str, ref: str) -> str:
    if ref.startswith(SYMBOLIC_REF_PREFIXES):
        return ref
    text = ref.split("#", 1)[0]
    fragment = f"#{ref.split('#', 1)[1]}" if "#" in ref else ""
    return f"repo:{repo}/memo/{text}{fragment}"


def infer_object_kind(candidates: list[JsonDict]) -> str:
    kinds = {str(candidate.get("kind") or "") for candidate in candidates}
    mapped = {LOCAL_KIND_TO_OBJECT_KIND[kind] for kind in kinds if kind in LOCAL_KIND_TO_OBJECT_KIND}
    if len(mapped) == 1:
        return next(iter(mapped))
    raise LandingError("cannot infer object kind; pass --object-kind")


def title_from_candidates(candidates: list[JsonDict]) -> str:
    claim = str(candidates[0].get("claim") or "Reviewed memo intake").strip()
    first_sentence = claim.split(".", 1)[0].strip()
    if len(first_sentence) > 96:
        first_sentence = first_sentence[:93].rstrip() + "..."
    return first_sentence[0].upper() + first_sentence[1:] if first_sentence else "Reviewed memo intake"


def summary_from_candidates(candidates: list[JsonDict], repo: str) -> str:
    if len(candidates) == 1:
        return str(candidates[0]["claim"])
    claims = "; ".join(str(candidate["claim"]).rstrip(".") for candidate in candidates)
    return f"Reviewed intake from {repo} consolidates {len(candidates)} local memory candidates: {claims}."


def build_memo_markdown(plan: LandingPlan, source_refs: list[str], candidate_claims: list[str]) -> str:
    claim_lines = "\n".join(f"- {claim}" for claim in candidate_claims)
    source_lines = "\n".join(f"- `{ref}`" for ref in source_refs[:8])
    return (
        f"# {plan.object_payload['title']}\n"
        "\n"
        "## Memory\n"
        f"{plan.object_payload['summary']}\n"
        "\n"
        "## Source Route\n"
        f"- Reviewed intake: `{plan.copied_intake_rel_path}`\n"
        f"{source_lines}\n"
        "\n"
        "## Review Posture\n"
        f"This bundle landed from `{plan.repo}` through the reviewed intake route. "
        "The local candidate packets remain source evidence; this object is the "
        "reviewed `aoa-memo` corpus memory.\n"
        "\n"
        "## Candidate Claims\n"
        f"{claim_lines}\n"
        "\n"
        "## Next Routes\n"
        "- Validate with `python scripts/memory/validate_memo_corpus.py`.\n"
        "- Refresh object read models with `python scripts/memory/generate_memory_object_surfaces.py`.\n"
        "- Keep durable edits in `memo/objects/`; keep origin packet history in the source repo memo port.\n"
    )


def build_landing_plan(
    inputs: LandingInputs,
    *,
    output_root: Path = ROOT,
    object_kind: str | None = None,
    slug: str | None = None,
    title: str | None = None,
    summary: str | None = None,
    object_id: str | None = None,
    reviewed_at: str | None = None,
    reviewed_by: str = "aoa-memo:reviewed-intake-landing",
    current_recall_status: str = "allowed",
    temperature: str = "cool",
    confidence: float = 0.85,
) -> LandingPlan:
    output_root = output_root.resolve()
    reviewed_at = reviewed_at or rfc3339_now()
    stamp = stamp_from_rfc3339(reviewed_at)
    repo = str(inputs.port_payload["repo"])
    repo_slug = slugify(repo)
    export_slug = str(inputs.export_payload["id"]).split(":")[-1]
    slug_value = slugify(slug or export_slug)
    object_kind = object_kind or infer_object_kind(inputs.candidate_payloads)
    if object_kind not in KIND_DIRS:
        raise LandingError(f"unsupported memory object kind {object_kind!r}")
    year = year_from_rfc3339(reviewed_at)
    object_id = object_id or f"memo.{ID_PREFIX_BY_KIND[object_kind]}.{date_from_rfc3339(reviewed_at)}.{slug_value}"

    copied_intake_rel = f"memo/intake/reviewed/{repo_slug}.{inputs.export_path.name}"
    object_rel = f"memo/objects/{KIND_DIRS[object_kind]}/{year}/{slug_value}/object.json"
    memo_rel = f"memo/objects/{KIND_DIRS[object_kind]}/{year}/{slug_value}/MEMO.md"
    receipt_rel = f"memo/intake/receipts/{stamp}.{repo_slug}.{slug_value}.landing-receipt.json"

    candidate_packet_refs = [
        normalize_packet_ref(repo, ref) for ref in inputs.export_payload["candidate_refs"]
    ]
    receipt_packet_refs = [
        normalize_packet_ref(repo, ref) for ref in inputs.export_payload.get("receipt_refs", [])
    ]
    origin_refs = [
        *(normalize_origin_ref(repo, ref) for ref in inputs.export_payload.get("source_refs", [])),
        *(normalize_origin_ref(repo, ref) for ref in inputs.export_payload.get("evidence_refs", [])),
    ]
    for candidate in inputs.candidate_payloads:
        origin_refs.extend(normalize_origin_ref(repo, ref) for ref in candidate.get("source_refs", []))
        origin_refs.extend(normalize_origin_ref(repo, ref) for ref in candidate.get("evidence_refs", []))
    source_refs = dedupe([copied_intake_rel, *candidate_packet_refs, *receipt_packet_refs, *origin_refs])

    candidate_claims = [str(candidate["claim"]) for candidate in inputs.candidate_payloads]
    candidate_families = [str(candidate.get("family")) for candidate in inputs.candidate_payloads if candidate.get("family")]
    candidate_kinds = [str(candidate.get("kind")) for candidate in inputs.candidate_payloads if candidate.get("kind")]
    risks = [
        str(risk)
        for candidate in inputs.candidate_payloads
        for risk in candidate.get("risk", [])
        if isinstance(risk, str)
    ]

    object_payload: JsonDict = {
        "id": object_id,
        "kind": object_kind,
        "title": title or title_from_candidates(inputs.candidate_payloads),
        "summary": summary or summary_from_candidates(inputs.candidate_payloads, repo),
        "scope": dedupe([f"repo:{repo}", "repo:aoa-memo", "workspace:OS-Abyss"]),
        "owner_refs": dedupe([f"repo:{repo}", "repo:aoa-memo"]),
        "payload_ref": copied_intake_rel,
        "tags": dedupe(["reviewed-intake", "local-memo-port", *candidate_families, *candidate_kinds, *risks]),
        "time": {
            "created_at": reviewed_at,
            "observed_at": inputs.export_payload["created_at"],
            "valid_from": reviewed_at,
            "valid_to": None,
        },
        "provenance": {
            "source_refs": source_refs,
            "episode_refs": [],
            "provenance_thread_id": f"prov.{repo_slug}.{slug_value}.{date_from_rfc3339(reviewed_at)}",
        },
        "trust": {
            "temperature": temperature,
            "confidence": confidence,
            "confidence_note": "Landed from reviewed local memo export after schema, guardrail, packet, and receipt checks.",
            "authority_kind": "human_reviewed",
            "authority": f"reviewed intake landing from {repo}",
            "freshness": 1.0,
            "freshness_note": "Fresh at landing time; future recall depends on lifecycle review.",
            "salience": 0.8,
            "salience_note": "Imported because the origin port requested durable reviewed memory.",
        },
        "lifecycle": {
            "review_state": "confirmed",
            "supersedes": [],
            "superseded_by": None,
            "retention_class": "reviewed-intake",
            "promotion_state": "promoted",
            "current_recall": {
                "status": current_recall_status,
                "status_reason": "Landed through reviewed intake; use as reviewed recall, not proof or stronger owner truth.",
            },
        },
        "access": {
            "access_class": "public",
            "read_scopes": ["public"],
            "write_scopes": ["maintainer"],
            "promotion_scopes": ["maintainer", "human-review"],
        },
        "bridges": {
            "tos_refs": [],
            "skill_refs": [],
            "eval_refs": [],
            "kag_lift_status": "candidate",
            "route_capsule_ref": copied_intake_rel,
        },
    }

    object_errors = [
        *object_schema_errors(object_payload, "memory_object.schema.json"),
        *object_schema_errors(object_payload, f"{object_kind}.schema.json"),
    ]
    if object_errors:
        rendered = "\n".join(f"- {error}" for error in object_errors)
        raise LandingError(f"landing object validation failed:\n{rendered}")

    receipt_payload: JsonDict = {
        "schema": "aoa_memo_reviewed_intake_landing_receipt_v1",
        "id": f"landing-receipt:{repo}:{stamp}:{repo_slug}-{slug_value}",
        "repo": repo,
        "source_export_ref": normalize_packet_ref(repo, inputs.export_path.relative_to(inputs.port_path).as_posix()),
        "copied_intake_ref": copied_intake_rel,
        "candidate_refs": candidate_packet_refs,
        "receipt_refs": receipt_packet_refs,
        "object_ref": object_id,
        "object_path": object_rel,
        "result": "landed",
        "checks": [
            "export_schema",
            "allowed_result_reviewed_write",
            "candidate_schema",
            "candidate_guardrails",
            "receipt_schema",
            "receipt_errors_empty",
            "memory_object_schema",
        ],
        "errors": [],
        "landed_at": reviewed_at,
        "landed_by": reviewed_by,
    }
    receipt_errors = support_schema_errors(receipt_payload, "reviewed_intake_landing_receipt.schema.json")
    if receipt_errors:
        rendered = "\n".join(f"- {error}" for error in receipt_errors)
        raise LandingError(f"landing receipt validation failed:\n{rendered}")

    plan_stub = LandingPlan(
        repo=repo,
        slug=slug_value,
        object_id=object_id,
        object_kind=object_kind,
        reviewed_at=reviewed_at,
        object_rel_path=object_rel,
        memo_rel_path=memo_rel,
        copied_intake_rel_path=copied_intake_rel,
        receipt_rel_path=receipt_rel,
        export_payload=inputs.export_payload,
        object_payload=object_payload,
        memo_markdown="",
        receipt_payload=receipt_payload,
    )
    memo_markdown = build_memo_markdown(plan_stub, source_refs, candidate_claims)
    return LandingPlan(
        **{
            **plan_stub.__dict__,
            "memo_markdown": memo_markdown,
        }
    )


def write_landing_plan(plan: LandingPlan, *, output_root: Path = ROOT, replace: bool = False) -> None:
    output_root = output_root.resolve()
    targets = [
        output_root / plan.copied_intake_rel_path,
        output_root / plan.object_rel_path,
        output_root / plan.memo_rel_path,
        output_root / plan.receipt_rel_path,
    ]
    existing = [path for path in targets if path.exists()]
    if existing and not replace:
        rendered = ", ".join(relative_to_output(output_root, path) for path in existing)
        raise LandingError(f"landing target already exists: {rendered}")

    for path in targets:
        path.parent.mkdir(parents=True, exist_ok=True)

    write_json(output_root / plan.copied_intake_rel_path, plan.export_payload)
    write_json(output_root / plan.object_rel_path, plan.object_payload)
    (output_root / plan.memo_rel_path).write_text(plan.memo_markdown, encoding="utf-8")
    write_json(output_root / plan.receipt_rel_path, plan.receipt_payload)


def plan_summary(plan: LandingPlan) -> JsonDict:
    return {
        "repo": plan.repo,
        "object_id": plan.object_id,
        "object_kind": plan.object_kind,
        "object_path": plan.object_rel_path,
        "memo_path": plan.memo_rel_path,
        "copied_intake_ref": plan.copied_intake_rel_path,
        "receipt_path": plan.receipt_rel_path,
        "reviewed_at": plan.reviewed_at,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Land a reviewed local memo export into memo/objects.")
    parser.add_argument("--port", required=True, help="Path to the origin repository memo port.")
    parser.add_argument("--export", required=True, help="Export packet path relative to the memo port export dir.")
    parser.add_argument("--output-root", default=str(ROOT), help="Repository root to write into; defaults to aoa-memo.")
    parser.add_argument("--object-kind", choices=sorted(KIND_DIRS), help="Memory object kind to create.")
    parser.add_argument("--slug", help="Object slug; defaults to export id slug.")
    parser.add_argument("--title", help="Object title; defaults to first candidate claim.")
    parser.add_argument("--summary", help="Object summary; defaults to candidate claim summary.")
    parser.add_argument("--object-id", help="Object id; defaults to memo.<kind>.<date>.<slug>.")
    parser.add_argument("--reviewed-at", help="RFC3339 UTC-ish landing time; defaults to now.")
    parser.add_argument("--reviewed-by", default="aoa-memo:reviewed-intake-landing")
    parser.add_argument("--current-recall-status", default="allowed", choices=["preferred", "allowed", "historical", "withdrawn"])
    parser.add_argument("--temperature", default="cool", choices=["warm", "cool", "cold", "frozen"])
    parser.add_argument("--confidence", default=0.85, type=float)
    parser.add_argument("--write", action="store_true", help="Write the planned landing files.")
    parser.add_argument("--replace", action="store_true", help="Replace existing landing files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        inputs = load_landing_inputs(args.port, args.export)
        plan = build_landing_plan(
            inputs,
            output_root=Path(args.output_root),
            object_kind=args.object_kind,
            slug=args.slug,
            title=args.title,
            summary=args.summary,
            object_id=args.object_id,
            reviewed_at=args.reviewed_at,
            reviewed_by=args.reviewed_by,
            current_recall_status=args.current_recall_status,
            temperature=args.temperature,
            confidence=args.confidence,
        )
        if args.write:
            write_landing_plan(plan, output_root=Path(args.output_root), replace=args.replace)
            print(f"[OK]   landed reviewed intake as {plan.object_rel_path}")
        else:
            print(json.dumps(plan_summary(plan), indent=2, ensure_ascii=False))
            print("[OK]   reviewed intake landing plan is valid")
        return 0
    except (LandingError, OSError, json.JSONDecodeError, shutil.Error) as exc:
        print(f"[FAIL] reviewed intake landing: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
