# AGENTS.md

Route card for `scripts/root-topology/`.

## Purpose

This district owns root topology builders and validators.

## Source

Topology source truth routes to `config/root-topology/root_technical_districts.json`
and `docs/root/ROOT_SURFACE_LAW.md`.

## Route

- Up: `scripts/AGENTS.md`, then `AGENTS.md`.
- Across: `tests/root-topology/` and `generated/root-topology/`.
- Downstream: root district placement checks.

## Validate

```bash
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
python -m pytest -q tests/root-topology
```
