# AGENTS.md

## Applies To

This card applies to `mechanics/readiness-boundary/legacy/`.

## Role

`legacy/` preserves readiness-boundary placement provenance.

It is not the active route for readiness-boundary work and must not receive
new active schemas, examples, generated outputs, scripts, or tests.

## Read Before Editing

Read:

1. root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `mechanics/readiness-boundary/AGENTS.md`
4. `mechanics/readiness-boundary/PROVENANCE.md`
5. `legacy/INDEX.md`

## Boundaries

- Keep this lane about former paths and provenance.
- Do not duplicate active readiness-boundary docs here.
- Do not cite legacy paths as source truth.
- Route active readiness-boundary work to `mechanics/readiness-boundary/`.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```
