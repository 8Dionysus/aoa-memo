from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

import validate_memo


def load_json(relative_path: str) -> object:
    return json.loads((REPO_ROOT / relative_path).read_text(encoding="utf-8"))


def test_lineage_chain_validation_allows_strongest_available_partial_chain() -> None:
    errors: list[str] = []

    validate_memo.append_lineage_chain_errors(
        errors,
        {
            "cluster_ref": "cluster:checkpoint:session-growth-cycle",
            "candidate_ref": "candidate:aoa-playbooks:session-growth-cycle",
            "seed_ref": None,
            "object_ref": None,
        },
    )

    assert errors == []


def test_lineage_chain_validation_rejects_skipped_upstream_refs() -> None:
    errors: list[str] = []

    validate_memo.append_lineage_chain_errors(
        errors,
        {
            "cluster_ref": "cluster:checkpoint:session-growth-cycle",
            "candidate_ref": None,
            "seed_ref": "seed:aoa:session-growth-cycle",
            "object_ref": None,
        },
    )

    assert errors == [
        "lineage_refs.seed_ref requires lineage_refs.candidate_ref when later chain links are present"
    ]


def test_growth_refinery_writeback_doc_keeps_bounded_lineage_rules() -> None:
    doc = (REPO_ROOT / "docs" / "GROWTH_REFINERY_WRITEBACK.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    assert "preserve the strongest available chain in" in doc
    assert "mint `candidate_ref`, `seed_ref`, or `object_ref`" in doc
    assert "This context helps memory explain why a lesson mattered." in doc
    assert (
        "It does not override owner-local receipts, seed truth, landed object truth, or proof."
        in normalized
    )
    assert "Do not use lineage-aware memo recall as first authority" in doc


def test_growth_refinery_writeback_doc_maps_prune_cases_to_existing_memo_kinds() -> None:
    doc = (REPO_ROOT / "docs" / "GROWTH_REFINERY_WRITEBACK.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    assert "repeated drop, wrong-owner, or weak-owner supersession belongs in" in normalized
    assert "repeated reanchor, merge, or proof-first rescue belongs in" in normalized
    assert "seed staging repeatedly adds no value compared with direct owner landing" in normalized
    assert "let prune writeback become the first record of drop, merge, or supersession truth" in normalized
    assert "let memory decide whether a candidate should be dropped, merged, or superseded" in normalized


def test_failure_lesson_lineage_example_keeps_partial_chain_and_explanatory_note() -> None:
    example = load_json("examples/failure_lesson_memory.lineage.example.json")

    assert isinstance(example, dict)
    assert example["lineage_refs"] == {
        "cluster_ref": "cluster:checkpoint:session-growth-cycle",
        "candidate_ref": "candidate:aoa-playbooks:session-growth-cycle",
        "seed_ref": None,
        "object_ref": None,
    }
    assert example["lineage_context"]["status_posture"] == "reanchor"
    assert "Lineage refs are recall support only." in example["notes"]
    assert "Final owner truth stays with reviewed owner-local receipts" in example["notes"]


def test_recovery_pattern_lineage_example_keeps_full_chain_and_review_first_recall() -> None:
    example = load_json("examples/recovery_pattern_memory.lineage.example.json")

    assert isinstance(example, dict)
    assert example["lineage_refs"] == {
        "cluster_ref": "cluster:checkpoint:session-growth-cycle",
        "candidate_ref": "candidate:aoa-playbooks:session-growth-cycle",
        "seed_ref": "seed:aoa:session-growth-cycle",
        "object_ref": "playbook:AOA-P-0025",
    }
    assert example["lineage_context"]["status_posture"] == "stable"
    assert "bounded recall only after checking the linked owner receipt" in example["recall_posture"]
    assert "Memo preserves the bounded recovery pattern" in example["notes"]
