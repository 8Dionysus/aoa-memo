from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_phase_alpha_curated_thread_names_new_contradiction_evidence_refs() -> None:
    payload = json.loads(
        (REPO_ROOT / "examples" / "provenance_thread.phase-alpha-curated.example.json").read_text(
            encoding="utf-8"
        )
    )

    assert "repo:abyss-stack/Logs/phase-alpha/alpha-05-restartable-inquiry-loop/next_pass_brief.md" in payload[
        "source_refs"
    ]
    assert (
        "repo:abyss-stack/Logs/phase-alpha/alpha-06-validation-driven-remediation-recall-rerun/"
        "remediation_decision.json"
    ) in payload["source_refs"]
