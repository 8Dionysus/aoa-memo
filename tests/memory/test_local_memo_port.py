from __future__ import annotations

import copy
import importlib.util
import json
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
    spec.loader.exec_module(module)
    return module


validate_local_memo_port = load_script(
    "validate_local_memo_port",
    REPO_ROOT / "scripts" / "memory" / "validate_local_memo_port.py",
)
build_local_memo_port_index = load_script(
    "build_local_memo_port_index",
    REPO_ROOT / "scripts" / "memory" / "build_local_memo_port_index.py",
)
build_memo_port_vocabulary = load_script(
    "build_memo_port_vocabulary",
    REPO_ROOT / "scripts" / "memory" / "build_memo_port_vocabulary.py",
)


EXAMPLE_PORT = REPO_ROOT / "examples" / "memory-ports" / "example-port"


def test_local_memo_port_example_validates() -> None:
    assert validate_local_memo_port.validate_port(EXAMPLE_PORT) == []


def test_local_memo_port_index_is_stable() -> None:
    index = validate_local_memo_port.build_index(EXAMPLE_PORT)
    index_path = EXAMPLE_PORT / "index.min.json"
    assert validate_local_memo_port.render_json(index) == index_path.read_text(encoding="utf-8")
    markdown = build_local_memo_port_index.render_markdown(index)
    assert markdown == (EXAMPLE_PORT / "INDEX.md").read_text(encoding="utf-8")
    assert "## Agent Route" in markdown
    assert "## Validate" not in markdown


def test_memo_port_vocabulary_is_stable() -> None:
    generated = REPO_ROOT / "generated" / "memory" / "memo_port_vocabulary.min.json"
    assert build_memo_port_vocabulary.render() == generated.read_text(encoding="utf-8")


def test_unreviewed_candidate_cannot_claim_current_lifecycle(monkeypatch) -> None:
    candidate = EXAMPLE_PORT / "candidates" / "20260520T171200Z.codex-plane-memory-route.candidate.json"
    payload = json.loads(candidate.read_text(encoding="utf-8"))
    payload = copy.deepcopy(payload)
    payload["lifecycle"] = "current"
    original_load_json = validate_local_memo_port.load_json

    def fake_load_json(path: Path):
        if Path(path) == candidate:
            return copy.deepcopy(payload)
        return original_load_json(path)

    monkeypatch.setattr(validate_local_memo_port, "load_json", fake_load_json)

    errors = validate_local_memo_port.validate_port(EXAMPLE_PORT)
    assert any("must not claim lifecycle" in error for error in errors)


def test_unknown_vocabulary_term_is_rejected(monkeypatch) -> None:
    candidate = EXAMPLE_PORT / "candidates" / "20260520T171200Z.codex-plane-memory-route.candidate.json"
    payload = json.loads(candidate.read_text(encoding="utf-8"))
    payload = copy.deepcopy(payload)
    payload["family"] = "private-taxonomy"
    original_load_json = validate_local_memo_port.load_json

    def fake_load_json(path: Path):
        if Path(path) == candidate:
            return copy.deepcopy(payload)
        return original_load_json(path)

    monkeypatch.setattr(validate_local_memo_port, "load_json", fake_load_json)

    errors = validate_local_memo_port.validate_port(EXAMPLE_PORT)
    assert any("unknown vocabulary term" in error for error in errors)


def test_blank_ref_after_trimming_is_rejected(monkeypatch) -> None:
    export = EXAMPLE_PORT / "exports" / "20260520T172000Z.codex-plane-memory-route.aoa-memo-intake.json"
    payload = json.loads(export.read_text(encoding="utf-8"))
    payload = copy.deepcopy(payload)
    payload["source_refs"] = ["   "]
    original_load_json = validate_local_memo_port.load_json

    def fake_load_json(path: Path):
        if Path(path) == export:
            return copy.deepcopy(payload)
        return original_load_json(path)

    monkeypatch.setattr(validate_local_memo_port, "load_json", fake_load_json)

    errors = validate_local_memo_port.validate_port(EXAMPLE_PORT)
    assert any("source_refs[0] must be a non-empty string" in error for error in errors)
