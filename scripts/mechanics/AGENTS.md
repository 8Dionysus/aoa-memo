# AGENTS.md

Route card for `scripts/mechanics/`.

## Purpose

This district owns mechanic index, readiness, owner route, landing log, card,
parts, and artifact validators.

## Source

Source truth routes to `config/mechanics/memo_mechanics.json`,
`mechanics/README.md`, and package-local mechanic files.

## Route

- Up: `scripts/AGENTS.md`, then `AGENTS.md`.
- Across: `tests/mechanics/` and `generated/mechanics/`.
- Downstream: mechanic package readiness and artifact inventory.

## Validate

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/validate_memo_mechanic_parts.py
python -m pytest -q tests/mechanics
```
