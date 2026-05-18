# AGENTS.md

## Applies To

This card applies to `mechanics/titan/legacy/`.

## Role

Legacy preserves Titan placement provenance from the former flat docs-root
surface and the transitional `mechanics/titan/docs/` district.

It is not the active route for Titan doctrine and must not become a place to
hide new work.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `../AGENTS.md`,
`../PROVENANCE.md`, and `legacy/INDEX.md`.

## Boundaries

- Start from active Titan surfaces before using legacy.
- Do not treat old flat docs-root or transitional docs-district paths as live
  aliases.
- Do not add new legacy material without indexing it and naming the active
  Titan surface it explains.
- Do not delete provenance just to make the active tree look cleaner.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
```

## Closeout

Report legacy index changes, active Titan surfaces consulted, and whether any
old Titan docs-root or docs-district reference remains outside allowed
provenance.
