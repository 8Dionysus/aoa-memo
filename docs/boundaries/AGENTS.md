# AGENTS.md

Route card for `docs/boundaries/`.

## Purpose

This district owns repository and operational boundary language for memo:
what memory may claim, what must route to stronger owners, and where live
operation remains outside memo.

## Source

`BOUNDARIES.md` is the primary owner-boundary surface.
`OPERATIONAL_BOUNDARY.md` narrows operational claims and runtime-facing limits.

## Route

- Up: `docs/AGENTS.md`, then `AGENTS.md`.
- Across: `docs/memory/` for object doctrine and `docs/posture/` for temporal
  and provenance posture.
- Downstream: mechanic `OWNER_MAP.md` files when a boundary is package-local.

## Validate

```bash
python scripts/memory/validate_memo.py
python scripts/root-topology/validate_docs_districts.py
```
