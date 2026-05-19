# AGENTS.md

## Applies To

This card applies to `mechanics/shape-guard/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
shape-guard memo mechanic.

It is not a legacy route, proof bundle, deletion authority, runtime cleanup
lane, role-rights surface, route implementation, KAG promotion lane, or source
owner adoption path.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/ARTIFACT_TOPOLOGY.md`,
`../AGENTS.md`, `../README.md`, `../PARTS.md`, `../OWNER_MAP.md`, and
`../PROVENANCE.md`.

## Boundaries

- Keep shape-guard docs memory-only, reviewable, and operation-first.
- Do not claim proof, current health, action authority, runtime cleanup,
  deletion execution, route sovereignty, role rights, KAG promotion, or owner
  adoption.
- Do not add root technical artifacts here; use the artifact topology rule
  before moving schemas, examples, generated outputs, scripts, or tests.
- Do not preserve old governance-local via-negativa aliases.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q mechanics/shape-guard/parts/via-negativa-checklist/tests/test_shape_guard_mechanic.py tests/test_memo_mechanics.py
```

## Closeout

Report active shape-guard docs changed, whether artifact placement changed,
and whether stronger owners remain outside `aoa-memo`.
