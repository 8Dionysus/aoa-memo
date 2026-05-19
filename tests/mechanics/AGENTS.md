# AGENTS.md

Route card for `tests/mechanics/`.

## Purpose

This district owns regression tests for mechanic indexes, artifact topology,
parts contracts, owner routes, landing logs, and readiness.

## Source

Tests here protect `mechanics/`, `config/mechanics/`, `scripts/mechanics/`,
and `generated/mechanics/`.

## Route

- Up: `tests/AGENTS.md`, then `AGENTS.md`.
- Across: `scripts/mechanics/`.
- Downstream: OS Abyss mechanic readiness inspection.

## Validate

```bash
python -m pytest -q tests/mechanics
```
