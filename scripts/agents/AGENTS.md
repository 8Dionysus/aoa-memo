# AGENTS.md

Route card for `scripts/agents/`.

## Purpose

This district owns AGENTS mesh builders, validators, and semantic route-card
checks.

## Source

`config/agents/agents_mesh.json` and route cards are source surfaces.
Generated parity lands in `generated/agents/`.

## Route

- Up: `scripts/AGENTS.md`, then `AGENTS.md`.
- Across: `config/agents/` and `tests/agents/`.
- Downstream: `generated/agents/agents_mesh.min.json`.

## Validate

```bash
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python -m pytest -q tests/agents
```
