# AGENTS.md

## Applies To

This card applies to `mechanics/antifragility/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
antifragility memo mechanic.

It is not a legacy route, schema home, example warehouse, generated index,
proof bundle, route implementation, stats summary, or runtime repair lane.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/ARTIFACT_TOPOLOGY.md`,
`../AGENTS.md`, `../README.md`, `../PARTS.md`, `../OWNER_MAP.md`, and
`../PROVENANCE.md`.

## Boundaries

- Keep antifragility docs memory-only and reviewable.
- Do not claim proof, current health, route sovereignty, stats truth, rollback
  authorization, or runtime repair.
- Do not add root technical artifacts here; use the artifact topology rule
  before moving schemas, examples, generated outputs, scripts, or tests.
- Do not preserve old flat `docs/*.md` aliases.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q mechanics/antifragility/tests/test_antifragility_failure_lessons.py mechanics/antifragility/tests/test_antifragility_recovery_patterns.py
```

## Closeout

Report active antifragility docs changed, whether artifact placement changed,
and whether stronger owners remain outside `aoa-memo`.
