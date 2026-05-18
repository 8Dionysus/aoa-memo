# AGENTS.md

## Applies To

This card applies to `mechanics/governance/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
governance memo mechanic.

It is not a legacy route, proof bundle, release approval lane, council
authority, role-rights surface, runtime governance worker, KAG promotion lane,
or Tree-of-Sophia write path.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/ARTIFACT_TOPOLOGY.md`,
`../AGENTS.md`, `../README.md`, `../PARTS.md`, `../OWNER_MAP.md`, and
`../PROVENANCE.md`.

## Boundaries

- Keep governance docs memory-only and reviewable.
- Do not claim council authority, proof, release approval, route sovereignty,
  role rights, KAG promotion, runtime governance, or Tree-of-Sophia writes.
- Do not add root technical artifacts here; use the artifact topology rule
  before moving schemas, examples, generated outputs, scripts, or tests.
- Do not preserve old flat `docs/*.md` aliases.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q tests/test_governance_mechanic.py tests/test_memo_mechanics.py
```

## Closeout

Report active governance docs changed, whether artifact placement changed, and
whether stronger owners remain outside `aoa-memo`.
