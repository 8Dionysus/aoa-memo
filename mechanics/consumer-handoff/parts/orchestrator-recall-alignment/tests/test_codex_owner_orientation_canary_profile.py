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
    PART
    / "examples"
    / "codex_owner_orientation_canary_v0.consumer-profile.json"
)
PROFILE_SCHEMA_PATH = (
    PART
    / "schemas"
    / "codex_owner_orientation_canary_profile_v0.schema.json"
)
POLICY_PATH = (
    PART
    / "examples"
    / "codex_owner_orientation_canary_v0.influence-policy.json"
)
BUNDLE_SCHEMA_PATH = (
    PART / "schemas" / "codex_owner_orientation_canary_bundle_v0.schema.json"
)
SDK_PIN_PATH = (
    PART
    / "examples"
    / "codex_owner_orientation_canary_v0.sdk-compatibility-pin.json"
)
SDK_PIN_SCHEMA_PATH = (
    PART
    / "schemas"
    / "codex_owner_orientation_canary_sdk_compatibility_pin_v0.schema.json"
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
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def test_canary_profile_policy_and_bundle_keep_the_visible_lane_bounded() -> None:
    profile_schema = load(PROFILE_SCHEMA_PATH)
    profile = load(PROFILE_PATH)
    policy_schema = load(ACTIVE_ORGAN_SCHEMA_PATH)
    policy = load(POLICY_PATH)
    bundle_schema = load(BUNDLE_SCHEMA_PATH)

    for schema in (profile_schema, policy_schema, bundle_schema):
        Draft202012Validator.check_schema(schema)
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
    assert profile["decision_ref"] == "decision:AOA-MEM-D-0077"
    assert profile["admission"]["risk_class"] == "R2"
    assert profile["admission"]["no_secrets"] is True
    assert profile["delivery"]["max_reminders_per_window"] == 1
    assert profile["delivery"]["directive_authority"] is False
    assert profile["delivery"]["source_visible"] is True
    assert profile["delivery"]["currentness_visible"] is True
    assert profile["experiment"]["randomized_holdout_required"] is True
    assert profile["experiment"]["always_shadow_counterfactual_required"] is True
    assert profile["rollback"]["instant_disable"] is True
    assert not any(profile["authority"].values())


def test_canary_sdk_pin_accepts_only_the_exact_release_profile_and_policy() -> None:
    schema = load(SDK_PIN_SCHEMA_PATH)
    pin = load(SDK_PIN_PATH)

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    ).validate(pin)
    assert pin["semantic_owner"] == "aoa-memo"
    assert pin["control_plane_owner"] == "aoa-sdk"
    assert pin["supported_plan_versions"] == [
        "codex_owner_orientation_canary_release_plan_v0"
    ]
    assert pin["consumer_profile"]["sha256"] == (
        "sha256:" + hashlib.sha256(PROFILE_PATH.read_bytes()).hexdigest()
    )
    assert pin["influence_policy"]["sha256"] == (
        "sha256:" + hashlib.sha256(POLICY_PATH.read_bytes()).hexdigest()
    )
    assert pin["max_reminders_per_window"] == 1
    assert pin["directive_authority"] == "forbidden"
    assert pin["rollback_target"] == "codex_owner_orientation_v0"
