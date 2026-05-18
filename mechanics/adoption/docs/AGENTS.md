# AGENTS.md

## Applies To

This card applies to `mechanics/adoption/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
adoption mechanic.

It is not a legacy route, schema home, example warehouse, generated index, or
runtime adoption implementation.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/ARTIFACT_TOPOLOGY.md`,
`../AGENTS.md`, `../README.md`, `../PARTS.md`, `../OWNER_MAP.md`, and
`../PROVENANCE.md`.

## Boundaries

- Keep adoption docs candidate-only and reviewable.
- Do not claim proof, route sovereignty, runtime write, or owner acceptance.
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

Report active adoption docs changed, whether artifact placement changed, and
whether stronger owners remain outside `aoa-memo`.
