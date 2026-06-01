from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "aoa_memo_spark_lane_registry_v1"
SCENARIO_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

REQUIRED_SCENARIO_FILES = (
    "README.md",
    "PROMPT.md",
    "templates/result.md",
    "templates/handoff.md",
    "examples/result.example.md",
)

REQUIRED_README_MARKERS = (
    "## Scope",
    "## Done Signal",
    "## Stop-line",
    "## Handoff Route",
)

REQUIRED_RESULT_MARKERS = (
    "Scenario:",
    "Status: done",
    "Scope:",
    "Files read:",
    "Findings:",
    "Changes made:",
    "Validation run:",
    "Skipped checks:",
    "Remaining risk:",
    "Next owner route:",
)

REQUIRED_HANDOFF_MARKERS = (
    "Scenario:",
    "Status: handoff",
    "Reason for handoff:",
    "Scope read:",
    "Findings:",
    "Files likely affected:",
    "Validation already run:",
    "Validation still needed:",
    "Stop-line:",
    "Suggested next prompt:",
)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validation_command_text(root: Path) -> str:
    lanes = root / "config" / "validation_lanes.json"
    if lanes.exists():
        return json.dumps(load_json(lanes), sort_keys=True)
    release_check = root / "scripts/release/release_check.py"
    if release_check.exists():
        return release_check.read_text(encoding="utf-8")
    return ""


def require_string(problems: list[str], where: str, value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        problems.append(f"{where} must be a non-empty string")


def require_string_list(problems: list[str], where: str, value: object) -> None:
    if not isinstance(value, list) or not value:
        problems.append(f"{where} must be a non-empty list")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            problems.append(f"{where}[{index}] must be a non-empty string")


def rel_exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def read_text(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8")


def require_markers(
    problems: list[str],
    root: Path,
    rel: str,
    markers: tuple[str, ...],
) -> None:
    path = root / rel
    if not path.is_file():
        problems.append(f"missing file: {rel}")
        return
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            problems.append(f"{rel} missing marker: {marker}")


def validate_scenario(root: Path, scenario: dict[str, Any], seen_ids: set[str]) -> list[str]:
    problems: list[str] = []
    scenario_id = scenario.get("scenario_id")
    where = f"scenarios[{scenario_id or '?'}]"

    for key in (
        "scenario_id",
        "role",
        "path",
        "prompt_ref",
        "result_template_ref",
        "handoff_template_ref",
        "result_example_ref",
        "done_signal",
        "stop_line",
    ):
        require_string(problems, f"{where}.{key}", scenario.get(key))
    require_string_list(problems, f"{where}.default_validation", scenario.get("default_validation"))

    if isinstance(scenario_id, str):
        if not SCENARIO_ID_RE.match(scenario_id):
            problems.append(f"{where}.scenario_id must be lowercase kebab-case")
        if scenario_id in seen_ids:
            problems.append(f"duplicate scenario_id: {scenario_id}")
        seen_ids.add(scenario_id)

    path = scenario.get("path")
    if isinstance(path, str):
        scenario_dir = root / path
        if not scenario_dir.is_dir():
            problems.append(f"{where}.path does not exist as directory: {path}")
        for rel in REQUIRED_SCENARIO_FILES:
            expected = f"{path}/{rel}"
            if not (root / expected).is_file():
                problems.append(f"{where} missing required scenario file: {expected}")

    for key in (
        "prompt_ref",
        "result_template_ref",
        "handoff_template_ref",
        "result_example_ref",
    ):
        value = scenario.get(key)
        if isinstance(value, str) and not (root / value).is_file():
            problems.append(f"{where}.{key} does not exist: {value}")

    if isinstance(path, str):
        require_markers(problems, root, f"{path}/README.md", REQUIRED_README_MARKERS)
    prompt_ref = scenario.get("prompt_ref")
    if isinstance(prompt_ref, str) and (root / prompt_ref).is_file():
        prompt = read_text(root, prompt_ref)
        if "done-or-handoff" not in prompt:
            problems.append(f"{prompt_ref} must mention done-or-handoff")

    result_ref = scenario.get("result_template_ref")
    if isinstance(result_ref, str):
        require_markers(problems, root, result_ref, REQUIRED_RESULT_MARKERS)
    handoff_ref = scenario.get("handoff_template_ref")
    if isinstance(handoff_ref, str):
        require_markers(problems, root, handoff_ref, REQUIRED_HANDOFF_MARKERS)
    example_ref = scenario.get("result_example_ref")
    if isinstance(example_ref, str):
        require_markers(problems, root, example_ref, REQUIRED_RESULT_MARKERS)

    return problems


def validate_packet_dir(
    root: Path,
    packet_dir: Path,
    required_markers: tuple[str, ...],
    scenario_ids: set[str],
) -> list[str]:
    problems: list[str] = []
    if not packet_dir.exists():
        return problems
    for path in sorted(packet_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        for marker in required_markers:
            if marker not in text:
                problems.append(f"{rel} missing marker: {marker}")
        scenario_line = next((line for line in text.splitlines() if line.startswith("Scenario:")), "")
        scenario_id = scenario_line.partition(":")[2].strip()
        if scenario_id and scenario_id not in scenario_ids:
            problems.append(f"{rel} names unknown scenario: {scenario_id}")
    return problems
