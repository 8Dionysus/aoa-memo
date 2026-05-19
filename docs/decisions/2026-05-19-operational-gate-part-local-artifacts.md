# Operational Gate Part-Local Artifacts

## Status

Accepted on 2026-05-19.

## Context

Operational-gate already had functioning parts for deployment incidents,
office/service incidents, service revision ledgers, and post-release
boundaries. Its schemas, examples, and local regressions still lived at the
package level under `mechanics/operational-gate/{schemas,examples,tests}`.

That left the parts descriptive while the executable admission contracts sat
one layer above the operations that owned them. For OS Abyss, operational
memory admission needs the schema, example, and regression close to the part
that owns the stop-lines.

## Decision

Move operational-gate technical artifacts to the nearest functioning part:

- deployment incident gate and deployment lesson candidate contracts plus the
  package boundary regression under
  `mechanics/operational-gate/parts/deployment-incident-gate/`
- service incident memory entry contracts under
  `mechanics/operational-gate/parts/office-incident-gate/`
- service revision ledger entry contracts under
  `mechanics/operational-gate/parts/service-revision-ledger/`
- train release memory entry contracts and the post-release-boundary contract regression under
  `mechanics/operational-gate/parts/post-release-boundaries/`

Keep release revision ledger and rollback memory entry contracts in writeback,
and keep retention marker contracts in retention. Operational-gate consumes
those neighboring contracts only as boundary checks.

## Alternatives

Leaving the artifacts under package-level `schemas/`, `examples/`, and `tests/`
would preserve shorter paths but keep the part structure decorative.

Moving every contract into deployment incident gate would reduce path variety
but would blur deployment incidents, office/service incidents, service
revision recall, and post-release release-train memory.

Creating a generic `technical-contracts` part would centralize files while
weakening the operation-first naming that mechanics rely on.

## Consequences

The operational-gate artifact inventory should now report all operational-gate
schemas, examples, and tests as `scope: part`. Package-level artifact homes are
provenance only, not active routes.

Post-release boundary validation still covers retention, governance,
writeback, rollback, and operational-gate contracts, but operational-gate
contracts are now owned by their nearest parts.

The move keeps `aoa-memo` below stronger owners. It does not grant release
approval, current service health, incident root-cause truth, runtime
remediation, proof verdicts, role rights, route dispatch, stats truth,
Tree-of-Sophia runtime writes, or source-owner acceptance.

## Affected Surfaces

- `mechanics/operational-gate/PARTS.md`
- `mechanics/operational-gate/PROVENANCE.md`
- `mechanics/operational-gate/parts/*`
- `mechanics/operational-gate/AGENTS.md`
- `mechanics/operational-gate/docs/AGENTS.md`
- `mechanics/operational-gate/docs/DEPLOYMENT_INCIDENT_MEMORY_GATE.md`
- `mechanics/operational-gate/docs/OFFICE_INCIDENT_MEMORY_GATE.md`
- `mechanics/operational-gate/docs/SERVICE_REVISION_LEDGER.md`
- `config/root_technical_districts.json`
- `generated/agents_mesh.min.json`
- `generated/mechanic_artifacts.min.json`
- `generated/memo_mechanic_landing_logs.min.json`
- `generated/memo_mechanic_readiness.min.json`
- `generated/memo_registry.min.json`

## Verification

Expected verification:

- `python -m pytest -q mechanics/operational-gate/parts/deployment-incident-gate/tests mechanics/operational-gate/parts/post-release-boundaries/tests tests/test_memo_mechanics.py tests/test_agents_mesh.py`
- `python scripts/build_mechanic_artifact_inventory.py --check`
- `python scripts/validate_mechanic_artifact_inventory.py`
- `python scripts/validate_memo_mechanic_parts.py`
- `python scripts/build_memo_mechanic_readiness.py --check`
- `python scripts/validate_memo_mechanic_readiness.py`
- `python scripts/validate_memo.py`
- `python scripts/release_check.py`
