# AGENTS.md

Route card for `config/agents/`.

## Purpose

This district owns the source map for agent-facing route-card coverage.

## Source

`agents_mesh.json` is source-authored and drives
`generated/agents/agents_mesh.min.json`.

## Route

- Up: `config/AGENTS.md`, then `AGENTS.md`.
- Across: every `AGENTS.md` named in `canonical_cards`.
- Downstream: `scripts/agents/` builders and validators.

## Validate

```bash
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
```
