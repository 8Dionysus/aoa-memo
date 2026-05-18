# AGENTS.md

## Applies To

This card applies to `mechanics/operational-gate/legacy/`.

## Role

`legacy/` preserves old operational-gate placement provenance through
`legacy/INDEX.md`.

It is not the active route for operational-gate docs, not a source of current
authority, and not a place to park active schemas, examples, generated outputs,
scripts, tests, quests, manifests, runtime receipts, incident logs, or release
owner doctrine.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `../AGENTS.md`, `../README.md`,
and `../PROVENANCE.md`.

## Boundaries

- Keep legacy entries short and route-like.
- Do not add old-path aliases back into active docs.
- Do not treat former flat docs-root paths as current contracts.
- Do not move active operational-gate docs here.
- Do not use legacy entries to claim release approval, runtime state, proof,
  role rights, route dispatch, stats truth, ToS writes, or owner acceptance.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
```

## Closeout

Report whether legacy provenance changed and whether the active route still
points to `mechanics/operational-gate/docs/`.
