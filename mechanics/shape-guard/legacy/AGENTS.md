# AGENTS.md

## Applies To

This card applies to `mechanics/shape-guard/legacy/`.

## Role

`legacy/` preserves old shape-guard placement provenance through
`legacy/INDEX.md`.

It is not the active route for shape-guard docs, not a source of current
authority, and not a place to park active schemas, examples, generated outputs,
scripts, tests, or runtime receipts.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `../AGENTS.md`, `../README.md`,
and `../PROVENANCE.md`.

## Boundaries

- Keep legacy entries short and route-like.
- Do not add old-path aliases back into active docs.
- Do not treat former flat or governance-local paths as current contracts.
- Do not move active shape-guard docs here.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
```

## Closeout

Report whether legacy provenance changed and whether the active route still
points to `mechanics/shape-guard/docs/`.
