# AGENTS.md

Route card for `docs/root/`.

## Purpose

This district owns root placement law, release procedure, and preserved root
reference guidance for the repository.

## Source

`ROOT_SURFACE_LAW.md` is the active placement law.
`RELEASING.md` owns release procedure.
`AGENTS_ROOT_REFERENCE.md` preserves deep root guidance that should migrate to
nearer owner cards when it becomes active local law.

## Route

- Up: `docs/AGENTS.md`, then `AGENTS.md`.
- Across: `config/root-topology/` and `generated/root-topology/` for machine
  mirrors of district placement.
- Downstream: root district `AGENTS.md` files when placement rules become local.

## Validate

```bash
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
python scripts/release/release_check.py
```
