# AGENTS.md

Route card for `scripts/release/`.

## Purpose

This district owns the repo-wide release gate.

## Source

`release_check.py` orchestrates validators but does not replace owner surfaces.
When it fails, fix the failing owner district rather than weakening the gate.

## Route

- Up: `scripts/AGENTS.md`, then `AGENTS.md`.
- Across: `docs/root/RELEASING.md`.
- Downstream: all validator districts.

## Validate

```bash
python scripts/release/release_check.py
```
