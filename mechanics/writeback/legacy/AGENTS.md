# AGENTS.md

## Applies To

This card applies to `mechanics/writeback/legacy/`.

## Role

Legacy preserves writeback placement provenance from the former flat docs-root
surface.

It is not the active route for writeback doctrine, runtime writeback, or live
receipt state.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `../AGENTS.md`,
`../PROVENANCE.md`, and `legacy/INDEX.md`.

## Boundaries

- Start from active writeback surfaces before using legacy.
- Do not treat old flat docs-root paths as live aliases.
- Do not add new legacy material without indexing it and naming the active
  writeback surface it explains.
- Do not store runtime evidence, private traces, or unreduced receipts here.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
```

## Closeout

Report legacy index changes, active writeback surfaces consulted, and whether
any old flat docs-root reference remains outside allowed provenance.
