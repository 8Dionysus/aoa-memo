"""Shared validation lane loader for aoa-memo.

Executable command authority lives in ``config/validation_lanes.json``.
This module keeps Python callers stable while the command lists remain
reviewable source data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, NamedTuple


class CommandStep(NamedTuple):
    label: str
    command: tuple[str, ...]
    layer: str
    mode: str
    owner_surface: str
    failure_route: str


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATION_LANES_PATH = REPO_ROOT / "config" / "validation_lanes.json"


def _load_manifest() -> dict[str, Any]:
    payload = json.loads(VALIDATION_LANES_PATH.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 2:
        raise ValueError(
            f"{VALIDATION_LANES_PATH}: unsupported schema_version "
            f"{payload.get('schema_version')!r}"
        )
    return payload


def _command(command: object, where: str) -> tuple[str, ...]:
    if not isinstance(command, list) or not command:
        raise ValueError(f"{VALIDATION_LANES_PATH}: {where}.command must be a non-empty list")
    if any(not isinstance(part, str) or not part for part in command):
        raise ValueError(f"{VALIDATION_LANES_PATH}: {where}.command must contain strings")
    return tuple(command)


def _string_field(value: object, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{VALIDATION_LANES_PATH}: {where} must be a non-empty string")
    return value


def _validator_layers(manifest: dict[str, Any]) -> dict[str, Any]:
    layers = manifest.get("validator_layers")
    if not isinstance(layers, dict) or not layers:
        raise ValueError(f"{VALIDATION_LANES_PATH}: validator_layers must be a non-empty mapping")
    return layers


def _sequence_defaults(manifest: dict[str, Any], name: str) -> dict[str, str]:
    defaults_by_sequence = manifest.get("sequence_defaults")
    if not isinstance(defaults_by_sequence, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: sequence_defaults must be a mapping")
    defaults = defaults_by_sequence.get(name)
    if not isinstance(defaults, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: sequence_defaults.{name} must be an object")
    return {
        "layer": _string_field(defaults.get("layer"), f"sequence_defaults.{name}.layer"),
        "mode": _string_field(defaults.get("mode"), f"sequence_defaults.{name}.mode"),
        "owner_surface": _string_field(
            defaults.get("owner_surface"),
            f"sequence_defaults.{name}.owner_surface",
        ),
        "failure_route": _string_field(
            defaults.get("failure_route"),
            f"sequence_defaults.{name}.failure_route",
        ),
    }


def _metadata_field(
    step: dict[str, object],
    defaults: dict[str, str],
    key: str,
    where: str,
) -> str:
    return _string_field(step.get(key, defaults[key]), f"{where}.{key}")


def _step(
    step: object,
    where: str,
    defaults: dict[str, str],
    layers: dict[str, Any],
) -> CommandStep:
    if not isinstance(step, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: {where} must be an object")
    label = step.get("label")
    if not isinstance(label, str) or not label:
        raise ValueError(f"{VALIDATION_LANES_PATH}: {where}.label must be a non-empty string")
    layer = _metadata_field(step, defaults, "layer", where)
    if layer not in layers:
        raise ValueError(f"{VALIDATION_LANES_PATH}: {where}.layer references unknown layer {layer!r}")
    return CommandStep(
        label=label,
        command=_command(step.get("command"), where),
        layer=layer,
        mode=_metadata_field(step, defaults, "mode", where),
        owner_surface=_metadata_field(step, defaults, "owner_surface", where),
        failure_route=_metadata_field(step, defaults, "failure_route", where),
    )


def _raw_sequence(manifest: dict[str, Any], name: str) -> tuple[CommandStep, ...]:
    sequences = manifest.get("command_sequences")
    if not isinstance(sequences, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: command_sequences must be a mapping")
    sequence = sequences.get(name)
    if not isinstance(sequence, list) or not sequence:
        raise ValueError(f"{VALIDATION_LANES_PATH}: missing command sequence {name!r}")
    defaults = _sequence_defaults(manifest, name)
    layers = _validator_layers(manifest)
    return tuple(
        _step(step, f"command_sequences.{name}[{idx}]", defaults, layers)
        for idx, step in enumerate(sequence)
    )


def _composition(manifest: dict[str, Any], name: str) -> tuple[str, ...] | None:
    compositions = manifest.get("sequence_compositions", {})
    if not isinstance(compositions, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: sequence_compositions must be a mapping")
    composition = compositions.get(name)
    if composition is None:
        return None
    if not isinstance(composition, list) or not composition:
        raise ValueError(f"{VALIDATION_LANES_PATH}: sequence_compositions.{name} must be a non-empty list")
    if any(not isinstance(item, str) or not item for item in composition):
        raise ValueError(f"{VALIDATION_LANES_PATH}: sequence_compositions.{name} must contain strings")
    return tuple(composition)


def _sequence(manifest: dict[str, Any], name: str, seen: frozenset[str] = frozenset()) -> tuple[CommandStep, ...]:
    if name in seen:
        raise ValueError(f"{VALIDATION_LANES_PATH}: recursive sequence composition at {name!r}")
    composition = _composition(manifest, name)
    if composition is None:
        return _raw_sequence(manifest, name)
    steps: list[CommandStep] = []
    for child in composition:
        steps.extend(_sequence(manifest, child, seen | {name}))
    return tuple(steps)


def command_sequence(name: str) -> tuple[CommandStep, ...]:
    return _sequence(_MANIFEST, name)


def ci_mode_sequence_name(mode: str) -> str:
    modes = _MANIFEST.get("ci_modes")
    if not isinstance(modes, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: ci_modes must be a mapping")
    sequence_name = modes.get(mode)
    if not isinstance(sequence_name, str) or not sequence_name:
        raise KeyError(mode)
    return sequence_name


def ci_modes() -> tuple[str, ...]:
    modes = _MANIFEST.get("ci_modes")
    if not isinstance(modes, dict):
        raise ValueError(f"{VALIDATION_LANES_PATH}: ci_modes must be a mapping")
    return tuple(sorted(str(mode) for mode in modes))


_MANIFEST = _load_manifest()

SOURCE_FAST_COMMAND_SEQUENCE = command_sequence("source_fast")
GENERATED_COMMAND_SEQUENCE = command_sequence("generated")
EXPORT_RUNTIME_COMMAND_SEQUENCE = command_sequence("export_runtime")
RUNTIME_COMMAND_SEQUENCE = command_sequence("runtime")
MEMORY_CONTEXT_COMMAND_SEQUENCE = command_sequence("memory_context")
INTER_AGENT_HANDOFF_COMMAND_SEQUENCE = command_sequence("inter_agent_handoff")
EVAL_COMMAND_SEQUENCE = command_sequence("eval")
AUDIT_COMMAND_SEQUENCE = command_sequence("audit")
SECURITY_COMMAND_SEQUENCE = command_sequence("security")
TEST_COMMAND_SEQUENCE = command_sequence("tests")
RELEASE_OPS_COMMAND_SEQUENCE = command_sequence("release_ops")
RELEASE_CHECK_COMMAND_SEQUENCE = command_sequence("release_check")
NIGHTLY_COMMAND_SEQUENCE = command_sequence("nightly")
POST_MERGE_COMMAND_SEQUENCE = command_sequence("post_merge")

# Compatibility aliases for older callers during the lane rename.
MEMORY_CORE_COMMAND_SEQUENCE = MEMORY_CONTEXT_COMMAND_SEQUENCE
AGENT_LANE_COMMAND_SEQUENCE = EVAL_COMMAND_SEQUENCE
ROOT_TOPOLOGY_COMMAND_SEQUENCE = SOURCE_FAST_COMMAND_SEQUENCE
MECHANIC_INDEX_COMMAND_SEQUENCE = command_sequence("mechanics")
