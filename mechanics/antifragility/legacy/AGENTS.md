# AGENTS.md

## Applies To

This card applies to `mechanics/antifragility/legacy/`.

## Role

Legacy preserves antifragility placement provenance from the former flat
docs-root surface.

It is not the active route for antifragility doctrine and must not become a
place to hide new work.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `../AGENTS.md`,
`../PROVENANCE.md`, and `legacy/INDEX.md`.

## Boundaries

- Start from active antifragility surfaces before using legacy.
- Do not treat old flat docs-root paths as live aliases.
- Do not add new legacy material without indexing it and naming the active
  antifragility surface it explains.
- Do not delete provenance just to make the active tree look cleaner.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
```

## Closeout

Report legacy index changes, active antifragility surfaces consulted, and
whether any old flat docs-root reference remains outside allowed provenance.
