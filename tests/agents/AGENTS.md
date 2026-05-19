# AGENTS.md

Route card for `tests/agents/`.

## Purpose

This district owns regression tests for AGENTS mesh and agent-facing lane
contracts.

## Source

Tests here protect `config/agents/agents_mesh.json`, route cards, and Spark
lane contracts.

## Route

- Up: `tests/AGENTS.md`, then `AGENTS.md`.
- Across: `scripts/agents/` and `.agents/spark/`.
- Downstream: `generated/agents/`.

## Validate

```bash
python -m pytest -q tests/agents
```
