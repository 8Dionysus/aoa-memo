# AGENTS.md

## Guidance for `mechanics/titan/docs/`

`mechanics/titan/docs/` owns active mechanic-owned doctrine and support notes
for the Titan memo mechanic.

This docs route keeps Titan recall candidates, remembrance source refs, memory
loom posture, audit memory policy, personality memory policy, bridge digest,
console digest, closeout posture, and swarm memory policy together. It does
not grant memory write authority, role rights, proof status, or private
retention.

## Read Before Editing

Start with:

1. root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `mechanics/ARTIFACT_TOPOLOGY.md`
4. `mechanics/titan/AGENTS.md`
5. `mechanics/titan/README.md`
6. `mechanics/titan/PARTS.md`
7. `mechanics/titan/OWNER_MAP.md`
8. `mechanics/titan/PROVENANCE.md`
9. this file
10. `mechanics/titan/docs/README.md`
11. the target Titan doc plus matching schemas, examples, tests, and owner route
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
- Keep refs pointed at `mechanics/titan/docs/`, not old flat docs-root or
  transitional docs-district paths.
- Do not add root technical artifacts here; use the artifact topology rule
  before moving schemas, examples, generated outputs, scripts, or tests.

## Validation

For Titan district edits, run:

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q tests/test_titan_remembrance_record.py tests/test_titan_candidate_schemas.py tests/test_titan_audit_memory_candidate.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report which Titan memory posture changed, whether schemas, examples, or tests
changed, and whether any old Titan docs-root or docs-district reference
remains outside allowed provenance.
