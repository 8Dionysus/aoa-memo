# AGENTS.md

## Applies To

This card applies to `mechanics/checkpoint/legacy/`.

## Role

`legacy/` preserves checkpoint placement provenance.

It is not the active route for checkpoint work and must not receive new active
schemas, examples, generated outputs, scripts, or tests.

## Route Stack

- Above: the package `AGENTS.md`, `PROVENANCE.md`, and `OWNER_MAP.md` define
  the active route and stronger-owner boundary.
- Here: `INDEX.md` maps former paths to active surfaces, `DISTILLATION_LOG.md`
  records restoration decisions, and `raw/` contains historical snapshots.
- Below: `raw/` is evidence only. Do not edit it as current doctrine and do not
  cite it as an active route.

## Read Before Editing

Read:

1. root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `mechanics/checkpoint/AGENTS.md`
4. `mechanics/checkpoint/PROVENANCE.md`
5. `legacy/INDEX.md`

## Boundaries

- Keep this lane about former paths and provenance.
- Do not duplicate active checkpoint docs here.
- Do not cite legacy paths as source truth.
- Route active checkpoint work to `mechanics/checkpoint/`.

## Validation

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

Before landing, also run:

```bash
python scripts/release/release_check.py
```
