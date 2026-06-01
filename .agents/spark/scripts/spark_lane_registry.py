from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from spark_lane_contracts import (
    REQUIRED_HANDOFF_MARKERS,
    REQUIRED_RESULT_MARKERS,
    SCHEMA_VERSION,
    load_json,
    rel_exists,
    require_string,
    require_string_list,
    validate_packet_dir,
    validate_scenario,
    validation_command_text,
)


REGISTRY_PATH = Path(".agents/spark/registry.json")


def validate(root: Path) -> list[str]:
    problems: list[str] = []
    registry_path = root / REGISTRY_PATH
    if not registry_path.exists():
        return [f"missing Spark registry: {REGISTRY_PATH}"]

    try:
        registry = load_json(registry_path)
    except json.JSONDecodeError as exc:
        return [f"{REGISTRY_PATH} is not valid JSON: {exc}"]

    if not isinstance(registry, dict):
        return [f"{REGISTRY_PATH} must be a JSON object"]

    if registry.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"schema_version must be {SCHEMA_VERSION}")
    expected_refs = {
        "authority_ref": ".agents/spark/README.md",
        "agents_ref": ".agents/spark/AGENTS.md",
        "notebook_ref": ".agents/spark/SPARK_EXTRAPOLATION_NOTEBOOK.md",
        "swarm_ref": ".agents/spark/SWARM.md",
    }
    for key, expected in expected_refs.items():
        if registry.get(key) != expected:
            problems.append(f"{key} must be {expected}")
        if not rel_exists(root, expected):
            problems.append(f"{key} target does not exist: {expected}")

    storage_refs = registry.get("storage_refs")
    if not isinstance(storage_refs, dict):
        problems.append("storage_refs must be an object")
        storage_refs = {}
    for key in ("handoffs", "handoffs_open", "handoffs_closed", "results"):
        require_string(problems, f"storage_refs.{key}", storage_refs.get(key))
        value = storage_refs.get(key)
        if isinstance(value, str) and not rel_exists(root, value):
            problems.append(f"storage_refs.{key} target does not exist: {value}")

    schema_refs = registry.get("schema_refs")
    if not isinstance(schema_refs, dict):
        problems.append("schema_refs must be an object")
        schema_refs = {}
    for key in ("registry", "result", "handoff"):
        require_string(problems, f"schema_refs.{key}", schema_refs.get(key))
        value = schema_refs.get(key)
        if isinstance(value, str):
            if not rel_exists(root, value):
                problems.append(f"schema_refs.{key} target does not exist: {value}")
            else:
                try:
                    load_json(root / value)
                except json.JSONDecodeError as exc:
                    problems.append(f"{value} is not valid JSON: {exc}")

    scenarios = registry.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        problems.append("scenarios must be a non-empty list")
        scenarios = []

    seen_ids: set[str] = set()
    registered_paths: set[str] = set()
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            problems.append("scenarios entries must be objects")
            continue
        path = scenario.get("path")
        if isinstance(path, str):
            registered_paths.add(path)
        problems.extend(validate_scenario(root, scenario, seen_ids))

    scenarios_root = root / ".agents/spark/scenarios"
    discovered_paths = (
        {path.relative_to(root).as_posix() for path in scenarios_root.iterdir() if path.is_dir()}
        if scenarios_root.is_dir()
        else set()
    )
    if registered_paths != discovered_paths:
        missing = sorted(discovered_paths - registered_paths)
        stale = sorted(registered_paths - discovered_paths)
        if missing:
            problems.append(f"Spark scenarios missing from registry: {', '.join(missing)}")
        if stale:
            problems.append(
                "registry scenario paths missing from .agents/spark/scenarios/: "
                + ", ".join(stale)
            )

    require_string_list(problems, "validation_commands", registry.get("validation_commands"))
    _validate_spark_docs(root, seen_ids, problems)
    _validate_packet_dirs(root, seen_ids, problems)
    return problems


def _validate_spark_docs(root: Path, seen_ids: set[str], problems: list[str]) -> None:
    spark_readme = root / ".agents/spark/README.md"
    if spark_readme.exists():
        readme = spark_readme.read_text(encoding="utf-8")
        for scenario_id in sorted(seen_ids):
            if f"`{scenario_id}`" not in readme and f"[{scenario_id}]" not in readme:
                problems.append(f".agents/spark/README.md does not mention scenario: {scenario_id}")

    agents = root / ".agents/spark/AGENTS.md"
    if agents.exists():
        agents_text = agents.read_text(encoding="utf-8")
        for required in (
            "done-or-handoff",
            ".agents/spark/registry.json",
            "python .agents/spark/scripts/validate_spark_lane.py",
            "memory-is-not-proof",
        ):
            if required not in agents_text:
                problems.append(f".agents/spark/AGENTS.md does not mention {required}")

    notebook = root / ".agents/spark/SPARK_EXTRAPOLATION_NOTEBOOK.md"
    if notebook.exists():
        notebook_text = notebook.read_text(encoding="utf-8")
        for required in ("Agents-of-Abyss", "aoa-techniques", "aoa-skills", "OpenAI"):
            if required not in notebook_text:
                problems.append(f".agents/spark/SPARK_EXTRAPOLATION_NOTEBOOK.md missing {required}")

    swarm = root / ".agents/spark/SWARM.md"
    if swarm.exists() and ".agents/spark/registry.json" not in swarm.read_text(encoding="utf-8"):
        problems.append(".agents/spark/SWARM.md does not mention .agents/spark/registry.json")

    commands_text = validation_command_text(root)
    if ".agents/spark/scripts/validate_spark_lane.py" not in commands_text:
        problems.append("validation lanes do not run .agents/spark/scripts/validate_spark_lane.py")


def _validate_packet_dirs(root: Path, seen_ids: set[str], problems: list[str]) -> None:
    problems.extend(
        validate_packet_dir(root, root / ".agents/spark/results", REQUIRED_RESULT_MARKERS, seen_ids)
    )
    problems.extend(
        validate_packet_dir(root, root / ".agents/spark/handoffs/open", REQUIRED_HANDOFF_MARKERS, seen_ids)
    )
    problems.extend(
        validate_packet_dir(root, root / ".agents/spark/handoffs/closed", REQUIRED_HANDOFF_MARKERS, seen_ids)
    )
