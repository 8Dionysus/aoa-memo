# AGENTS.md

Route card for `generated/root-topology/`.

## Purpose

This district holds the generated root technical district atlas.
The current output is `root_technical_districts.min.json`.

## Source

`config/root-topology/root_technical_districts.json` is source truth.
`docs/root/ROOT_SURFACE_LAW.md` explains placement policy.

## Route

- Up: `generated/AGENTS.md`, then `AGENTS.md`.
- Across: `config/root-topology/` and `scripts/root-topology/`.
- Downstream: root district placement audits.

## Validate

```bash
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
```
