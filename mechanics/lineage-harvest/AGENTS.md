# AGENTS.md

## Applies To

This card applies to `mechanics/lineage-harvest/` until a nearer `AGENTS.md`
narrows the lane.

## Role

`mechanics/lineage-harvest/` is the memo-side lineage-harvest mechanic.

It owns reviewable pattern-lineage memory posture for cross-repo recurring
signals: what may enter as owner-local evidence, what may become a bounded
lineage candidate, what gates must remain visible, and which stronger owner
receives the next claim.

It is not the federation authority, proof layer, KAG promoter, stats judge,
Tree-of-Sophia canon route, source owner, runtime watchtower, or adoption
engine.

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

Read:

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `mechanics/README.md`
5. `mechanics/ARTIFACT_TOPOLOGY.md` when schemas, examples, generated outputs,
   tests, or quests may move
6. this package `README.md`
7. `DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and `PROVENANCE.md`
8. `docs/AGENTS.md` before editing active lineage-harvest docs
9. `legacy/AGENTS.md` before editing placement history

## Boundaries

- Active lineage-harvest docs live under `mechanics/lineage-harvest/docs/`.
- Lineage-harvest schemas, examples, and tests stay under
  `mechanics/lineage-harvest/` when they belong only to this mechanic.
  Root technical districts are for shared or cross-mechanic contracts.
- The former flat docs-root `PATTERN_LINEAGE_MEMORY.md` placement is
  provenance only. Do not restore it as an active alias.
- Governance, writeback, retention, and adoption mechanics keep their adjacent
  operations; this package only owns the pattern-lineage memory gate.
- Route federation program law to `Agents-of-Abyss`, proof to `aoa-evals`,
  derived graph promotion to `aoa-kag`, recurrence summaries to `aoa-stats`,
  authored meaning to `Tree-of-Sophia`, runtime incidents to `abyss-stack`, and
  owner consent to the source repository.

## Validation

For lineage-harvest changes, run:

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
```

For release-bound work, also run:

```bash
python scripts/release/release_check.py
```

## Closeout

Report whether active docs, owner map, provenance, legacy bridge, schema and
example refs, generated companions, tests, and old flat docs-root references
changed. Name any stronger owner route that was deliberately left outside
`aoa-memo`.
