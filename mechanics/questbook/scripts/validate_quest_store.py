#!/usr/bin/env python3
from __future__ import annotations

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
                    validate_yaml(path, lane, state, problems)
                elif path.suffix == ".md":
                    validate_markdown(path, lane, state, problems)
                else:
                    problems.append(f"{rel(path)}: quest source must be YAML or Markdown")

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
