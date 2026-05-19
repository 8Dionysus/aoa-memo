# AGENTS.md

## Applies To

This card applies to `mechanics/adoption/`.

## Role

The adoption mechanic owns memo-side adoption posture: reviewable memory
candidate intake, adoption boundaries, forgetting and revision pressure, scar
writeback posture, and routing adoption source refs.

It does not prove adoption, grant route sovereignty, run retention, write live
memory, or accept owner-local behavior.

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

## Post-Change Review

After adoption changes, check whether these surfaces moved:

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
python -m pytest -q mechanics/adoption/parts/adoption-boundary/tests mechanics/adoption/parts/revision-and-retention-pressure/tests mechanics/adoption/parts/scar-and-routing-adoption/tests
```

Before landing, also run:

```bash
python scripts/release/release_check.py
```

## Closeout

Report the adoption part changed, whether legacy/provenance was consulted,
which owner route remains stronger, and whether any old flat adoption docs-root
reference remains.
