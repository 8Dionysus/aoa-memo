from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[5]
PART = (
    ROOT
    / "mechanics"
    / "consumer-handoff"
    / "parts"
    / "orchestrator-recall-alignment"
)
PROFILE_PATH = (
    PART / "examples" / "codex_owner_orientation_v0.consumer-profile.json"
)
PROFILE_SCHEMA_PATH = (
    PART / "schemas" / "codex_owner_orientation_profile_v0.schema.json"
)
POLICY_PATH = (
    PART / "examples" / "codex_owner_orientation_v0.influence-policy.json"
)
SHADOW_PROFILE_PATH = (
    PART
    / "examples"
    / "codex_owner_orientation_shadow_v0.consumer-profile.json"
)
SHADOW_PROFILE_SCHEMA_PATH = (
    PART
    / "schemas"
    / "codex_owner_orientation_shadow_profile_v0.schema.json"
)
SHADOW_POLICY_PATH = (
    PART
    / "examples"
    / "codex_owner_orientation_shadow_v0.influence-policy.json"
)
SHADOW_SDK_PIN_PATH = (
    PART
    / "examples"
    / "codex_owner_orientation_shadow_v0.sdk-compatibility-pin.json"
)
SHADOW_SDK_PIN_SCHEMA_PATH = (
    PART
    / "schemas"
    / "codex_owner_orientation_shadow_sdk_compatibility_pin_v0.schema.json"
)
SDK_PIN_PATH = (
    PART / "examples" / "codex_owner_orientation_v0.sdk-compatibility-pin.json"
)
SDK_PIN_SCHEMA_PATH = (
    PART
    / "schemas"
    / "codex_owner_orientation_sdk_compatibility_pin_v0.schema.json"
)
BUNDLE_SCHEMA_PATH = (
    PART
    / "schemas"
    / "codex_owner_orientation_memo_bundle_v0.schema.json"
)
ACTIVE_ORGAN_SCHEMA_PATH = (
    ROOT
    / "schemas"
    / "support-objects"
    / "active_organ_memo_contracts_v1.schema.json"
)


def load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def canonical_digest(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def test_codex_owner_orientation_profile_and_policy_are_exact() -> None:
    profile_schema = load(PROFILE_SCHEMA_PATH)
    profile = load(PROFILE_PATH)
    policy_schema = load(ACTIVE_ORGAN_SCHEMA_PATH)
    policy = load(POLICY_PATH)

    Draft202012Validator.check_schema(profile_schema)
    Draft202012Validator.check_schema(policy_schema)
    Draft202012Validator(
        profile_schema,
        format_checker=FormatChecker(),
    ).validate(profile)
    Draft202012Validator(
        policy_schema,
        format_checker=FormatChecker(),
    ).validate(policy)

    policy_without_digest = dict(policy)
    observed_content_digest = policy_without_digest.pop("content_digest")
    assert observed_content_digest == (
        "sha256:" + canonical_digest(policy_without_digest)
    )
    assert profile["influence_policy"]["sha256"] == (
        "sha256:" + hashlib.sha256(POLICY_PATH.read_bytes()).hexdigest()
    )


def test_sdk_compatibility_pin_preserves_owner_split_and_exact_memo_inputs() -> None:
    schema = load(SDK_PIN_SCHEMA_PATH)
    pin = load(SDK_PIN_PATH)

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    ).validate(pin)
    assert pin["semantic_owner"] == "aoa-memo"
    assert pin["control_plane_owner"] == "aoa-sdk"
    assert pin["mirror_authority"] == "compatibility_only"
    assert pin["unknown_version_posture"] == "fail_closed"
    assert pin["consumer_profile"]["sha256"] == (
        "sha256:" + hashlib.sha256(PROFILE_PATH.read_bytes()).hexdigest()
    )
    assert pin["influence_policy"]["sha256"] == (
        "sha256:" + hashlib.sha256(POLICY_PATH.read_bytes()).hexdigest()
    )


def test_owner_orientation_bundle_schema_keeps_delivery_authority_empty() -> None:
    schema = load(BUNDLE_SCHEMA_PATH)

    Draft202012Validator.check_schema(schema)
    properties = schema["properties"]
    assert properties["semantic_owner"]["const"] == "aoa-memo"
    assert properties["control_plane_owner"]["const"] == "aoa-sdk"
    assert properties["runtime_delivery_owner"]["const"] == "abyss-stack"
    assert properties["effect_authority"]["const"] == "none"
    assert properties["action_use"]["const"] == "forbidden"
    assert properties["memory_write_performed"]["const"] is False


def test_codex_owner_orientation_profile_stays_pull_only_and_reversible() -> None:
    profile = load(PROFILE_PATH)

    assert profile["trigger"] == {
        "trigger_id": "operator-explicit-pull",
        "explicit_pull_required": True,
        "proactive_delivery": "forbidden",
    }
    assert profile["admission"]["allowed_consumer_modes"] == [
        "off",
        "fresh-start",
        "bounded",
        "high-fidelity",
    ]
    assert profile["admission"]["data_class"] == "D0"
    assert profile["admission"]["risk_class"] == "R1"
    assert profile["admission"]["sdk_route_required"] is True
    assert profile["admission"]["hidden_fallback"] == "forbidden"
    assert profile["model_prompt_provider_pin"] == {
        "provider": "none",
        "model_id": "deterministic-lexical",
        "model_version": "1",
        "prompt_digest": (
            "sha256:e3b0c44298fc1c149afbf4c8996fb924"
            "27ae41e4649b934ca495991b7852b855"
        ),
    }
    assert profile["selection"]["allowed_source_kinds"] == [
        "reviewed_corpus"
    ]
    assert profile["delivery"]["effect_ceiling"] == "none"
    assert profile["delivery"]["action_use"] == "forbidden"
    assert profile["receipts"]["content_persisted"] is False
    assert profile["rollback"]["target"] == "verified-current-no-memory"
    assert profile["rollback"]["memory_dependency_after_rollback"] is False
    assert not any(profile["authority"].values())


def test_shadow_profile_and_policy_are_exact_and_consumer_invisible() -> None:
    profile_schema = load(SHADOW_PROFILE_SCHEMA_PATH)
    profile = load(SHADOW_PROFILE_PATH)
    policy_schema = load(ACTIVE_ORGAN_SCHEMA_PATH)
    policy = load(SHADOW_POLICY_PATH)

    Draft202012Validator.check_schema(profile_schema)
    Draft202012Validator(
        profile_schema,
        format_checker=FormatChecker(),
    ).validate(profile)
    Draft202012Validator(
        policy_schema,
        format_checker=FormatChecker(),
    ).validate(policy)

    policy_without_digest = dict(policy)
    observed_content_digest = policy_without_digest.pop("content_digest")
    assert observed_content_digest == (
        "sha256:" + canonical_digest(policy_without_digest)
    )
    assert profile["influence_policy"]["sha256"] == (
        "sha256:" + hashlib.sha256(SHADOW_POLICY_PATH.read_bytes()).hexdigest()
    )
    assert profile["admission"]["risk_class"] == "R4"
    assert profile["delivery"]["consumer_visible"] is False
    assert profile["delivery"]["delivery_eligible"] is False
    assert profile["delivery"]["content_persistence"] == "forbidden"
    assert profile["metabolism"]["candidate_persistence"] == "forbidden"
    assert profile["metabolism"]["semantic_transition"] == "forbidden"
    assert profile["metabolism"]["policy_output"] == "proposal_only"
    assert profile["outcome"]["access_count_used_as_utility"] is False
    assert profile["outcome"]["eval_unavailable_posture"] == (
        "freeze_policy_and_mark_unknown"
    )
    assert not any(profile["authority"].values())


def test_shadow_sdk_pin_accepts_only_exact_profile_policy_and_plan_schema() -> None:
    schema = load(SHADOW_SDK_PIN_SCHEMA_PATH)
    pin = load(SHADOW_SDK_PIN_PATH)

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    ).validate(pin)
    assert pin["semantic_owner"] == "aoa-memo"
    assert pin["control_plane_owner"] == "aoa-sdk"
    assert pin["supported_plan_versions"] == [
        "codex_owner_orientation_shadow_plan_v0"
    ]
    assert pin["consumer_profile"]["sha256"] == (
        "sha256:" + hashlib.sha256(SHADOW_PROFILE_PATH.read_bytes()).hexdigest()
    )
    assert pin["influence_policy"]["sha256"] == (
        "sha256:" + hashlib.sha256(SHADOW_POLICY_PATH.read_bytes()).hexdigest()
    )
