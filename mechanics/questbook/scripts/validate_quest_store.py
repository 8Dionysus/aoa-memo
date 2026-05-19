#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
QUESTS = ROOT / "quests"

LIFECYCLE_STATES = {
    "captured",
    "triaged",
    "ready",
    "active",
    "blocked",
    "reanchor",
    "done",
    "dropped",
}
ALLOWED_LANES = {"memo", "agon"}
ROOT_ALLOWED_FILES = {"AGENTS.md", "README.md"}
MARKDOWN_CONTRACT = "source_contract: memo_quest_markdown_contract_v1"
REQUIRED_MARKDOWN_HEADINGS = (
    "## Quest",
    "## Owner Route",
    "## Next Action",
    "## Acceptance Evidence",
    "## Stop-lines",
)
QUEST_GENERATED_OUTPUTS = (
    "generated/quest_catalog.min.example.json",
    "generated/quest_catalog.min.json",
    "generated/quest_dispatch.min.example.json",
    "generated/quest_dispatch.min.json",
)
QUEST_GENERATED_BUILDER = "mechanics/questbook/scripts/build_quest_surfaces.py"
GENERATED_VIEWS_PART_FILES = (
    "mechanics/questbook/parts/generated-views/README.md",
    "mechanics/questbook/parts/generated-views/CONTRACT.md",
    "mechanics/questbook/parts/generated-views/VALIDATION.md",
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def quest_id_lane(quest_id: str) -> str | None:
    if quest_id.startswith("AOA-MEM-Q-"):
        return "memo"
    if quest_id.startswith(("AOM-Q-AGON-", "AOMEMO-Q-AGON-")):
        return "agon"
    return None


def markdown_sections(text: str) -> set[str]:
    return {line.strip() for line in text.splitlines() if line.startswith("## ")}


def validate_yaml(path: Path, lane: str, state: str, problems: list[str]) -> None:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validation context
        problems.append(f"{rel(path)}: cannot parse YAML: {exc}")
        return
    if not isinstance(payload, dict):
        problems.append(f"{rel(path)}: YAML quest must be an object")
        return
    quest_id = str(payload.get("id") or "")
    if quest_id != path.stem:
        problems.append(f"{rel(path)}: id must match filename stem")
    if quest_id_lane(quest_id) != lane:
        problems.append(f"{rel(path)}: id prefix must route to lane {lane}")
    if payload.get("state") != state:
        problems.append(f"{rel(path)}: state must match lifecycle directory {state}")
    if payload.get("public_safe") is not True:
        problems.append(f"{rel(path)}: public_safe must be true")


def validate_markdown(path: Path, lane: str, state: str, problems: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if lane != "agon":
        problems.append(f"{rel(path)}: Markdown quest sources are currently only supported for agon")
    if quest_id_lane(path.stem) != lane:
        problems.append(f"{rel(path)}: id prefix must route to lane {lane}")
    if state not in {"ready", "active", "blocked", "reanchor", "done", "dropped"}:
        problems.append(f"{rel(path)}: Markdown follow-through must not stay in unshaped state {state}")
    if not text.startswith("# "):
        problems.append(f"{rel(path)}: Markdown quest must start with an H1")
    if MARKDOWN_CONTRACT not in text:
        problems.append(f"{rel(path)}: missing {MARKDOWN_CONTRACT}")
    sections = markdown_sections(text)
    for heading in REQUIRED_MARKDOWN_HEADINGS:
        if heading not in sections:
            problems.append(f"{rel(path)}: missing {heading}")


def validate_generated_views_part(problems: list[str]) -> None:
    part_text = ""
    for part_file in GENERATED_VIEWS_PART_FILES:
        path = ROOT / part_file
        if not path.is_file():
            problems.append(f"{part_file}: generated-views part file is required")
            continue
        part_text += "\n" + path.read_text(encoding="utf-8")

    if part_text:
        for output in QUEST_GENERATED_OUTPUTS:
            if output not in part_text:
                problems.append(f"mechanics/questbook/parts/generated-views: missing output {output}")
        if QUEST_GENERATED_BUILDER not in part_text:
            problems.append(
                "mechanics/questbook/parts/generated-views: missing Questbook surface builder"
            )
        for forbidden in (
            "proof or closure verdict",
            "route dispatch authority",
            "runtime scheduling or live state",
            "owner acceptance",
            "private memory",
        ):
            if forbidden not in part_text:
                problems.append(
                    "mechanics/questbook/parts/generated-views: missing stop-line "
                    f"{forbidden!r}"
                )

    config_path = ROOT / "config" / "root_technical_districts.json"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validation context
        problems.append(f"{rel(config_path)}: cannot parse root technical districts: {exc}")
        return

    generated_allowed = set(config.get("districts", {}).get("generated", {}).get("allowed_files", []))
    missing_allowed = sorted(set(QUEST_GENERATED_OUTPUTS) - generated_allowed)
    for output in missing_allowed:
        problems.append(f"config/root_technical_districts.json: generated allowlist missing {output}")

    families = config.get("generated_families", [])
    family = next(
        (
            item
            for item in families
            if isinstance(item, dict) and item.get("id") == "questbook_projections"
        ),
        None,
    )
    if not isinstance(family, dict):
        problems.append("config/root_technical_districts.json: missing questbook_projections family")
        return

    if family.get("source_kind") != "projection":
        problems.append("questbook_projections family source_kind must be projection")
    if family.get("owner_surface") != "mechanics/questbook/README.md":
        problems.append("questbook_projections family owner_surface must be mechanics/questbook/README.md")
    if tuple(family.get("outputs", [])) != QUEST_GENERATED_OUTPUTS:
        problems.append("questbook_projections family outputs must match required Questbook outputs")
    if family.get("builders") != [QUEST_GENERATED_BUILDER]:
        problems.append("questbook_projections family builders must name the Questbook surface builder")


def validate() -> list[str]:
    problems: list[str] = []
    if not (QUESTS / "AGENTS.md").is_file():
        problems.append("quests/AGENTS.md is required")
    if not (QUESTS / "README.md").is_file():
        problems.append("quests/README.md is required")

    for child in sorted(QUESTS.iterdir()):
        if child.is_file() and child.name not in ROOT_ALLOWED_FILES:
            problems.append(f"{rel(child)}: quest source must live under quests/<lane>/<state>/")
        if not child.is_dir():
            continue
        lane = child.name
        if lane not in ALLOWED_LANES:
            problems.append(f"{rel(child)}: unsupported quest lane")
            continue
        if not (child / "README.md").is_file():
            problems.append(f"{rel(child / 'README.md')}: lane README is required")
        for path in sorted(item for item in child.iterdir() if item.is_file()):
            if path.name != "README.md":
                problems.append(f"{rel(path)}: lane root may only contain README.md")
        for state_dir in sorted(path for path in child.iterdir() if path.is_dir()):
            state = state_dir.name
            if state not in LIFECYCLE_STATES:
                problems.append(f"{rel(state_dir)}: unsupported lifecycle state")
                continue
            for path in sorted(state_dir.iterdir()):
                if not path.is_file():
                    continue
                if path.suffix == ".yaml":
                    if lane == "agon":
                        problems.append(f"{rel(path)}: agon quest sources must be Markdown, not YAML")
                    else:
                        validate_yaml(path, lane, state, problems)
                elif path.suffix == ".md":
                    validate_markdown(path, lane, state, problems)
                else:
                    problems.append(f"{rel(path)}: quest source must be YAML or Markdown")

    validate_generated_views_part(problems)
    return problems


def main() -> int:
    problems = validate()
    if problems:
        print("Quest store validation failed:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1
    print("[ok] memo quest store is lane-first and source-contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
