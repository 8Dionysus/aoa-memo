# AGENTS.md

## Applies To

This card applies to `mechanics/governance/`.

## Role

The governance mechanic owns memo-side authority-boundary memory for
governance, federation, installation, certification, precedent, and stay
orders.

It does not own council authority, source-owner consent, proof verdicts,
runtime governance, Tree-of-Sophia writes, release approval, or hidden
assistant self-change.

## Route Stack

- Above: root `AGENTS.md` owns repo identity and release route;
  `mechanics/AGENTS.md` owns shared mechanic package law and validators.
- Here: `README.md` is the mechanic card, `DIRECTION.md` names current
  pressure, `PARTS.md` lists active function nodes, `OWNER_MAP.md` names
  stronger owners, and `PROVENANCE.md` plus `legacy/` preserve placement
  history.
- Below: `docs/` holds active source docs, `parts/` holds functioning
  contracts and artifact homes, and `legacy/` is historical evidence only.

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
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python -m pytest -q mechanics/governance/parts/governance-boundary/tests tests/mechanics/test_memo_mechanics.py
```

Before landing, also run:

```bash
python scripts/release/release_check.py
```

## Closeout

Report the governance source family changed, whether legacy/provenance was
consulted, which stronger owner route remains outside `aoa-memo`, and whether
any old governance docs-root reference remains outside allowed provenance.
