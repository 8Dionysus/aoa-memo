# AGENTS.md

Route card for `generated/mechanics/`.

## Purpose

This district holds generated mechanic indexes, cards, owner routes, landing
logs, readiness, and artifact inventory.

## Source

Source truth routes to `config/mechanics/memo_mechanics.json`,
`mechanics/README.md`, and package-local mechanic surfaces.

## Route

- Up: `generated/AGENTS.md`, then `AGENTS.md`.
- Across: `mechanics/` and `scripts/mechanics/`.
- Downstream: OS Abyss readiness inspection and package route selection.

## Validate

```bash
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/mechanics/validate_memo_mechanic_readiness.py
```
