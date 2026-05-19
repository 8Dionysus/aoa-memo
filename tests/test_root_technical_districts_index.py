from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from root_technical_districts_common import DISTRICT_ORDER, GENERATED_PATH, build_index  # noqa: E402
from validate_root_technical_districts_index import validate  # noqa: E402


def test_root_technical_districts_index_is_valid() -> None:
    assert validate() == []


def test_root_technical_districts_index_matches_builder() -> None:
    payload = json.loads(GENERATED_PATH.read_text(encoding="utf-8"))

    assert payload == build_index()


def test_root_technical_districts_index_names_every_route_card() -> None:
    payload = json.loads(GENERATED_PATH.read_text(encoding="utf-8"))

    assert payload["district_order"] == list(DISTRICT_ORDER)
    for district in DISTRICT_ORDER:
        entry = payload["districts"][district]
        assert entry["path"] == f"{district}/"
        assert (REPO_ROOT / entry["route_card"]).is_file()
        assert entry["root_role"]
        assert entry["use_for"]
        assert entry["route_local_to"]
        assert entry["check"]


def test_root_technical_districts_index_preserves_compact_counts() -> None:
    payload = json.loads(GENERATED_PATH.read_text(encoding="utf-8"))
    config = json.loads((REPO_ROOT / "config" / "root_technical_districts.json").read_text())

    assert payload["counts"]["districts"] == len(DISTRICT_ORDER)
    assert payload["counts"]["allowed_files"] == sum(
        len(config["districts"][district]["allowed_files"]) for district in DISTRICT_ORDER
    )
    for district in DISTRICT_ORDER:
        assert payload["districts"][district]["allowed_count"] == len(
            config["districts"][district]["allowed_files"]
        )
