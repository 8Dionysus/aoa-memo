# AGENTS.md

## Applies To

This card applies to `mechanics/retention/`.

## Role

The retention mechanic owns memo-side retention review posture: cross-repo
retention memory, office markers, governance retention checks,
consolidation/forgetting operations, and post-release watch or outcome
surfaces.

It does not execute retention, schedule checks, store private traces, keep
unreduced personal data, or own runtime retention policy.

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

After retention changes, check whether these surfaces moved:

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
python scripts/memory/validate_memory_operations.py
python -m pytest -q mechanics/retention/parts/consolidation-and-forgetting/tests mechanics/retention/parts/cross-repo-and-governance-retention/tests mechanics/retention/parts/office-markers/tests mechanics/retention/parts/post-release-retention/tests
```

Before landing, also run:

```bash
python scripts/release/release_check.py
```

## Closeout

Report the retention part changed, whether legacy/provenance was consulted,
which owner route remains stronger, and whether any old flat retention
docs-root reference remains.
