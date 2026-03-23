#!/usr/bin/env python3
"""Validate lifecycle and audit examples for aoa-memo."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from validate_memo import local_ref_error, validator_for

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
MEMORY_OBJECT_REF_LABELS = (
    ("payload_ref", lambda data: data.get("payload_ref")),
    ("bridges.route_capsule_ref", lambda data: data.get("bridges", {}).get("route_capsule_ref")),
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate(path: Path, validator, extra_errors=None) -> dict:
    data = load_json(path)
    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
    ]
    if extra_errors is not None:
        errors.extend(extra_errors(data))
    if errors:
        print(f"[FAIL] {path.name}")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print(f"[OK]   {path.name}")
    return data


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def memory_object_ref_errors(data: dict) -> list[str]:
    errors = []
    for label, getter in MEMORY_OBJECT_REF_LABELS:
        error = local_ref_error(getter(data), label)
        if error:
            errors.append(error)
    return errors


def main() -> int:
    memory_validator = validator_for("memory_object.schema.json")
    thread_validator = validator_for("provenance_thread.schema.json")

    superseded_claim = validate(
        EXAMPLES / "claim.superseded.example.json",
        memory_validator,
        memory_object_ref_errors,
    )
    anchor = validate(
        EXAMPLES / "anchor.example.json",
        memory_validator,
        memory_object_ref_errors,
    )
    replacement_claim = validate(
        EXAMPLES / "claim.current-entrypoint.example.json",
        memory_validator,
        memory_object_ref_errors,
    )
    retracted_claim = validate(
        EXAMPLES / "claim.retracted.example.json",
        memory_validator,
        memory_object_ref_errors,
    )
    supersession_event = validate(
        EXAMPLES / "audit_event.supersession.example.json",
        memory_validator,
        memory_object_ref_errors,
    )
    retraction_event = validate(
        EXAMPLES / "audit_event.retraction.example.json",
        memory_validator,
        memory_object_ref_errors,
    )
    lifecycle_thread = validate(EXAMPLES / "provenance_thread.lifecycle.example.json", thread_validator)

    objects = {
        item["id"]: item
        for item in (
            anchor,
            superseded_claim,
            replacement_claim,
            retracted_claim,
            supersession_event,
            retraction_event,
        )
    }

    ensure(
        anchor["kind"] == "anchor" and anchor["lifecycle"]["review_state"] == "frozen",
        "anchor.example.json must be a frozen anchor",
    )
    ensure(
        superseded_claim["kind"] == "claim" and superseded_claim["lifecycle"]["review_state"] == "superseded",
        "claim.superseded.example.json must be a superseded claim",
    )
    ensure(
        replacement_claim["kind"] == "claim" and replacement_claim["lifecycle"]["review_state"] == "confirmed",
        "claim.current-entrypoint.example.json must be the confirmed replacement claim",
    )
    ensure(
        retracted_claim["kind"] == "claim" and retracted_claim["lifecycle"]["review_state"] == "retracted",
        "claim.retracted.example.json must be a retracted claim",
    )
    ensure(
        supersession_event["kind"] == "audit_event",
        "audit_event.supersession.example.json must be an audit_event",
    )
    ensure(
        retraction_event["kind"] == "audit_event",
        "audit_event.retraction.example.json must be an audit_event",
    )
    ensure(
        anchor["trust"]["temperature"] == "frozen",
        "anchor.example.json must keep trust.temperature at frozen",
    )
    ensure(
        "freeze_basis" in anchor["lifecycle"] and anchor["lifecycle"]["freeze_basis"]["qualifies_by"],
        "anchor.example.json must expose non-empty freeze_basis qualifiers",
    )
    ensure(
        anchor["lifecycle"]["current_recall"]["status"] == "preferred",
        "anchor.example.json must stay a preferred current recall surface",
    )

    thread_ids = set(lifecycle_thread["memory_object_ids"])
    for required_id in objects:
        if required_id == anchor["id"]:
            continue
        ensure(required_id in thread_ids, f"provenance_thread.lifecycle.example.json missing {required_id}")
    for referenced_id in thread_ids:
        ensure(
            referenced_id in objects,
            f"provenance_thread.lifecycle.example.json references unknown memory object {referenced_id}",
        )

    timeline_object_ids = {entry["object_id"] for entry in lifecycle_thread["timeline"] if "object_id" in entry}
    for required_id in objects:
        if required_id == anchor["id"]:
            continue
        ensure(required_id in timeline_object_ids, f"provenance_thread.lifecycle.example.json missing timeline entry for {required_id}")
    for referenced_id in timeline_object_ids:
        ensure(
            referenced_id in objects,
            f"provenance_thread.lifecycle.example.json timeline points to unknown memory object {referenced_id}",
        )

    for item in objects.values():
        if item["id"] == anchor["id"]:
            continue
        ensure(
            item["provenance"]["provenance_thread_id"] == lifecycle_thread["id"],
            f"{item['id']} must point to lifecycle provenance thread",
        )
        for episode_ref in item["provenance"].get("episode_refs", []):
            ensure(episode_ref in objects, f"{item['id']} provenance.episode_refs points to unknown object {episode_ref}")
        for supersedes_ref in item["lifecycle"].get("supersedes", []):
            ensure(supersedes_ref in objects, f"{item['id']} lifecycle.supersedes points to unknown object {supersedes_ref}")
        superseded_by = item["lifecycle"].get("superseded_by")
        if superseded_by is not None:
            ensure(
                superseded_by in objects,
                f"{item['id']} lifecycle.superseded_by points to unknown object {superseded_by}",
            )

    ensure(
        superseded_claim["lifecycle"]["superseded_by"] == replacement_claim["id"],
        "superseded claim must point to the replacement claim",
    )
    ensure(
        superseded_claim["lifecycle"]["current_recall"]["status"] == "historical",
        "superseded claim must keep historical current_recall posture",
    )
    ensure(
        superseded_claim["lifecycle"]["current_recall"]["replacement_ref"] == replacement_claim["id"],
        "superseded claim current_recall.replacement_ref must point to the replacement claim",
    )
    ensure(
        superseded_claim["id"] in replacement_claim["lifecycle"]["supersedes"],
        "replacement claim must record which claim it supersedes",
    )
    ensure(
        replacement_claim["lifecycle"]["current_recall"]["status"] == "preferred",
        "replacement claim must stay the preferred current recall surface",
    )
    ensure(
        retracted_claim["lifecycle"]["current_recall"]["status"] == "withdrawn",
        "retracted claim must keep withdrawn current_recall posture",
    )
    ensure(
        retracted_claim["id"] in replacement_claim["lifecycle"]["current_recall"].get("contradiction_refs", []),
        "replacement claim must keep a contradiction ref to the retracted claim",
    )
    ensure(
        replacement_claim["id"] in retracted_claim["lifecycle"]["current_recall"].get("contradiction_refs", []),
        "retracted claim must keep a contradiction ref back to the replacement claim",
    )

    print("Lifecycle and audit examples validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
