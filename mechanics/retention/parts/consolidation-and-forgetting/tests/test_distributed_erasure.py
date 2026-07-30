from __future__ import annotations

import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker


PART_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = PART_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from distributed_erasure import (  # noqa: E402
    RACE_REBUILD_REQUIRED,
    SURFACE_CLASSES,
    SURFACE_MATERIALS,
    ZERO_DIGEST,
    build_erasure_recovery_probe,
    evaluate_distributed_erasure_closure,
    normalized_digest,
    validate_erasure_recovery_probe,
)


SCHEMA = (
    PART_ROOT
    / "schemas"
    / "active_organ_erasure_recovery_probe_v0.schema.json"
)


def owner(surface_id: str) -> str:
    return {
        "ER0": "aoa-memo-er0",
        "ER1": "aoa-session-memory-er1",
        "ER2": "aoa-session-memory-er2",
        "ER3": "aoa-kag-er3",
        "ER4": "abyss-stack-er4",
        "ER5": "abyss-stack-er5",
        "ER6": "abyss-machine",
        "ER7": "aoa-evals-er7",
        "ER8": "synthetic-model-owner-er8",
        "ER9": "aoa-memo-er9",
    }[surface_id]


def fixture() -> dict:
    manifest_id = "erase-manifest:phase11:complete"
    work_items = []
    receipts = []
    extensions = {}
    probes = {}
    surfaces = []
    owner_results = []
    for surface_id, surface_class in SURFACE_CLASSES.items():
        worker = owner(surface_id)
        work_ref = f"erase-work:phase11:{surface_id}"
        receipt_ref = f"erase-receipt:phase11:{surface_id}"
        probe_ref = f"erase-probe:phase11:{surface_id}"
        extension_ref = f"erase-extension:phase11:{surface_id}"
        extension = {
            "schema_version": "active_organ_owner_erasure_extension_v0",
            "extension_id": extension_ref,
            "parent_owner": worker.rsplit("-", 1)[0],
            "worker_owner": worker,
            "surface_id": surface_id,
            "work_item_ref": work_ref,
            "material_classes": sorted(SURFACE_MATERIALS[surface_id]),
            "target_ref_digests": ["sha256:" + ("1" * 64)],
            "operation_evidence_refs": [
                f"operation-evidence:phase11:{surface_id}"
            ],
            "recovery_probe_ref": probe_ref,
            "result": "erased",
            "residue_refs": [],
            "retention_exceptions": [],
            "subject_material_included": False,
            "content_minimized": True,
            "execution_posture": "reference_lab_only",
            "live_execution": False,
            "effect_authority": "owner_local_erasure_only",
            "global_completion_authority": False,
            "content_digest": ZERO_DIGEST,
        }
        extension["content_digest"] = normalized_digest(extension)
        extensions[extension_ref] = extension
        probe = build_erasure_recovery_probe(
            probe_id=probe_ref,
            surface_id=surface_id,
            worker_owner=worker,
            work_item_ref=work_ref,
            canary_digest="sha256:" + ("2" * 64),
            positive_match_count=1,
            query_classes=["owner_native"],
            race_rebuild_required=surface_id in RACE_REBUILD_REQUIRED,
            race_rebuild_attempted=surface_id in RACE_REBUILD_REQUIRED,
            performed_at="2026-07-29T15:00:00Z",
        )
        probes[probe_ref] = probe
        pin = {
            "schema_ref": f"schema:phase11:{surface_id}",
            "schema_version": "0",
            "payload_ref": extension_ref,
            "payload_digest": extension["content_digest"],
        }
        work_items.append(
            {
                "contract_type": "per_owner_erase_work_item",
                "contract_id": "C16",
                "work_item_id": work_ref,
                "manifest_ref": manifest_id,
                "target_owner": worker,
                "erase_surface_id": surface_id,
                "owner_extension": pin,
            }
        )
        receipts.append(
            {
                "contract_type": "erase_completion_or_residue_receipt",
                "contract_id": "C17",
                "receipt_id": receipt_ref,
                "manifest_ref": manifest_id,
                "receipt_owner": worker,
                "work_item_ref": work_ref,
                "erase_surface_id": surface_id,
                "result": "erased",
                "residue_refs": [],
                "recovery_probe_refs": [probe_ref],
                "retention_exceptions": [],
                "owner_extension": pin,
            }
        )
        surfaces.append(
            {
                "surface_id": surface_id,
                "surface_class": surface_class,
                "owner": worker,
                "work_item_ref": work_ref,
                "surface_state": "erased",
                "retention_exceptions": [],
            }
        )
        owner_results.append(
            {
                "owner": worker,
                "work_item_ref": work_ref,
                "erase_receipt_ref": receipt_ref,
                "recovery_probe_ref": probe_ref,
                "result": "erased",
            }
        )
    request = {
        "contract_type": "memory_erase_request",
        "contract_id": "C14",
        "scope": {"erase_surface_ids": list(SURFACE_CLASSES)},
        "recovery_probe_required": True,
    }
    manifest = {
        "contract_type": "distributed_memory_erase_manifest",
        "contract_id": "C15",
        "manifest_id": manifest_id,
        "work_item_refs": [item["work_item_id"] for item in work_items],
        "erase_receipt_refs": [item["receipt_id"] for item in receipts],
        "erase_surfaces": surfaces,
        "owner_results": owner_results,
        "completion_state": "complete",
    }
    return {
        "request": request,
        "manifest": manifest,
        "work_items": work_items,
        "receipts": receipts,
        "owner_extensions": extensions,
        "probes": probes,
    }


def evaluate(data: dict) -> dict:
    return evaluate_distributed_erasure_closure(**data)


def test_recovery_probe_schema_and_semantics_are_content_minimized() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    probe = next(iter(fixture()["probes"].values()))

    assert list(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(probe)
    ) == []
    assert validate_erasure_recovery_probe(probe) == []
    assert probe["probe_storage"]["subject_material_included"] is False
    assert probe["global_completion_authority"] is False


def test_complete_er0_er9_closure_is_walkable_and_probe_gated() -> None:
    verdict = evaluate(fixture())

    assert verdict["issues"] == []
    assert verdict["walkable"] is True
    assert verdict["all_surfaces_covered"] is True
    assert verdict["every_probe_passed"] is True
    assert verdict["plain_complete"] is True
    assert verdict["private_memory_deployment_allowed"] is True
    assert verdict["live_execution"] is False


def test_missing_probe_or_unlearning_residue_blocks_private_deployment() -> None:
    missing_probe = fixture()
    missing_probe["probes"].pop("erase-probe:phase11:ER3")
    verdict = evaluate(missing_probe)
    assert verdict["plain_complete"] is False
    assert verdict["private_memory_deployment_allowed"] is False
    assert any("ER3 recovery probe is not resolvable" in issue for issue in verdict["issues"])

    residue = fixture()
    receipt = next(
        item for item in residue["receipts"] if item["erase_surface_id"] == "ER8"
    )
    surface = next(
        item
        for item in residue["manifest"]["erase_surfaces"]
        if item["surface_id"] == "ER8"
    )
    extension = residue["owner_extensions"][
        "erase-extension:phase11:ER8"
    ]
    exception = {
        "exception_id": "exception:phase11:unlearning-obligation",
        "decision_ref": "decision:operator:phase11:unlearning-obligation",
        "reason": "synthetic model owner unavailable",
    }
    receipt.update(
        {
            "result": "residue",
            "residue_refs": ["residue:phase11:unlearning-obligation"],
            "retention_exceptions": [exception],
        }
    )
    extension.update(
        {
            "result": "residue",
            "residue_refs": ["residue:phase11:unlearning-obligation"],
            "retention_exceptions": [exception],
            "content_digest": ZERO_DIGEST,
        }
    )
    extension["content_digest"] = normalized_digest(extension)
    receipt["owner_extension"]["payload_digest"] = extension["content_digest"]
    work = next(
        item for item in residue["work_items"] if item["erase_surface_id"] == "ER8"
    )
    work["owner_extension"]["payload_digest"] = extension["content_digest"]
    surface.update(
        {
            "surface_state": "residue",
            "retention_exceptions": [exception],
        }
    )
    owner_result = next(
        item
        for item in residue["manifest"]["owner_results"]
        if item["owner"] == owner("ER8")
    )
    owner_result["result"] = "residue"
    residue["manifest"]["completion_state"] = "complete_with_approved_exceptions"

    verdict = evaluate(residue)
    assert verdict["residue_present"] is True
    assert verdict["exceptions_present"] is True
    assert verdict["plain_complete"] is False
    assert verdict["private_memory_deployment_allowed"] is False
