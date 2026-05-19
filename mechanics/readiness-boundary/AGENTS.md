# AGENTS.md

## Applies To

This card applies to `mechanics/readiness-boundary/`.

## Role

The readiness-boundary mechanic owns memo-side admission posture for
high-pressure memory questions: future durable consequences, deltas,
retention pressure, recall anchors, contradiction pressure, bridge candidates,
and service traces.

It keeps those pressures mapped to existing memory objects and stronger owner
routes. It does not own proof, runtime retention, live ledgers, graph
normalization, route dispatch, role rights, or new memory object families.

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

For source docs, continue through `docs/AGENTS.md` and the target `docs/*.md`
surface.

For schemas, examples, generated outputs, scripts, tests, quests, or manifests
that reference readiness boundary posture, read the nearest local `AGENTS.md`
before editing that district.

## Boundaries

- Keep readiness-boundary surfaces memory-only, evidence-linked, and
  operation-first.
- Do not claim proof, runtime retention, live ledger state, role authority,
  route dispatch, KAG substrate truth, or owner acceptance.
- Do not create a new scar, readiness, survivor, or checkpoint-only memory
  object family from this package.
- Keep pressure mapping tied to existing memory objects and explicit owner
  routes.
- Keep writeback and checkpoint details with their own mechanics; this package
  may cite them as boundary outputs only.

## Post-Change Review

After readiness-boundary changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- readiness-boundary docs, schemas, examples, and tests
- generated object surfaces and memo registry refs
- root route cards, docs maps, decision records, changelog, or roadmap

Update only surfaces whose future-facing meaning changed.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/validate_memo.py
python -m pytest -q mechanics/readiness-boundary/parts/memory-readiness-boundary/tests/test_readiness_boundary_mechanic.py tests/test_memo_validators.py tests/test_current_direction_routes.py tests/test_mechanic_artifact_topology.py tests/test_memo_mechanics.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report readiness-boundary docs changed, whether contract artifacts stayed
owner-routed, whether old root doc/schema/example/test refs remain, and which
stronger owner boundaries stayed outside `aoa-memo`.
