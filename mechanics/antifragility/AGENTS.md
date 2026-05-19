# AGENTS.md

## Applies To

This card applies to `mechanics/antifragility/`.

## Role

The antifragility mechanic owns memo-side failure lesson and recovery pattern
memory: when to preserve a reviewed stress lesson, how to recall it, when a
drift-review or rollback-followthrough window should remain visible, and which
stronger owners must still be checked.

It does not own proof, route authority, stats conclusions, source receipts,
runtime repair, rollback execution, or current health claims.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, this file, `README.md`,
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and `PROVENANCE.md`.

For source docs, continue through `docs/AGENTS.md` and the target
`docs/*.md` surface.

## Post-Change Review

After antifragility changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- matching schemas, examples, generated object surfaces, tests, and writeback
  refs
- generated mechanics or AGENTS mesh companions

Update only surfaces whose future-facing meaning changed.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q mechanics/antifragility/parts/failure-lesson-memory/tests mechanics/antifragility/parts/recovery-pattern-memory/tests
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the antifragility source family changed, whether legacy/provenance was
consulted, which stronger owner route remains outside `aoa-memo`, and whether
any old antifragility docs-root reference remains outside allowed provenance.
