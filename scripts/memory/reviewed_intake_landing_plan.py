from __future__ import annotations

from pathlib import Path

from reviewed_intake_landing_common import (
    ID_PREFIX_BY_KIND,
    KIND_DIRS,
    LOCAL_KIND_TO_OBJECT_KIND,
    SYMBOLIC_REF_PREFIXES,
    JsonDict,
    LandingError,
    LandingInputs,
    LandingPlan,
    date_from_rfc3339,
    dedupe,
    object_schema_errors,
    rfc3339_now,
    slugify,
    stamp_from_rfc3339,
    support_schema_errors,
    year_from_rfc3339,
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
    output_root: Path,
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
    output_root.resolve()
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
            "export_source_refs",
            "export_evidence_refs",
            "allowed_result_reviewed_write",
            "candidate_schema",
            "candidate_source_refs",
            "candidate_evidence_refs",
            "candidate_guardrails",
            "receipt_schema",
            "receipt_candidate_ref",
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
