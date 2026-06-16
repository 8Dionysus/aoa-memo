from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_ROOT = REPO_ROOT / "scripts" / "memory"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


landing = load_script(
    "land_reviewed_memo_intake",
    REPO_ROOT / "scripts" / "memory" / "land_reviewed_memo_intake.py",
)


EXAMPLE_PORT = REPO_ROOT / "examples" / "memory-ports" / "example-port"
EXPORT_REF = "exports/20260520T172000Z.codex-plane-memory-route.aoa-memo-intake.json"


def copy_reviewed_write_port(tmp_path: Path) -> Path:
    port = tmp_path / "example-port"
    shutil.copytree(EXAMPLE_PORT, port)
    repo_docs = tmp_path / "docs" / "memory"
    repo_docs.mkdir(parents=True)
    for name in ("LOCAL_MEMO_PORT_STANDARD.md", "MEMO_PORT_INDEXING_VOCABULARY.md"):
        source = REPO_ROOT / "docs" / "memory" / name
        (repo_docs / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    source_example_dir = tmp_path / "examples" / "memory-ports" / "example-port"
    source_example_dir.mkdir(parents=True)
    shutil.copy2(port / "PORT.yaml", source_example_dir / "PORT.yaml")
    export_path = port / EXPORT_REF
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["allowed_result"] = "reviewed_write"
    payload["notes"] = "Reviewed-write fixture for aoa-memo corpus landing tests."
    export_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return port


def add_second_candidate(port: Path) -> str:
    candidate_name = "20260520T171201Z.codex-plane-memory-route-extra.candidate.json"
    original_path = port / "candidates" / "20260520T171200Z.codex-plane-memory-route.candidate.json"
    candidate_path = port / "candidates" / candidate_name
    payload = json.loads(original_path.read_text(encoding="utf-8"))
    payload["id"] = "candidate:example-repo:20260520T171201Z:codex-plane-memory-route-extra"
    payload["claim"] = "A second reviewed-intake candidate must be covered by its own successful receipt."
    payload["created_at"] = "2026-05-20T17:12:01Z"
    candidate_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return f"candidates/{candidate_name}"


def test_reviewed_write_export_lands_as_corpus_bundle(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    output_root = tmp_path / "aoa-memo"

    inputs = landing.load_landing_inputs(port, EXPORT_REF)
    plan = landing.build_landing_plan(
        inputs,
        output_root=output_root,
        object_kind="decision",
        slug="example-reviewed-intake",
        reviewed_at="2026-05-22T01:23:45Z",
        reviewed_by="test-suite",
    )
    landing.write_landing_plan(plan, output_root=output_root)

    object_path = output_root / "memo" / "objects" / "decisions" / "2026" / "example-reviewed-intake" / "object.json"
    memo_path = object_path.with_name("MEMO.md")
    receipt_path = output_root / "memo" / "intake" / "receipts" / "20260522T012345Z.example-repo.example-reviewed-intake.landing-receipt.json"
    copied_intake_path = output_root / "memo" / "intake" / "reviewed" / "example-repo.20260520T172000Z.codex-plane-memory-route.aoa-memo-intake.json"

    assert object_path.is_file()
    assert memo_path.is_file()
    assert receipt_path.is_file()
    assert copied_intake_path.is_file()

    memory_object = json.loads(object_path.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

    assert memory_object["id"] == "memo.decision.2026-05-22.example-reviewed-intake"
    assert memory_object["payload_ref"] == "memo/intake/reviewed/example-repo.20260520T172000Z.codex-plane-memory-route.aoa-memo-intake.json"
    assert memory_object["lifecycle"]["review_state"] == "confirmed"
    assert memory_object["lifecycle"]["current_recall"]["status"] == "allowed"
    assert "repo:example-repo/memo/candidates/20260520T171200Z.codex-plane-memory-route.candidate.json" in memory_object["provenance"]["source_refs"]
    assert all(
        ref.startswith("repo:") or ref.startswith("memo/intake/")
        for ref in memory_object["provenance"]["source_refs"]
    )

    assert receipt["schema"] == "aoa_memo_reviewed_intake_landing_receipt_v1"
    assert receipt["result"] == "landed"
    assert receipt["object_ref"] == memory_object["id"]
    assert receipt["object_path"] == "memo/objects/decisions/2026/example-reviewed-intake/object.json"
    assert "export_evidence_refs" in receipt["checks"]
    assert "candidate_source_refs" in receipt["checks"]
    assert "receipt_candidate_ref" in receipt["checks"]

    assert landing.object_schema_errors(memory_object, "memory_object.schema.json") == []
    assert landing.object_schema_errors(memory_object, "decision.schema.json") == []
    assert landing.support_schema_errors(receipt, "reviewed_intake_landing_receipt.schema.json") == []


def test_candidate_only_export_cannot_land() -> None:
    try:
        landing.load_landing_inputs(EXAMPLE_PORT, EXPORT_REF)
    except landing.LandingError as exc:
        assert "allowed_result must be 'reviewed_write'" in str(exc)
    else:
        raise AssertionError("candidate_only export unexpectedly loaded as landable input")


def test_packet_refs_must_stay_inside_port(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    export_path = port / EXPORT_REF
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload = copy.deepcopy(payload)
    payload["candidate_refs"] = ["../outside.candidate.json"]
    export_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    try:
        landing.load_landing_inputs(port, EXPORT_REF)
    except landing.LandingError as exc:
        assert "must stay under" in str(exc)
    else:
        raise AssertionError("outside packet ref unexpectedly accepted")


def test_export_source_ref_rejects_absolute_path(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    outside = tmp_path / "outside-source.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    export_path = port / EXPORT_REF
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["source_refs"] = [str(outside)]
    export_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    try:
        landing.load_landing_inputs(port, EXPORT_REF)
    except landing.LandingError as exc:
        assert "source_refs[0] local refs must be relative or symbolic" in str(exc)
    else:
        raise AssertionError("absolute source ref unexpectedly accepted")


def test_export_evidence_ref_rejects_parent_traversal(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    outside = tmp_path / "outside-evidence.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    export_path = port / EXPORT_REF
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["evidence_refs"] = ["../outside-evidence.md"]
    export_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    try:
        landing.load_landing_inputs(port, EXPORT_REF)
    except landing.LandingError as exc:
        assert "evidence_refs[0] local refs must not use '..' traversal" in str(exc)
    else:
        raise AssertionError("traversing evidence ref unexpectedly accepted")


def test_missing_export_evidence_blocks_corpus_landing(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    export_path = port / EXPORT_REF
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["evidence_refs"] = ["docs/memory/MISSING_EVIDENCE.md"]
    export_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    try:
        landing.load_landing_inputs(port, EXPORT_REF)
    except landing.LandingError as exc:
        assert "evidence_refs[0] points to missing ref docs/memory/MISSING_EVIDENCE.md" in str(exc)
    else:
        raise AssertionError("export with missing evidence unexpectedly loaded as landable input")


def test_missing_candidate_source_blocks_corpus_landing(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    candidate_path = port / "candidates" / "20260520T171200Z.codex-plane-memory-route.candidate.json"
    payload = json.loads(candidate_path.read_text(encoding="utf-8"))
    payload["source_refs"] = ["docs/memory/MISSING_SOURCE.md"]
    candidate_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    try:
        landing.load_landing_inputs(port, EXPORT_REF)
    except landing.LandingError as exc:
        assert "source_refs[0] points to missing ref docs/memory/MISSING_SOURCE.md" in str(exc)
    else:
        raise AssertionError("candidate with missing source unexpectedly loaded as landable input")


def test_untrusted_candidate_blocks_corpus_landing(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    candidate_path = port / "candidates" / "20260520T171200Z.codex-plane-memory-route.candidate.json"
    payload = json.loads(candidate_path.read_text(encoding="utf-8"))
    payload["source_trust"] = "untrusted"
    candidate_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    try:
        landing.load_landing_inputs(port, EXPORT_REF)
    except landing.LandingError as exc:
        assert "source_trust 'untrusted' blocks corpus landing" in str(exc)
    else:
        raise AssertionError("untrusted candidate unexpectedly loaded as landable input")


def test_reviewed_write_requires_receipt_ref(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    export_path = port / EXPORT_REF
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["receipt_refs"] = []
    export_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    try:
        landing.load_landing_inputs(port, EXPORT_REF)
    except landing.LandingError as exc:
        assert "reviewed_write landing requires at least one receipt_ref" in str(exc)
    else:
        raise AssertionError("reviewed_write export without receipt unexpectedly loaded")


def test_reviewed_write_requires_receipt_for_each_candidate(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    second_ref = add_second_candidate(port)
    export_path = port / EXPORT_REF
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["candidate_refs"].append(second_ref)
    export_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    try:
        landing.load_landing_inputs(port, EXPORT_REF)
    except landing.LandingError as exc:
        assert f"missing successful receipt for candidate_ref {second_ref}" in str(exc)
    else:
        raise AssertionError("multi-candidate export with missing receipt unexpectedly loaded")


def test_reviewed_write_rejects_receipt_for_unexported_candidate(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    second_ref = add_second_candidate(port)
    receipt_path = port / "receipts" / "20260520T171500Z.codex-plane-memory-route.validation-receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["candidate_ref"] = second_ref
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    try:
        landing.load_landing_inputs(port, EXPORT_REF)
    except landing.LandingError as exc:
        message = str(exc)
        assert f"{receipt_path}: candidate_ref {second_ref} is not listed in export candidate_refs" in message
        assert "missing successful receipt for candidate_ref candidates/20260520T171200Z.codex-plane-memory-route.candidate.json" in message
    else:
        raise AssertionError("receipt for unexported candidate unexpectedly authorized landing")


def test_reviewed_write_rejects_symbolic_receipt_candidate_ref(tmp_path: Path) -> None:
    port = copy_reviewed_write_port(tmp_path)
    receipt_name = "20260520T171501Z.codex-plane-memory-route.symbolic-receipt.json"
    original_path = port / "receipts" / "20260520T171500Z.codex-plane-memory-route.validation-receipt.json"
    receipt_path = port / "receipts" / receipt_name
    receipt = json.loads(original_path.read_text(encoding="utf-8"))
    receipt["id"] = "receipt:example-repo:20260520T171501Z:codex-plane-memory-route-symbolic"
    receipt["candidate_ref"] = "candidate:example-repo:20260520T171200Z:codex-plane-memory-route"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    export_path = port / EXPORT_REF
    payload = json.loads(export_path.read_text(encoding="utf-8"))
    payload["receipt_refs"].append(f"receipts/{receipt_name}")
    export_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    try:
        landing.load_landing_inputs(port, EXPORT_REF)
    except landing.LandingError as exc:
        message = str(exc)
        assert f"{receipt_path}: receipt candidate_ref must be a local packet ref" in message
    else:
        raise AssertionError("symbolic receipt candidate_ref was silently ignored")
