# AGENTS.md

## Applies To

This card applies to `mechanics/shape-guard/`.

## Role

The shape-guard mechanic owns memo-side pruning and anti-inflation checks for
memory object families, mechanic packages, trust posture, and action-trigger
claims.

It does not own proof verdicts, current health, runtime execution, deletion
authority, schema replacement by itself, route sovereignty, role rights, KAG
promotion, or source-owner adoption.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, this file, `README.md`,
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and `PROVENANCE.md`.

For source docs, continue through `docs/AGENTS.md` and the target
`docs/*.md` surface.

## Post-Change Review

After shape-guard changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- generated mechanics or AGENTS mesh companions
- validators that enforce operation-first mechanics or stale route refs

Update only surfaces whose future-facing meaning changed.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q mechanics/shape-guard/tests/test_shape_guard_mechanic.py tests/test_memo_mechanics.py tests/test_agents_mesh.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the shape guard source docs changed, whether operation-first mechanics
validation changed, whether legacy/provenance was consulted, and whether any
old governance-local via-negativa route remains outside allowed provenance.
