# AGENTS.md

## Guidance for `docs/titan/`

`docs/titan/` owns memo-side Titan memory posture surfaces that were formerly
flat Titan docs-root files. In short: formerly flat Titan docs now route here.

This district keeps Titan recall candidates, remembrance source refs, memory
loom posture, audit memory policy, personality memory policy, bridge digest,
console digest, closeout posture, and swarm memory policy together. It does not
grant memory write authority, role rights, proof status, or private retention.

## Read Before Editing

Start with:

1. root `AGENTS.md`
2. `docs/AGENTS.md`
3. `docs/README.md`
4. `docs/ROOT_SURFACE_LAW.md`
5. this file
6. `docs/titan/README.md`
7. the target Titan doc plus matching schemas, examples, tests, and owner route
   refs when they exist

## Boundaries

- Keep Titan memory as candidate posture unless an owner confirms the stronger
  writeback.
- Do not persist sensitive personal data, private traces, or hidden retention
  decisions here.
- Do not turn recall candidates into policy, proof, role rights, or canonical
  owner-repo truth.
- Route agent authority to `aoa-agents`, proof to `aoa-evals`, runtime storage
  to `abyss-stack`, and authored source doctrine to the owning source repo.
- Keep refs pointed at `docs/titan/`, not old flat docs-root paths.

## Validation

For Titan district edits, run:

```bash
python scripts/validate_docs_districts.py
python -m pytest -q tests/test_titan_remembrance_record.py tests/test_titan_candidate_schemas.py tests/test_titan_audit_memory_candidate.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report which Titan memory posture changed, whether schemas, examples, or tests
changed, and whether any old flat Titan docs-root reference remains.
