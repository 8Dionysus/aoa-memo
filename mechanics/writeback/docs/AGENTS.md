# AGENTS.md

## Applies To

This card applies to `mechanics/writeback/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
writeback mechanic.

It is not runtime storage, a live receipt ledger, a generated companion home,
or owner-local implementation.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/ARTIFACT_TOPOLOGY.md`,
`../AGENTS.md`, `../README.md`, `../PARTS.md`, `../OWNER_MAP.md`, and
`../PROVENANCE.md`.

## Boundaries

- Keep writeback source-linked, candidate-only where appropriate, and weaker
  than runtime or owner acceptance.
- Do not claim a live writeback occurred.
- Do not add root technical artifacts here; use the artifact topology rule
  before moving schemas, examples, generated outputs, scripts, or tests.
- Do not preserve old flat `docs/*.md` aliases.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
```

## Closeout

Report active writeback docs changed, generated companions affected or not
affected, and which stronger owner remains responsible for live behavior.
