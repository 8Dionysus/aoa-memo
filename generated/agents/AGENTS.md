# AGENTS.md

Route card for `generated/agents/`.

## Purpose

This district holds the compact AGENTS mesh generated companion.
The current output is `agents_mesh.min.json`.

## Source

`config/agents/agents_mesh.json` and the referenced `AGENTS.md` cards are the
source surfaces. The JSON here is a generated inspection surface.

## Route

- Up: `generated/AGENTS.md`, then `AGENTS.md`.
- Across: `config/agents/`.
- Downstream: agent route-card audits.

## Validate

```bash
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
```
