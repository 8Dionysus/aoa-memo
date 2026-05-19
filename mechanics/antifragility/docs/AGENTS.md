# AGENTS.md

## Applies To

This card applies to `mechanics/antifragility/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
antifragility memo mechanic.

It is not a legacy route, schema home, example warehouse, generated index,
proof bundle, route implementation, stats summary, or runtime repair lane.

## Route Stack

- Above: the package `AGENTS.md`, `README.md`, `PARTS.md`, and `OWNER_MAP.md`
  set the operation and stronger-owner split.
- Here: `docs/README.md` maps the source family; individual docs own active
  mechanic doctrine and support notes.
- Adjacent: package or part artifact homes own schemas, examples, config,
  generated outputs, scripts, tests, manifests, and quests. Use
  `mechanics/ARTIFACT_TOPOLOGY.md` before moving root technical artifacts.
- Below: no nested active law is expected here; legacy context routes through
  `../PROVENANCE.md` and `../legacy/`.

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
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/antifragility/parts/failure-lesson-memory/tests mechanics/antifragility/parts/recovery-pattern-memory/tests
```

## Closeout

Report active antifragility docs changed, whether artifact placement changed,
and whether stronger owners remain outside `aoa-memo`.
