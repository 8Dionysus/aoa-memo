# AGENTS.md

## Applies To

This card applies to `mechanics/operational-gate/`.

## Role

The operational-gate mechanic owns memo-side memory admission for operational
incidents, office/service events, untrusted or derived write attempts, service
revisions, release-train memory, and post-release boundary surfaces.

It decides how `aoa-memo` preserves operational memory as public, reviewable,
source-linked recall. It does not decide releases, execute runtime changes,
prove incidents, grant service rights, route live traffic, or summarize current
operational health.

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
that reference operational-gate docs, read the nearest local `AGENTS.md`
before editing that district.

## Boundaries

- Keep operational-gate docs memory-only, evidence-linked, and
  operation-first.
- Do not claim release approval, current service health, incident root cause,
  runtime remediation, eval verdicts, service role rights, route dispatch, ToS
  runtime writes, or owner acceptance.
- Keep old flat docs-root paths out of active references except in provenance,
  legacy, decisions, and former-path source maps.
- Do not move public schemas or examples into this package unless the artifact
  topology rule proves they are single-mechanic-owned.
- Keep retention outcomes with the retention mechanic and writeback return
  lanes with the writeback mechanic unless this package is only deciding the
  admission gate.

## Post-Change Review

After operational-gate changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- part-local contract refs in `mechanics/operational-gate/parts/*/{schemas,examples,tests}/`
  and adjacent writeback/retention package refs
- generated mechanics or AGENTS mesh companions
- docs-root maps, root route cards, decision records, changelog, or roadmap

Update only surfaces whose future-facing meaning changed.

## Validation

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_operations.py
python -m pytest -q mechanics/operational-gate/parts/deployment-incident-gate/tests mechanics/operational-gate/parts/write-path-guardrails/tests mechanics/operational-gate/parts/post-release-boundaries/tests tests/mechanics/test_memo_mechanics.py tests/agents/test_agents_mesh.py
```

Before landing, also run:

```bash
python scripts/release/release_check.py
```

## Closeout

Report the operational-gate docs changed, whether mechanic-local artifacts and
adjacent package refs stayed owner-routed, whether old flat docs-root references
remain only as allowed provenance, and which stronger owner boundaries stayed
outside `aoa-memo`.
