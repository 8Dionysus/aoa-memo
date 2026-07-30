#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parent
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from codex_owner_orientation_packet import (  # noqa: E402
    _artifact_digest,
    _canonical_digest,
    _common_header,
    _load,
    _parse_timestamp,
    _seal,
    _source_pin,
    _validate,
)


REPO_ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = (
    REPO_ROOT
    / "mechanics"
    / "consumer-handoff"
    / "parts"
    / "orchestrator-recall-alignment"
)
DEFAULT_PROFILE = (
    PART_ROOT
    / "examples"
    / "codex_owner_orientation_shadow_v0.consumer-profile.json"
)
DEFAULT_POLICY = (
    PART_ROOT
    / "examples"
    / "codex_owner_orientation_shadow_v0.influence-policy.json"
)
DEFAULT_COMPATIBILITY_PIN = (
    PART_ROOT
    / "examples"
    / "codex_owner_orientation_shadow_v0.sdk-compatibility-pin.json"
)
DEFAULT_COMPATIBILITY_SCHEMA = (
    PART_ROOT
    / "schemas"
    / "codex_owner_orientation_shadow_sdk_compatibility_pin_v0.schema.json"
)
DEFAULT_BUNDLE_SCHEMA = (
    PART_ROOT
    / "schemas"
    / "codex_owner_orientation_shadow_bundle_v0.schema.json"
)
ACTIVE_ORGAN_SCHEMA = (
    REPO_ROOT
    / "schemas"
    / "support-objects"
    / "active_organ_memo_contracts_v1.schema.json"
)


def _ref_source_pin(ref: dict[str, Any]) -> dict[str, Any]:
    return _source_pin(
        source_ref=ref["source_ref"],
        source_owner=ref["owner_repo"],
        source_version=ref["schema_version"],
        content_digest=ref["artifact_digest"],
    )


def _is_raw_aoa_ref(ref: dict[str, Any]) -> bool:
    return (
        ref.get("owner_repo") == ".aoa"
        or str(ref.get("artifact_ref", "")).startswith(".aoa/")
        or str(ref.get("source_ref", "")).startswith("repo:.aoa/")
    )


def validate_shadow_sdk_plan(
    *,
    plan: dict[str, Any],
    plan_schema: dict[str, Any],
    plan_schema_path: Path,
    profile: dict[str, Any],
    profile_path: Path,
    policy: dict[str, Any],
    policy_path: Path,
    compatibility_pin: dict[str, Any],
) -> None:
    _validate(plan_schema, plan, "SDK shadow plan")
    expected_schema = compatibility_pin["plan_schema"]
    if _artifact_digest(plan_schema_path) != expected_schema["sha256"]:
        raise ValueError("SDK shadow plan schema digest does not match its pin")
    expected_profile = compatibility_pin["consumer_profile"]
    if _artifact_digest(profile_path) != expected_profile["sha256"]:
        raise ValueError("shadow profile artifact digest does not match its pin")
    if plan["profile_ref"]["artifact_digest"] != expected_profile["sha256"]:
        raise ValueError("SDK shadow plan did not retain the exact profile artifact")
    if plan["profile_digest"] != expected_profile["semantic_digest"]:
        raise ValueError("SDK shadow profile semantic digest drifted")
    expected_policy = compatibility_pin["influence_policy"]
    if _artifact_digest(policy_path) != expected_policy["sha256"]:
        raise ValueError("shadow influence policy digest does not match its pin")
    if plan["schema_version"] not in compatibility_pin[
        "supported_plan_versions"
    ]:
        raise ValueError("unknown SDK shadow plan version")
    if plan["plan_digest"] != _canonical_digest(
        plan,
        exclude={"plan_digest"},
    ):
        raise ValueError("SDK shadow plan digest is invalid")

    intent = plan["recall_intent"]
    if (
        intent["contract_id"] != "C07"
        or intent["consumer_id"] != profile["consumer_id"]
        or intent["trigger_id"] != profile["trigger"]["trigger_id"]
        or intent["mode"] != "shadow_observation"
        or intent["data_class"] != "D0"
        or intent["risk_class"] != "R4"
        or intent["effect_ceiling"] != "none"
        or intent["action_use"] != "forbidden"
    ):
        raise ValueError("SDK shadow plan widened the C07 D0/R4 admission tuple")
    if intent["policy_pin"] != {
        "policy_id": profile["influence_policy"]["policy_id"],
        "policy_version": profile["influence_policy"]["policy_version"],
        "decision_ref": policy["policy_pin"]["decision_ref"],
        "policy_digest": expected_policy["sha256"],
    }:
        raise ValueError("SDK shadow plan C07 policy pin drifted")
    if intent["model_prompt_provider_pin"] != profile[
        "model_prompt_provider_pin"
    ]:
        raise ValueError("SDK shadow model/prompt/provider pin drifted")

    refs = [
        *intent["source_refs"],
        plan["pressure_evidence_ref"],
        plan["currentness_probe_ref"],
        plan["erase_reconciliation_ref"],
        *plan["outcome_refs"],
    ]
    if any(_is_raw_aoa_ref(ref) for ref in refs):
        raise ValueError("raw .aoa refs are forbidden in shadow construction")
    if plan["pressure_evidence_ref"]["owner_repo"] != "aoa-memo":
        raise ValueError("shadow pressure semantics must remain aoa-memo-owned")
    if plan["erase_reconciliation_ref"]["owner_repo"] != "aoa-memo":
        raise ValueError("shadow erase reconciliation must remain memo-owned")
    if not plan["outcome_refs"] or any(
        ref["owner_repo"] != "aoa-stats" for ref in plan["outcome_refs"]
    ):
        raise ValueError("shadow outcome refs must remain aoa-stats-owned C10")
    if (
        not plan["host_capability_ref"]["artifact_ref"].startswith("C18:")
        or not plan["host_resource_plan_ref"]["artifact_ref"].startswith("C19:")
    ):
        raise ValueError("shadow plan must retain exact C18/C19 refs")

    denied_true = (
        "consumer_visible",
        "delivery_authorized",
        "content_persisted",
        "candidate_persisted",
        "memory_write_performed",
        "semantic_transition_performed",
        "policy_promotion_performed",
    )
    if any(plan[field] for field in denied_true):
        raise ValueError("SDK shadow plan attempted delivery, persistence, or mutation")
    if plan["effect_authority"] != "none" or plan["action_use"] != "forbidden":
        raise ValueError("SDK shadow plan attempted effect or action authority")
    expected_policy_posture = (
        "proposal_only"
        if plan["eval_status"] == "available"
        and not plan["erase_residue_present"]
        else "frozen"
    )
    if plan["policy_posture"] != expected_policy_posture:
        raise ValueError("SDK shadow policy posture is not fail closed")
    if plan["status"] == "bounded_memory" and (
        plan["pressure_state"] != "clean"
        or plan["currentness_state"] != "current"
        or plan["erase_residue_present"]
        or plan["host_disposition"] in {"defer", "deny"}
    ):
        raise ValueError("inadmissible shadow inputs produced memory")

    for item in plan["items"]:
        card = item["card"]
        capsule = item["capsule"]
        if (
            card["source_kind"] != "reviewed_corpus"
            or card["review_state"] != "confirmed"
            or card["current_recall_status"] not in {"preferred", "allowed"}
            or capsule["source_kind"] != "reviewed_corpus"
            or item["expanded"] is not None
        ):
            raise ValueError("SDK shadow plan selected inadmissible memory")
        if (
            str(card["source_path"]).startswith(".aoa/")
            or str(capsule["source_path"]).startswith(".aoa/")
            or str(item["source_route"]).startswith(".aoa/")
        ):
            raise ValueError("SDK shadow plan selected a raw .aoa route")
        content = {
            "card": card,
            "capsule": capsule,
            "expanded": None,
            "source_route": item["source_route"],
        }
        if item["content_digest"] != _canonical_digest(content):
            raise ValueError(f"SDK shadow item digest is invalid: {card['id']}")

    planned_at = _parse_timestamp(plan["planned_at"], "planned_at")
    expires_at = _parse_timestamp(plan["expires_at"], "expires_at")
    if expires_at <= planned_at:
        raise ValueError("SDK shadow plan expiry must follow planning time")


def _shadow_header(
    *,
    contract_type: str,
    contract_id: str,
    contract_name: str,
    instance_id: str,
    produced_at: str,
    source_refs: list[dict[str, Any]],
    policy: dict[str, Any],
) -> dict[str, Any]:
    header = _common_header(
        contract_type=contract_type,
        contract_id=contract_id,
        contract_name=contract_name,
        instance_id=instance_id,
        produced_at=produced_at,
        source_refs=source_refs,
        policy=policy,
    )
    header["generation_pin"] = {
        "generator_id": "aoa-memo.codex-owner-orientation-shadow",
        "generator_version": "0",
        "generated_at": produced_at,
    }
    return header


def build_shadow_orientation_bundle(
    *,
    plan: dict[str, Any],
    plan_schema: dict[str, Any],
    plan_schema_path: Path,
    profile: dict[str, Any],
    profile_path: Path,
    policy: dict[str, Any],
    policy_path: Path,
    compatibility_pin: dict[str, Any],
    produced_at: str,
) -> dict[str, Any]:
    _validate(
        _load(DEFAULT_COMPATIBILITY_SCHEMA),
        compatibility_pin,
        "shadow SDK compatibility pin",
    )
    owner_schema = _load(ACTIVE_ORGAN_SCHEMA)
    _validate(owner_schema, policy, "C11 shadow influence policy")
    validate_shadow_sdk_plan(
        plan=plan,
        plan_schema=plan_schema,
        plan_schema_path=plan_schema_path,
        profile=profile,
        profile_path=profile_path,
        policy=policy,
        policy_path=policy_path,
        compatibility_pin=compatibility_pin,
    )
    produced = _parse_timestamp(produced_at, "produced_at")
    planned = _parse_timestamp(plan["planned_at"], "planned_at")
    expires = _parse_timestamp(plan["expires_at"], "expires_at")
    if produced < planned or produced > expires:
        raise ValueError("shadow bundle must be produced inside the plan window")

    suffix = plan["plan_digest"].removeprefix("sha256:")[:20]
    plan_source = _source_pin(
        source_ref=f"aoa-sdk:shadow-orientation-plan:{plan['plan_id']}",
        source_owner="aoa-sdk",
        source_version=plan["schema_version"],
        content_digest=plan["plan_digest"],
    )
    pressure_source = _ref_source_pin(plan["pressure_evidence_ref"])
    profile_source = _source_pin(
        source_ref=f"repo:aoa-memo/{plan['profile_ref']['artifact_ref']}",
        source_owner="aoa-memo",
        source_version=profile["schema_version"],
        content_digest=plan["profile_ref"]["artifact_digest"],
    )
    tainted = plan["pressure_state"] == "quarantine_required"
    taint = {
        "tainted": tainted,
        "labels": ["shadow-pressure-quarantine"] if tainted else [],
        "policy_version": "aoa-memo-shadow-pressure-v0",
        "sanitizer_receipt_ref": None,
        "quarantine_required": tainted,
    }
    freshness_class = (
        "current"
        if plan["currentness_state"] == "current"
        else plan["currentness_state"]
    )

    evidence_id = f"evidence:codex-owner-orientation-shadow:{suffix}"
    evidence = _seal(
        {
            **_shadow_header(
                contract_type="memory_evidence_envelope",
                contract_id="C01",
                contract_name="MemoryEvidenceEnvelope",
                instance_id=evidence_id,
                produced_at=produced_at,
                source_refs=[plan_source, pressure_source, profile_source],
                policy=policy,
            ),
            "observation_id": f"observation:shadow-pressure:{suffix}",
            "evidence_kind": "runtime_observation",
            "subject_ref": f"shadow-pressure:{plan['plan_id']}",
            "capture_ref": plan["pressure_evidence_ref"]["source_ref"],
            "evidence_refs": [
                plan["pressure_evidence_ref"]["source_ref"],
                plan["currentness_probe_ref"]["source_ref"],
            ],
            "freshness": {
                "observed_at": plan["recall_intent"]["anchor_freshness"][
                    "observed_at"
                ],
                "valid_at": plan["recall_intent"]["anchor_freshness"]["valid_at"],
                "expires_at": plan["recall_intent"]["anchor_freshness"][
                    "expires_at"
                ],
                "freshness_class": freshness_class,
            },
            "trust": {
                "authority_kind": "direct_observation",
                "confidence": 0.75,
            },
            "taint": taint,
        }
    )
    _validate(owner_schema, evidence, "C01 shadow pressure evidence")

    candidate_id = f"candidate:codex-owner-orientation-shadow:{suffix}"
    candidate = _seal(
        {
            **_shadow_header(
                contract_type="memory_candidate_packet",
                contract_id="C02",
                contract_name="MemoryCandidatePacket",
                instance_id=candidate_id,
                produced_at=produced_at,
                source_refs=[
                    plan_source,
                    _source_pin(
                        source_ref=evidence_id,
                        source_owner="aoa-memo",
                        source_version="1.0.0",
                        content_digest=evidence["content_digest"],
                    ),
                ],
                policy=policy,
            ),
            "candidate_id": candidate_id,
            "evidence_envelope_ref": evidence_id,
            "target_kind": "state_capsule",
            "candidate_payload_ref": f"ephemeral:shadow-pressure:{suffix}",
            "derivation_lineage_refs": [
                evidence_id,
                plan["pressure_evidence_ref"]["source_ref"],
            ],
            "risk_class": "R4",
            "data_class": "D0",
            "tenant_id": plan["recall_intent"]["tenant_id"],
            "expires_at": plan["expires_at"],
            "taint": taint,
            "proposed_belief": {
                "statement": (
                    "The current owner task pressure may benefit from bounded "
                    "reviewed-memory observation."
                ),
                "confidence": 0.5,
            },
            "proposed_applicability": {
                "scopes": ["workspace"],
                "conditions": [
                    "currentness remains current",
                    "host admission remains valid",
                    "consumer visibility remains false",
                ],
            },
            "expected_stronger_owner": "aoa-memo",
            "allowed_result": "quarantine" if tainted else "operator_review",
            "review_state": "proposed",
        }
    )
    _validate(owner_schema, candidate, "C02 shadow pressure candidate")

    quarantine = None
    if tainted:
        quarantine_id = f"quarantine:codex-owner-orientation-shadow:{suffix}"
        quarantine = _seal(
            {
                **_shadow_header(
                    contract_type="memory_quarantine_packet",
                    contract_id="C03",
                    contract_name="MemoryQuarantinePacket",
                    instance_id=quarantine_id,
                    produced_at=produced_at,
                    source_refs=[
                        _source_pin(
                            source_ref=candidate_id,
                            source_owner="aoa-memo",
                            source_version="1.0.0",
                            content_digest=candidate["content_digest"],
                        )
                    ],
                    policy=policy,
                ),
                "quarantine_id": quarantine_id,
                "candidate_ref": candidate_id,
                "reason_codes": ["shadow-pressure-quarantine"],
                "release_conditions": [
                    "owner-review-recorded",
                    "fresh-currentness-probe",
                ],
                "quarantined_at": produced_at,
                "expires_at": plan["expires_at"],
                "taint": taint,
                "expected_stronger_owner": "aoa-memo",
                "allowed_result": "operator_review",
                "semantic_promotion": "forbidden",
                "normal_recall": "forbidden",
                "proactive_delivery": "forbidden",
                "export_use": "forbidden",
                "training_use": "forbidden",
            }
        )
        _validate(owner_schema, quarantine, "C03 shadow quarantine")

    packet_id = f"recall-packet:codex-owner-orientation-shadow:{suffix}"
    result_mode = (
        "bounded_memory" if plan["status"] == "bounded_memory" else "silence"
    )
    result_refs = [
        f"memory-result:{item['card']['id']}:{item['content_digest'][7:23]}"
        for item in plan["items"]
    ]
    abstention_reason = (
        None if result_mode == "bounded_memory" else plan["silence_reason"]
    )
    packet_sources = [
        plan_source,
        profile_source,
        _source_pin(
            source_ref=evidence_id,
            source_owner="aoa-memo",
            source_version="1.0.0",
            content_digest=evidence["content_digest"],
        ),
        _source_pin(
            source_ref=candidate_id,
            source_owner="aoa-memo",
            source_version="1.0.0",
            content_digest=candidate["content_digest"],
        ),
    ]
    if quarantine is not None:
        packet_sources.append(
            _source_pin(
                source_ref=quarantine["instance_id"],
                source_owner="aoa-memo",
                source_version="1.0.0",
                content_digest=quarantine["content_digest"],
            )
        )
    recall_packet = _seal(
        {
            **_shadow_header(
                contract_type="recall_packet",
                contract_id="C08",
                contract_name="RecallPacket",
                instance_id=packet_id,
                produced_at=produced_at,
                source_refs=packet_sources,
                policy=policy,
            ),
            "request_ref": f"shadow-orientation-request:{plan['plan_id']}",
            "recall_intent_ref": (
                f"aoa-sdk:recall-intent:{plan['recall_intent']['intent_id']}"
            ),
            "trigger_ref": f"trigger:{plan['recall_intent']['trigger_id']}",
            "anchor_ref": plan["recall_intent"]["anchor_id"],
            "query_digest": plan["query_digest"],
            "scope": "workspace",
            "object_pins": [
                {
                    "object_ref": item["card"]["id"],
                    "object_version": plan["memory_object_catalog_version"],
                    "lifecycle_state": "confirmed",
                    "content_digest": _canonical_digest(item["card"]),
                }
                for item in plan["items"]
            ],
            "freshness": {
                "observed_at": plan["recall_intent"]["anchor_freshness"][
                    "observed_at"
                ],
                "valid_at": plan["recall_intent"]["anchor_freshness"]["valid_at"],
                "expires_at": plan["recall_intent"]["anchor_freshness"][
                    "expires_at"
                ],
                "freshness_class": freshness_class,
            },
            "taint": taint,
            "projection_pin": {
                "projection_id": "aoa-memo.memory-object-catalog.min",
                "projection_version": (
                    f"catalog-v{plan['memory_object_catalog_version']}"
                ),
                "built_from_digest": plan["memory_object_catalog_ref"][
                    "artifact_digest"
                ],
            },
            "model_pin": {
                "provider": plan["recall_intent"][
                    "model_prompt_provider_pin"
                ]["provider"],
                "model_id": plan["recall_intent"][
                    "model_prompt_provider_pin"
                ]["model_id"],
                "model_version": plan["recall_intent"][
                    "model_prompt_provider_pin"
                ]["model_version"],
            },
            "tenant_id": plan["recall_intent"]["tenant_id"],
            "result_mode": result_mode,
            "result_refs": result_refs,
            "abstention_reason": abstention_reason,
            "action_use": "forbidden",
        }
    )
    _validate(owner_schema, recall_packet, "C08 shadow recall packet")

    decision_id = f"intervention-decision:shadow:{suffix}"
    decision = (
        "bounded_observation"
        if recall_packet["result_mode"] == "bounded_memory"
        else "silence"
    )
    intervention_decision = _seal(
        {
            **_shadow_header(
                contract_type="intervention_decision",
                contract_id="C09",
                contract_name="InterventionDecision",
                instance_id=decision_id,
                produced_at=produced_at,
                source_refs=[
                    *packet_sources,
                    _source_pin(
                        source_ref=packet_id,
                        source_owner="aoa-memo",
                        source_version="1.0.0",
                        content_digest=recall_packet["content_digest"],
                    ),
                ],
                policy=policy,
            ),
            "decision_id": decision_id,
            "recall_packet_ref": packet_id,
            "trigger_ref": recall_packet["trigger_ref"],
            "anchor_ref": recall_packet["anchor_ref"],
            "taint_ref": f"taint:{packet_id}",
            "influence_policy_ref": policy["influence_policy_id"],
            "decision": decision,
            "rationale_codes": [
                (
                    "counterfactual-reviewed-current-memory"
                    if decision == "bounded_observation"
                    else recall_packet["abstention_reason"]
                )
            ],
            "effect_authority": "none",
            "observation_refs": result_refs,
        }
    )
    _validate(
        owner_schema,
        intervention_decision,
        "C09 shadow intervention decision",
    )

    residue = plan["erase_residue_present"]
    frozen = plan["policy_posture"] == "frozen"
    metabolism = {
        "currentness_probe_ref": plan["currentness_probe_ref"]["source_ref"],
        "currentness_state": plan["currentness_state"],
        "outcome_refs": [ref["source_ref"] for ref in plan["outcome_refs"]],
        "eval_status": plan["eval_status"],
        "policy_posture": plan["policy_posture"],
        "retention_proposal": (
            "blocked"
            if residue
            else "observe_only"
            if plan["status"] == "bounded_memory"
            else "no_change"
        ),
        "policy_proposal": (
            "frozen"
            if frozen
            else "observe_only"
            if plan["status"] == "bounded_memory"
            else "no_change"
        ),
        "erase_reconciliation_ref": plan["erase_reconciliation_ref"][
            "source_ref"
        ],
        "erase_residue_present": residue,
        "semantic_transition_performed": False,
        "proposal_accepted": False,
        "content_persisted": False,
    }
    bundle = {
        "schema_version": "codex_owner_orientation_shadow_bundle_v0",
        "semantic_owner": "aoa-memo",
        "control_plane_owner": "aoa-sdk",
        "runtime_owner": "abyss-stack",
        "host_owner": "abyss-machine",
        "outcome_owner": "aoa-stats",
        "proof_owner": "aoa-evals",
        "plan_ref": f"aoa-sdk:shadow-orientation-plan:{plan['plan_id']}",
        "plan_digest": plan["plan_digest"],
        "pressure_ingress": {
            "evidence_envelope": evidence,
            "candidate_packet": candidate,
            "quarantine_packet": quarantine,
            "workspace_persisted": False,
            "candidate_persisted": False,
            "semantic_promotion": "forbidden",
        },
        "recall_packet": recall_packet,
        "intervention_decision": intervention_decision,
        "metabolism": metabolism,
        "host_disposition": plan["host_disposition"],
        "consumer_visible": False,
        "delivery_eligible": False,
        "runtime_delivery_requested": False,
        "content_persisted": False,
        "candidate_persisted": False,
        "memory_write_performed": False,
        "semantic_transition_performed": False,
        "policy_promotion_performed": False,
        "effect_authority": "none",
        "action_use": "forbidden",
    }
    bundle["bundle_digest"] = _canonical_digest(
        bundle,
        exclude={"bundle_digest"},
    )
    _validate(
        _load(DEFAULT_BUNDLE_SCHEMA),
        bundle,
        "shadow orientation bundle",
    )
    return bundle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan")
    parser.add_argument("--sdk-plan-schema", required=True)
    parser.add_argument("--profile", default=str(DEFAULT_PROFILE))
    parser.add_argument("--policy", default=str(DEFAULT_POLICY))
    parser.add_argument(
        "--compatibility-pin",
        default=str(DEFAULT_COMPATIBILITY_PIN),
    )
    parser.add_argument("--produced-at", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    plan_path = Path(args.plan).expanduser().resolve()
    schema_path = Path(args.sdk_plan_schema).expanduser().resolve()
    profile_path = Path(args.profile).expanduser().resolve()
    policy_path = Path(args.policy).expanduser().resolve()
    pin_path = Path(args.compatibility_pin).expanduser().resolve()
    try:
        bundle = build_shadow_orientation_bundle(
            plan=_load(plan_path),
            plan_schema=_load(schema_path),
            plan_schema_path=schema_path,
            profile=_load(profile_path),
            profile_path=profile_path,
            policy=_load(policy_path),
            policy_path=policy_path,
            compatibility_pin=_load(pin_path),
            produced_at=args.produced_at,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}")
        return 1

    rendered = json.dumps(
        bundle,
        indent=2,
        ensure_ascii=True,
        sort_keys=True,
    )
    if args.output:
        Path(args.output).expanduser().resolve().write_text(
            rendered + "\n",
            encoding="utf-8",
        )
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
