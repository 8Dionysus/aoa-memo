# AGENTS.md

## Applies To

This card applies to `mechanics/titan/`.

## Role

The Titan mechanic owns memo-side Titan recall candidates, remembrance source
refs, memory loom posture, audit memory policy, personality memory policy,
bridge digest, console digest, closeout posture, and swarm memory policy.

It does not grant memory write authority, role rights, proof status, private
retention, or owner-repo Titan doctrine.

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
python -m pytest -q mechanics/titan/tests/test_titan_remembrance_record.py mechanics/titan/tests/test_titan_candidate_schemas.py mechanics/titan/tests/test_titan_audit_memory_candidate.py
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
