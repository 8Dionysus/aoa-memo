# AGENTS.md

Route card for `scripts/release/`.

## Purpose

This district owns the repo-wide release gate.

## Source

`release_check.py` orchestrates validators but does not replace owner surfaces.
The command sequence is source-authored in `config/validation_lanes.json` and
loaded through `scripts/validation_lanes.py`. When it fails, fix the failing
owner district rather than weakening the gate.

## Route

- Up: `scripts/AGENTS.md`, then `AGENTS.md`.
- Across: `docs/root/RELEASING.md`, `docs/validation/VALIDATOR_TOPOLOGY.md`,
  `docs/testing/TEST_TOPOLOGY.md`, and `config/validation_lanes.json`.
- Downstream: all validator districts.

## Validate

```bash
python scripts/release/release_check.py
```
