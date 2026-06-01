# AGENTS.md

Route card for `docs/validation/`.

## Purpose

This district owns the validator topology for `aoa-memo`: which boundary a
validator protects, which source owns that boundary, which lane runs it, and
which checks are only memo-side declarations because runtime, eval, security,
or downstream agent authority lives elsewhere.

It does not own the test inventory, generated outputs, release scripts, memory
truth, runtime policy engine, grader datasets, or tool permission enforcement.

## Source

Validator topology lives in `VALIDATOR_TOPOLOGY.md`.
Command-authority balance lives in `COMMAND_AUTHORITY.md`.
Validation entrypoint inventory lives in `validator_inventory.json`.
Executable lane data lives in `config/validation_lanes.json`.
Test file inventory lives in `docs/testing/test_inventory.json`.

## Route

- Up: `docs/AGENTS.md`, then root `AGENTS.md`.
- Across: `docs/testing/AGENTS.md`, `config/validation_lanes.json`,
  `scripts/validation_lanes.py`, and `scripts/root-topology/validate_validator_topology.py`.
- Downstream: `scripts/ci_gate.py`, `scripts/release/release_check.py`,
  focused CI modes, nightly drift checks, and release gates.

## Validate

```bash
python scripts/root-topology/validate_validator_topology.py
python -m pytest -q tests/root-topology/test_validator_topology.py tests/root-topology/test_validation_lanes.py
python scripts/ci_gate.py --mode source-fast
```
