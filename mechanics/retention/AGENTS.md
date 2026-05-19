# AGENTS.md

## Applies To

This card applies to `mechanics/retention/`.

## Role

The retention mechanic owns memo-side retention review posture: cross-repo
retention memory, office markers, governance retention checks, and post-release
watch or outcome surfaces.

It does not execute retention, schedule checks, store private traces, keep
unreduced personal data, or own runtime retention policy.

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
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q mechanics/retention/parts/cross-repo-and-governance-retention/tests mechanics/retention/parts/office-markers/tests mechanics/retention/parts/post-release-retention/tests
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the retention part changed, whether legacy/provenance was consulted,
which owner route remains stronger, and whether any old flat retention
docs-root reference remains.
