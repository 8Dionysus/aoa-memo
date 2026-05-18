# AGENTS.md

## Applies To

This card applies to `mechanics/retention/legacy/`.

## Role

Legacy preserves retention placement provenance from the former flat docs-root
surface.

It is not the active route for retention doctrine and must not become runtime
retention storage.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `../AGENTS.md`,
`../PROVENANCE.md`, and `legacy/INDEX.md`.

## Boundaries

- Start from active retention surfaces before using legacy.
- Do not treat old flat docs-root paths as live aliases.
- Do not add new legacy material without indexing it and naming the active
  retention surface it explains.
- Do not store private traces, runtime state, or unreduced personal data here.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
```

## Closeout

Report legacy index changes, active retention surfaces consulted, and whether
any old flat docs-root reference remains outside allowed provenance.
