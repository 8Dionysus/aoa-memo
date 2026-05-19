# AGENTS.md

## Applies To

This card applies to `mechanics/governance/legacy/`.

## Role

`legacy/` preserves old governance docs-root placement provenance through
`legacy/INDEX.md`.

It is not the active route for governance docs, not a source of current
authority, and not a place to park active schemas, examples, generated outputs,
scripts, tests, or runtime receipts.

## Route Stack

- Above: the package `AGENTS.md`, `PROVENANCE.md`, and `OWNER_MAP.md` define
  the active route and stronger-owner boundary.
- Here: `INDEX.md` maps former paths to active surfaces, `DISTILLATION_LOG.md`
  records restoration decisions, and `raw/` contains historical snapshots.
- Below: `raw/` is evidence only. Do not edit it as current doctrine and do not
  cite it as an active route.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `../AGENTS.md`, `../README.md`,
and `../PROVENANCE.md`.

## Boundaries

- Keep legacy entries short and route-like.
- Do not add old-path aliases back into active docs.
- Do not treat former flat paths as current contracts.
- Do not move active governance docs here.

## Validation

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

## Closeout

Report whether legacy provenance changed and whether the active route still
points to `mechanics/governance/docs/`.
