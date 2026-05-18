# AGENTS.md

## Applies To

This card applies to `mechanics/readiness-boundary/docs/`.

## Role

`mechanics/readiness-boundary/docs/` holds active mechanic-owned doctrine for
the readiness-boundary mechanic.

It is active mechanic-owned doctrine, not root memory-object canon and not
proof, runtime, graph, route, role, or source-owner authority.

## Read Before Editing

Read:

1. root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `mechanics/ARTIFACT_TOPOLOGY.md`
4. `mechanics/readiness-boundary/AGENTS.md`
5. `mechanics/readiness-boundary/README.md`
6. the target doc

## Boundaries

- Keep readiness pressure mapped to existing memory objects.
- Keep proof, runtime retention, graph substrate, route dispatch, role rights,
  scenario meaning, and source-owner acceptance outside this package.
- Do not introduce a new memory-object family from a docs edit.

Use `mechanics/ARTIFACT_TOPOLOGY.md` before moving readiness-boundary schemas,
examples, generated outputs, scripts, tests, manifests, or config.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/validate_memo.py
python -m pytest -q mechanics/readiness-boundary/tests/test_readiness_boundary_mechanic.py
```
