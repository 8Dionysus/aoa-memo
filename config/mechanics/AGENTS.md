# AGENTS.md

Route card for `config/mechanics/`.

## Purpose

This district owns repo-wide mechanic package source maps.

## Source

`memo_mechanics.json` is source-authored. It drives mechanic package indexes,
cards, owner routes, landing logs, readiness, and artifact inventory.

## Route

- Up: `config/AGENTS.md`, then `AGENTS.md`.
- Across: `mechanics/README.md` and each mechanic `README.md`.
- Downstream: `scripts/mechanics/` and `generated/mechanics/`.

## Validate

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```
