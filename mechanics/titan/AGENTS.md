# AGENTS.md

## Applies To

This card applies to `mechanics/titan/`.

## Role

The Titan mechanic owns memo-side Titan recall candidates, remembrance source
refs, memory loom posture, audit memory policy, personality memory policy,
bridge digest, console digest, closeout posture, and swarm memory policy.

It does not grant memory write authority, role rights, proof status, private
retention, or owner-repo Titan doctrine.

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
`docs/TITAN_*.md` surface.

## Post-Change Review

After Titan changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- matching schemas, examples, tests, and owner refs
- generated mechanics or AGENTS mesh companions

Update only surfaces whose future-facing meaning changed.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q mechanics/titan/parts/recall-and-remembrance-posture/tests mechanics/titan/parts/audit-personality-and-swarm-policy/tests
python -m pytest -q mechanics/titan/parts/recall-and-remembrance-posture/tests mechanics/titan/parts/closeout-and-digest-posture/tests mechanics/titan/parts/audit-personality-and-swarm-policy/tests
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the Titan memory posture changed, whether legacy/provenance was
consulted, which stronger owner route remains outside `aoa-memo`, and whether
any old Titan docs-root or docs-district reference remains outside allowed
provenance.
