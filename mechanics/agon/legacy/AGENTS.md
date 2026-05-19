# AGENTS.md

## Applies To

This card applies to `mechanics/agon/legacy/`.

## Role

Legacy preserves Agon placement provenance from the former flat docs-root
surface and the transitional `mechanics/agon/docs/` district.

It is not the active route for Agon doctrine and must not become a place to
hide new work.

## Route Stack

- Above: the package `AGENTS.md`, `PROVENANCE.md`, and `OWNER_MAP.md` define
  the active route and stronger-owner boundary.
- Here: `INDEX.md` maps former paths to active surfaces, `DISTILLATION_LOG.md`
  records restoration decisions, and `raw/` contains historical snapshots.
- Below: `raw/` is evidence only. Do not edit it as current doctrine and do not
  cite it as an active route.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `../AGENTS.md`,
`../PROVENANCE.md`, and `legacy/INDEX.md`.

## Boundaries

- Start from active Agon surfaces before using legacy.
- Do not treat old flat docs-root or transitional docs-district paths as live
  aliases.
- Do not add new legacy material without indexing it and naming the active
  Agon surface it explains.
- Do not delete provenance just to make the active tree look cleaner.

## Validation

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

## Closeout

Report legacy index changes, active Agon surfaces consulted, and whether any
old Agon docs-root or docs-district reference remains outside allowed
provenance.
