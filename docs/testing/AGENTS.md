# AGENTS.md

Route card for `docs/testing/`.

## Purpose

This district owns the human-readable test topology and the machine-readable
test inventory for `aoa-memo`.

It references validation lanes, but it does not own validator meaning, memory
doctrine, proof authority, runtime behavior, or mechanic source truth.

## Source

Validator meaning routes to `docs/validation/VALIDATOR_TOPOLOGY.md`.
Command authority routes to `config/validation_lanes.json`.
Test ownership routes to the source surfaces named in
`docs/testing/test_inventory.json`.
Release orchestration routes through `scripts/release/release_check.py`.

## Route

- Up: `docs/AGENTS.md`, then `AGENTS.md`.
- Across: `docs/validation/AGENTS.md`, `config/validation_lanes.json`,
  `scripts/validation_lanes.py`, and `scripts/ci_gate.py`.
- Downstream: `tests/`, mechanic-local tests, `.agents/spark/tests/`, and the
  release gate.

## Validate

```bash
python -m pytest -q tests/root-topology/test_test_topology.py
python -m pytest -q tests/root-topology/test_validation_lanes.py
python -m pytest -q tests/root-topology/test_validator_topology.py
python scripts/ci_gate.py --mode source-fast
```
