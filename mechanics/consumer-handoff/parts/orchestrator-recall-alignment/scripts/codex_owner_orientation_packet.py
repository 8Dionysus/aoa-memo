#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


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
    / "codex_owner_orientation_v0.consumer-profile.json"
)
DEFAULT_POLICY = (
    PART_ROOT
    / "examples"
    / "codex_owner_orientation_v0.influence-policy.json"
)
DEFAULT_COMPATIBILITY_PIN = (
    PART_ROOT
    / "examples"
    / "codex_owner_orientation_v0.sdk-compatibility-pin.json"
)
DEFAULT_COMPATIBILITY_SCHEMA = (
    PART_ROOT
    / "schemas"
    / "codex_owner_orientation_sdk_compatibility_pin_v0.schema.json"
)
DEFAULT_BUNDLE_SCHEMA = (
    PART_ROOT
    / "schemas"
    / "codex_owner_orientation_memo_bundle_v0.schema.json"
)
ACTIVE_ORGAN_SCHEMA = (
    REPO_ROOT
    / "schemas"
    / "support-objects"
    / "active_organ_memo_contracts_v1.schema.json"
)


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object: {path}")
    return payload


def _artifact_digest(path: Path) -> str:
    return f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}"


def _canonical_digest(
    payload: dict[str, Any],
    *,
    exclude: set[str] | None = None,
    ensure_ascii: bool = True,
) -> str:
    filtered = {
        key: value
        for key, value in payload.items()
        if key not in (exclude or set())
    }
    encoded = json.dumps(
        filtered,
        ensure_ascii=ensure_ascii,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _validate(schema: dict[str, Any], payload: dict[str, Any], label: str) -> None:
    errors = sorted(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        error = errors[0]
        location = "/".join(str(item) for item in error.absolute_path) or "<root>"
        raise ValueError(f"{label} {location}: {error.message}")


def _parse_timestamp(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must be timezone-aware")
    return parsed


def _source_pin(
    *,
    source_ref: str,
    source_owner: str,
    source_version: str,
    content_digest: str,
) -> dict[str, Any]:
    return {
        "source_ref": source_ref,
        "source_owner": source_owner,
        "source_version": source_version,
        "content_digest": content_digest,
    }


def validate_sdk_plan(
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
    _validate(plan_schema, plan, "SDK plan")
    expected_schema = compatibility_pin["plan_schema"]
    if _artifact_digest(plan_schema_path) != expected_schema["sha256"]:
        raise ValueError("SDK plan schema digest does not match the memo acceptance pin")
    expected_profile = compatibility_pin["consumer_profile"]
    if _artifact_digest(profile_path) != expected_profile["sha256"]:
        raise ValueError("consumer profile artifact digest does not match its pin")
    if plan["profile_ref"]["artifact_digest"] != expected_profile["sha256"]:
        raise ValueError("SDK plan did not retain the exact consumer profile artifact")
    if plan["profile_digest"] != expected_profile["semantic_digest"]:
        raise ValueError("SDK plan consumer profile semantic digest drifted")
    expected_policy = compatibility_pin["influence_policy"]
    if _artifact_digest(policy_path) != expected_policy["sha256"]:
        raise ValueError("influence policy artifact digest does not match its pin")
    if plan["schema_version"] not in compatibility_pin["supported_plan_versions"]:
        raise ValueError("unknown SDK owner-orientation plan version")
    if plan["plan_digest"] != _canonical_digest(
        plan,
        exclude={"plan_digest"},
    ):
        raise ValueError("SDK owner-orientation plan digest is invalid")

    intent = plan["recall_intent"]
    if (
        intent["contract_id"] != "C07"
        or intent["consumer_id"] != profile["consumer_id"]
        or intent["trigger_id"] != profile["trigger"]["trigger_id"]
        or intent["mode"] != "explicit_public_pull"
        or intent["data_class"] != "D0"
        or intent["risk_class"] != "R1"
        or intent["effect_ceiling"] != "none"
        or intent["action_use"] != "forbidden"
    ):
        raise ValueError("SDK plan widened the C07 owner-orientation admission tuple")
    if intent["policy_pin"] != {
        "policy_id": profile["influence_policy"]["policy_id"],
        "policy_version": profile["influence_policy"]["policy_version"],
        "decision_ref": policy["policy_pin"]["decision_ref"],
        "policy_digest": expected_policy["sha256"],
    }:
        raise ValueError("SDK plan C07 policy pin drifted")
    if intent["model_prompt_provider_pin"] != profile["model_prompt_provider_pin"]:
        raise ValueError("SDK plan model/prompt/provider pin drifted")
    if any(
        ref.get("owner_repo") == ".aoa"
        or str(ref.get("artifact_ref", "")).startswith(".aoa/")
        or str(ref.get("source_ref", "")).startswith("repo:.aoa/")
        for ref in intent["source_refs"]
    ):
        raise ValueError("raw .aoa source refs are forbidden")
    if plan["effect_authority"] != "none" or plan["action_use"] != "forbidden":
        raise ValueError("SDK plan attempted to grant effect or action authority")
    if plan["memory_write_performed"] or plan["policy_promotion_performed"]:
        raise ValueError("SDK plan reported a hidden memory write or promotion")

    for item in plan["items"]:
        card = item["card"]
        capsule = item["capsule"]
        if (
            card["source_kind"] != "reviewed_corpus"
            or card["review_state"] != "confirmed"
            or card["current_recall_status"] not in {"preferred", "allowed"}
            or capsule["source_kind"] != "reviewed_corpus"
        ):
            raise ValueError("SDK plan selected an inadmissible memory object")
        if (
            str(card["source_path"]).startswith(".aoa/")
            or str(capsule["source_path"]).startswith(".aoa/")
            or str(item["source_route"]).startswith(".aoa/")
        ):
            raise ValueError("SDK plan selected a forbidden raw .aoa route")
        content = {
            "card": card,
            "capsule": capsule,
            "expanded": item["expanded"],
            "source_route": item["source_route"],
        }
        if item["content_digest"] != _canonical_digest(content):
            raise ValueError(f"SDK plan item digest is invalid: {card['id']}")

    planned_at = _parse_timestamp(plan["planned_at"], "planned_at")
    expires_at = _parse_timestamp(plan["expires_at"], "expires_at")
    if expires_at <= planned_at:
        raise ValueError("SDK plan expiry must follow planning time")


def _common_header(
    *,
    contract_type: str,
    contract_id: str,
    contract_name: str,
    instance_id: str,
    produced_at: str,
    source_refs: list[dict[str, Any]],
    policy: dict[str, Any],
) -> dict[str, Any]:
    return {
        "contract_type": contract_type,
        "schema_version": "1.0.0",
        "contract_id": contract_id,
        "contract_name": contract_name,
        "instance_id": instance_id,
        "object_version": 1,
        "idempotency_key": instance_id,
        "produced_at": produced_at,
        "owner": "aoa-memo",
        "validation_status": "valid",
        "source_refs": source_refs,
        "generation_pin": {
            "generator_id": "aoa-memo.codex-owner-orientation-packet",
            "generator_version": "0",
            "generated_at": produced_at,
        },
        "policy_pin": policy["policy_pin"],
    }


def _seal(payload: dict[str, Any]) -> dict[str, Any]:
    payload["content_digest"] = _canonical_digest(
        payload,
        exclude={"content_digest"},
        ensure_ascii=False,
    )
    return payload


def build_owner_orientation_bundle(
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
    compatibility_schema = _load(DEFAULT_COMPATIBILITY_SCHEMA)
    _validate(
        compatibility_schema,
        compatibility_pin,
        "SDK compatibility pin",
    )
    owner_schema = _load(ACTIVE_ORGAN_SCHEMA)
    _validate(owner_schema, policy, "C11 influence policy")
    validate_sdk_plan(
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
    if produced > _parse_timestamp(plan["expires_at"], "plan expires_at"):
        raise ValueError("memo packet cannot be produced after the SDK plan expires")

    digest_suffix = plan["plan_digest"].removeprefix("sha256:")[:20]
    packet_id = f"recall-packet:codex-owner-orientation:{digest_suffix}"
    decision_id = f"intervention-decision:codex-owner-orientation:{digest_suffix}"
    source_refs = [
        _source_pin(
            source_ref=f"aoa-sdk:owner-orientation-plan:{plan['plan_id']}",
            source_owner="aoa-sdk",
            source_version=plan["schema_version"],
            content_digest=plan["plan_digest"],
        ),
        _source_pin(
            source_ref=f"repo:aoa-memo/{plan['profile_ref']['artifact_ref']}",
            source_owner="aoa-memo",
            source_version=profile["schema_version"],
            content_digest=plan["profile_ref"]["artifact_digest"],
        ),
        _source_pin(
            source_ref=plan["memory_object_catalog_ref"]["source_ref"],
            source_owner="aoa-memo",
            source_version=plan["memory_object_catalog_ref"]["schema_version"],
            content_digest=plan["memory_object_catalog_ref"]["artifact_digest"],
        ),
    ]
    common = _common_header(
        contract_type="recall_packet",
        contract_id="C08",
        contract_name="RecallPacket",
        instance_id=packet_id,
        produced_at=produced_at,
        source_refs=source_refs,
        policy=policy,
    )
    result_mode = (
        "bounded_memory" if plan["status"] == "bounded_memory" else "silence"
    )
    result_refs = [
        f"memory-result:{item['card']['id']}:{item['content_digest'][7:23]}"
        for item in plan["items"]
    ]
    abstention_reason = None
    if result_mode == "silence":
        abstention_reason = {
            "off": "consumer-mode-off",
            "no_memory": "fresh-start-no-memory",
            "silence": "no-admissible-memory",
        }[plan["status"]]
    recall_packet = _seal(
        {
            **common,
            "request_ref": f"orientation-request:{plan['plan_id']}",
            "recall_intent_ref": (
                f"aoa-sdk:recall-intent:{plan['recall_intent']['intent_id']}"
            ),
            "trigger_ref": (
                f"trigger:{plan['recall_intent']['trigger_id']}"
            ),
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
                "freshness_class": "current",
            },
            "taint": {
                "tainted": False,
                "labels": [],
                "policy_version": "aoa-memo-public-reviewed-only-v0",
                "sanitizer_receipt_ref": None,
                "quarantine_required": False,
            },
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
    _validate(owner_schema, recall_packet, "C08 recall packet")

    decision = (
        "bounded_observation"
        if recall_packet["result_mode"] == "bounded_memory"
        else "silence"
    )
    decision_common = _common_header(
        contract_type="intervention_decision",
        contract_id="C09",
        contract_name="InterventionDecision",
        instance_id=decision_id,
        produced_at=produced_at,
        source_refs=[
            *source_refs,
            _source_pin(
                source_ref=packet_id,
                source_owner="aoa-memo",
                source_version="1.0.0",
                content_digest=recall_packet["content_digest"],
            ),
        ],
        policy=policy,
    )
    intervention_decision = _seal(
        {
            **decision_common,
            "decision_id": decision_id,
            "recall_packet_ref": packet_id,
            "trigger_ref": recall_packet["trigger_ref"],
            "anchor_ref": recall_packet["anchor_ref"],
            "taint_ref": f"taint:{packet_id}",
            "influence_policy_ref": policy["influence_policy_id"],
            "decision": decision,
            "rationale_codes": [
                (
                    "reviewed-current-bounded-memory"
                    if decision == "bounded_observation"
                    else recall_packet["abstention_reason"]
                )
            ],
            "effect_authority": "none",
            "observation_refs": result_refs,
        }
    )
    _validate(owner_schema, intervention_decision, "C09 intervention decision")

    bundle = {
        "schema_version": "codex_owner_orientation_memo_bundle_v0",
        "semantic_owner": "aoa-memo",
        "control_plane_owner": "aoa-sdk",
        "runtime_delivery_owner": "abyss-stack",
        "plan_ref": f"aoa-sdk:owner-orientation-plan:{plan['plan_id']}",
        "plan_digest": plan["plan_digest"],
        "recall_packet": recall_packet,
        "intervention_decision": intervention_decision,
        "delivery_eligible": True,
        "effect_authority": "none",
        "action_use": "forbidden",
        "memory_write_performed": False,
    }
    bundle["bundle_digest"] = _canonical_digest(
        bundle,
        exclude={"bundle_digest"},
    )
    _validate(
        _load(DEFAULT_BUNDLE_SCHEMA),
        bundle,
        "owner-orientation memo bundle",
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
        bundle = build_owner_orientation_bundle(
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
