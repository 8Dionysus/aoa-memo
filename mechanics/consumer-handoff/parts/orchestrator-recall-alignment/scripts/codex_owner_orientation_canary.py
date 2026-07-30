#!/usr/bin/env python3
from __future__ import annotations

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
    / "codex_owner_orientation_canary_v0.consumer-profile.json"
)
DEFAULT_POLICY = (
    PART_ROOT
    / "examples"
    / "codex_owner_orientation_canary_v0.influence-policy.json"
)
DEFAULT_BUNDLE_SCHEMA = (
    PART_ROOT
    / "schemas"
    / "codex_owner_orientation_canary_bundle_v0.schema.json"
)
DEFAULT_COMPATIBILITY_PIN = (
    PART_ROOT
    / "examples"
    / "codex_owner_orientation_canary_v0.sdk-compatibility-pin.json"
)
ACTIVE_ORGAN_SCHEMA = (
    REPO_ROOT
    / "schemas"
    / "support-objects"
    / "active_organ_memo_contracts_v1.schema.json"
)


def _canary_header(
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
        "generator_id": "aoa-memo.codex-owner-orientation-canary",
        "generator_version": "0",
        "generated_at": produced_at,
    }
    return header


def validate_canary_release(
    *,
    release_plan: dict[str, Any],
    release_plan_schema: dict[str, Any],
    release_plan_schema_path: Path,
    shadow_plan: dict[str, Any],
    shadow_bundle: dict[str, Any],
    profile: dict[str, Any],
    profile_path: Path,
    policy: dict[str, Any],
    policy_path: Path,
    compatibility_pin: dict[str, Any],
) -> None:
    _validate(release_plan_schema, release_plan, "SDK canary release plan")
    if (
        _artifact_digest(release_plan_schema_path)
        != compatibility_pin["plan_schema"]["sha256"]
        or release_plan["schema_version"]
        not in compatibility_pin["supported_plan_versions"]
        or _artifact_digest(profile_path)
        != compatibility_pin["consumer_profile"]["sha256"]
        or _canonical_digest(profile)
        != compatibility_pin["consumer_profile"]["semantic_digest"]
        or _artifact_digest(policy_path)
        != compatibility_pin["influence_policy"]["sha256"]
    ):
        raise ValueError("canary SDK compatibility pin drifted")
    if release_plan["plan_digest"] != _canonical_digest(
        release_plan,
        exclude={"plan_digest"},
    ):
        raise ValueError("SDK canary release plan digest is invalid")
    if shadow_plan["plan_digest"] != _canonical_digest(
        shadow_plan,
        exclude={"plan_digest"},
    ):
        raise ValueError("source shadow plan digest is invalid")
    if shadow_bundle["bundle_digest"] != _canonical_digest(
        shadow_bundle,
        exclude={"bundle_digest"},
    ):
        raise ValueError("source shadow bundle digest is invalid")
    if (
        release_plan["source_shadow_plan_digest"]
        != shadow_plan["plan_digest"]
        or release_plan["source_shadow_plan_ref"]["artifact_digest"]
        != shadow_plan["plan_digest"]
        or release_plan["source_shadow_bundle_digest"]
        != shadow_bundle["bundle_digest"]
        or release_plan["source_shadow_bundle_ref"]["artifact_digest"]
        != shadow_bundle["bundle_digest"]
    ):
        raise ValueError("canary release does not bind the exact shadow artifacts")
    if (
        release_plan["profile_ref"]["owner_repo"] != "aoa-memo"
        or release_plan["profile_ref"]["artifact_digest"]
        != _artifact_digest(profile_path)
        or release_plan["profile_digest"] != _canonical_digest(profile)
        or release_plan["policy_ref"]["owner_repo"] != "aoa-memo"
        or release_plan["policy_digest"] != _artifact_digest(policy_path)
        or release_plan["policy_ref"]["artifact_digest"]
        != _artifact_digest(policy_path)
    ):
        raise ValueError("canary profile or C11 policy pin drifted")
    if (
        profile["decision_ref"] != "decision:AOA-MEM-D-0077"
        or profile["consumer_id"] != "codex_owner_orientation_canary_v0"
        or release_plan["consumer_id"] != profile["consumer_id"]
        or policy["consumer_id"] != profile["consumer_id"]
        or policy["risk_class"] != "R2"
        or policy["data_class"] != "D0"
        or policy["external_effects"] != "forbidden"
    ):
        raise ValueError("canary owner decision or D0/R2 policy drifted")
    if policy["content_digest"] != _canonical_digest(
        policy,
        exclude={"content_digest"},
    ):
        raise ValueError("canary C11 policy self-digest is invalid")
    if release_plan["assigned_arm"] == "canary" and (
        release_plan["always_shadow_counterfactual_ref"]["owner_repo"]
        != "aoa-evals"
        or release_plan["assignment_ref"]["owner_repo"] != "aoa-evals"
    ):
        raise ValueError("canary requires eval-owned holdout/counterfactual refs")
    if release_plan["status"] == "bounded_observation":
        if (
            len(release_plan["items"]) != 1
            or shadow_plan["status"] != "bounded_memory"
            or not shadow_plan["items"]
        ):
            raise ValueError("bounded canary requires one frozen shadow item")
        release_item = release_plan["items"][0]
        source_item = shadow_plan["items"][0]
        if release_item != {
            "object_id": source_item["card"]["id"],
            "content_digest": source_item["content_digest"],
            "source_route": source_item["source_route"],
            "selection_score": source_item["selection_score"],
            "source_visible": True,
            "currentness_visible": True,
        }:
            raise ValueError("canary release item drifted from shadow selection")
        if (
            source_item["card"]["source_kind"] != "reviewed_corpus"
            or source_item["card"]["review_state"] != "confirmed"
            or source_item["card"]["current_recall_status"]
            not in {"preferred", "allowed"}
            or source_item["expanded"] is not None
        ):
            raise ValueError("canary selected inadmissible memory")
    elif release_plan["items"]:
        raise ValueError("non-delivery canary release must carry no items")


def build_canary_orientation_bundle(
    *,
    release_plan: dict[str, Any],
    release_plan_schema: dict[str, Any],
    release_plan_schema_path: Path,
    shadow_plan: dict[str, Any],
    shadow_bundle: dict[str, Any],
    profile: dict[str, Any],
    profile_path: Path,
    policy: dict[str, Any],
    policy_path: Path,
    compatibility_pin: dict[str, Any],
    produced_at: str,
) -> dict[str, Any]:
    owner_schema = _load(ACTIVE_ORGAN_SCHEMA)
    _validate(owner_schema, policy, "C11 canary influence policy")
    validate_canary_release(
        release_plan=release_plan,
        release_plan_schema=release_plan_schema,
        release_plan_schema_path=release_plan_schema_path,
        shadow_plan=shadow_plan,
        shadow_bundle=shadow_bundle,
        profile=profile,
        profile_path=profile_path,
        policy=policy,
        policy_path=policy_path,
        compatibility_pin=compatibility_pin,
    )
    produced = _parse_timestamp(produced_at, "produced_at")
    planned = _parse_timestamp(release_plan["planned_at"], "planned_at")
    expires = _parse_timestamp(release_plan["expires_at"], "expires_at")
    if produced < planned or produced > expires:
        raise ValueError("canary bundle must be produced inside release window")

    suffix = release_plan["plan_digest"][7:27]
    release_source = _source_pin(
        source_ref=f"aoa-sdk:canary-release:{release_plan['plan_id']}",
        source_owner="aoa-sdk",
        source_version=release_plan["schema_version"],
        content_digest=release_plan["plan_digest"],
    )
    shadow_source = _source_pin(
        source_ref=release_plan["source_shadow_plan_ref"]["source_ref"],
        source_owner="aoa-sdk",
        source_version="codex_owner_orientation_shadow_plan_v0",
        content_digest=shadow_plan["plan_digest"],
    )
    profile_source = _source_pin(
        source_ref=release_plan["profile_ref"]["source_ref"],
        source_owner="aoa-memo",
        source_version=profile["schema_version"],
        content_digest=release_plan["profile_ref"]["artifact_digest"],
    )
    packet_sources = [release_source, shadow_source, profile_source]
    delivery = release_plan["status"] == "bounded_observation"
    source_item = shadow_plan["items"][0] if delivery else None
    result_refs = (
        [
            "canary-observation:"
            + release_plan["items"][0]["object_id"]
            + ":"
            + release_plan["items"][0]["content_digest"][7:23]
        ]
        if delivery
        else []
    )
    packet_id = f"recall-packet:codex-owner-orientation-canary:{suffix}"
    freshness = shadow_bundle["recall_packet"]["freshness"]
    recall_packet = _seal(
        {
            **_canary_header(
                contract_type="recall_packet",
                contract_id="C08",
                contract_name="RecallPacket",
                instance_id=packet_id,
                produced_at=produced_at,
                source_refs=packet_sources,
                policy=policy,
            ),
            "request_ref": f"canary-release-request:{release_plan['plan_id']}",
            "recall_intent_ref": (
                release_plan["source_shadow_plan_ref"]["source_ref"]
            ),
            "trigger_ref": "trigger:owner-task-pressure-canary",
            "anchor_ref": shadow_plan["recall_intent"]["anchor_id"],
            "query_digest": shadow_plan["query_digest"],
            "scope": "workspace",
            "object_pins": (
                [
                    {
                        "object_ref": source_item["card"]["id"],
                        "object_version": shadow_plan[
                            "memory_object_catalog_version"
                        ],
                        "lifecycle_state": "confirmed",
                        "content_digest": _canonical_digest(source_item["card"]),
                    }
                ]
                if source_item is not None
                else []
            ),
            "freshness": freshness,
            "taint": {
                "tainted": False,
                "labels": [],
                "policy_version": "aoa-memo-canary-v0",
                "sanitizer_receipt_ref": None,
                "quarantine_required": False,
            },
            "projection_pin": shadow_bundle["recall_packet"]["projection_pin"],
            "model_pin": policy["model_pin"],
            "tenant_id": "owner-local",
            "result_mode": "bounded_memory" if delivery else "silence",
            "result_refs": result_refs,
            "abstention_reason": (
                None if delivery else release_plan["silence_reason"]
            ),
            "action_use": "forbidden",
        }
    )
    _validate(owner_schema, recall_packet, "C08 canary recall packet")

    decision_id = f"intervention-decision:canary:{suffix}"
    intervention_decision = _seal(
        {
            **_canary_header(
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
            "decision": "bounded_observation" if delivery else "silence",
            "rationale_codes": [
                (
                    "operator-approved-selective-canary"
                    if delivery
                    else release_plan["silence_reason"]
                )
            ],
            "effect_authority": "none",
            "observation_refs": result_refs,
        }
    )
    _validate(owner_schema, intervention_decision, "C09 canary decision")

    observation = None
    if source_item is not None:
        observation = {
            "observation_kind": "source_linked_memory_observation",
            "object_id": source_item["card"]["id"],
            "title": source_item["card"]["title"],
            "summary": source_item["capsule"]["summary"],
            "use_when": source_item["capsule"]["use_when_short"],
            "do_not_use": source_item["capsule"]["do_not_use_short"],
            "source_route": source_item["source_route"],
            "currentness": source_item["card"]["current_recall_status"],
            "contradiction_refs": source_item["card"]["contradiction_refs"],
            "directive": False,
            "suggested_action": None,
            "source_visible": True,
            "currentness_visible": True,
        }
        observation["content_digest"] = _canonical_digest(observation)

    bundle = {
        "schema_version": "codex_owner_orientation_canary_bundle_v0",
        "semantic_owner": "aoa-memo",
        "control_plane_owner": "aoa-sdk",
        "runtime_owner": "abyss-stack",
        "host_owner": "abyss-machine",
        "outcome_owner": "aoa-stats",
        "proof_owner": "aoa-evals",
        "release_plan_ref": f"aoa-sdk:canary-release:{release_plan['plan_id']}",
        "release_plan_digest": release_plan["plan_digest"],
        "source_shadow_plan_digest": shadow_plan["plan_digest"],
        "source_shadow_bundle_digest": shadow_bundle["bundle_digest"],
        "assignment_ref": release_plan["assignment_ref"]["source_ref"],
        "assigned_arm": release_plan["assigned_arm"],
        "window_id": release_plan["window_id"],
        "recall_packet": recall_packet,
        "intervention_decision": intervention_decision,
        "observation": observation,
        "consumer_visible": delivery,
        "delivery_eligible": delivery,
        "directive_authority": False,
        "source_visible": True,
        "currentness_visible": True,
        "content_persisted": False,
        "candidate_persisted": False,
        "memory_write_performed": False,
        "semantic_transition_performed": False,
        "policy_promotion_performed": False,
        "effect_authority": "none",
        "action_use": "forbidden",
        "rollback_target": "codex_owner_orientation_v0",
        "bundle_digest": "sha256:" + ("0" * 64),
    }
    bundle["bundle_digest"] = _canonical_digest(
        bundle,
        exclude={"bundle_digest"},
    )
    _validate(_load(DEFAULT_BUNDLE_SCHEMA), bundle, "canary bundle")
    return bundle


def main() -> int:
    raise SystemExit(
        "use build_canary_orientation_bundle through the source-local lab"
    )


if __name__ == "__main__":
    main()
