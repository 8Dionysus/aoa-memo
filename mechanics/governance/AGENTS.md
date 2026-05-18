# AGENTS.md

## Applies To

This card applies to `mechanics/governance/`.

## Role

The governance mechanic owns memo-side governance, federation, installation,
certification, precedent, stay-order, and via-negativa memory boundaries.

It does not own council authority, source-owner consent, proof verdicts,
runtime governance, Tree-of-Sophia writes, release approval, or hidden
assistant self-change.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, this file, `README.md`,
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and `PROVENANCE.md`.

For source docs, continue through `docs/AGENTS.md` and the target
`docs/*.md` surface.

## Post-Change Review

After governance changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- generated mechanics or AGENTS mesh companions

Update only surfaces whose future-facing meaning changed.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q tests/test_governance_mechanic.py tests/test_memo_mechanics.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the governance source family changed, whether legacy/provenance was
consulted, which stronger owner route remains outside `aoa-memo`, and whether
any old governance docs-root reference remains outside allowed provenance.
