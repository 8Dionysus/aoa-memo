# AGENTS.md

## Applies To

This card applies to `mechanics/adoption/`.

## Role

The adoption mechanic owns memo-side adoption posture: reviewable memory
candidate intake, adoption boundaries, forgetting and revision pressure, scar
writeback posture, and routing adoption source refs.

It does not prove adoption, grant route sovereignty, run retention, write live
memory, or accept owner-local behavior.

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
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q mechanics/adoption/tests/test_routing_memory_adoption.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the adoption part changed, whether legacy/provenance was consulted,
which owner route remains stronger, and whether any old flat adoption docs-root
reference remains.
