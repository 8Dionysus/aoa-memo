# AGENTS.md

## Guidance for `mechanics/titan/docs/`

`mechanics/titan/docs/` owns active mechanic-owned doctrine and support notes
for the Titan memo mechanic.

This docs route keeps Titan recall candidates, remembrance source refs, memory
loom posture, audit memory policy, personality memory policy, bridge digest,
console digest, closeout posture, and swarm memory policy together. It does
not grant memory write authority, role rights, proof status, or private
retention.

## Route Stack

- Above: the package `AGENTS.md`, `README.md`, `PARTS.md`, and `OWNER_MAP.md`
  set the operation and stronger-owner split.
- Here: `docs/README.md` maps the source family; individual docs own active
  mechanic doctrine and support notes.
- Adjacent: package or part artifact homes own schemas, examples, config,
  generated outputs, scripts, tests, manifests, and quests. Use
  `mechanics/ARTIFACT_TOPOLOGY.md` before moving root technical artifacts.
- Below: no nested active law is expected here; legacy context routes through
  `../PROVENANCE.md` and `../legacy/`.

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
- When a Titan source family changes, keep source refs in part-local examples,
  schemas, and tests aligned with this district rather than editing the doc as
  an isolated note.

## Validation

For Titan district edits, run:

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python -m pytest -q mechanics/titan/parts/recall-and-remembrance-posture/tests mechanics/titan/parts/closeout-and-digest-posture/tests mechanics/titan/parts/audit-personality-and-swarm-policy/tests
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report which Titan memory posture changed, whether schemas, examples, or tests
changed, and whether any old Titan docs-root or docs-district reference
remains outside allowed provenance.
