# AGENTS.md

Route card for `scripts/memory/validators/`.

## Purpose

This district owns the layer modules behind `scripts/memory/validate_memo.py`.
Each module maps to one validation boundary: schema, memory-context, runtime,
handoff, eval, or shared helper state. The CLI wrapper remains only for
compatibility and lane dispatch.

## Source

Validator meaning routes to `docs/validation/VALIDATOR_TOPOLOGY.md` and
`config/validation_lanes.json`. Memory doctrine, examples, and schemas remain
owned by their local source surfaces; these modules must not become a hidden source of memory meaning.

## Route

- Up: `scripts/memory/AGENTS.md`, then `scripts/AGENTS.md`.
- Across: `tests/memory/test_memo_validators.py` and
  `tests/root-topology/test_validator_topology.py`.
- Downstream: `scripts/memory/validate_memo.py` compatibility CLI and release
  lanes in `config/validation_lanes.json`.

## Validate

```bash
python scripts/memory/validate_memo.py --profile all
python scripts/root-topology/validate_validator_topology.py
python -m pytest -q tests/memory/test_memo_validators.py tests/root-topology/test_validator_topology.py
```
