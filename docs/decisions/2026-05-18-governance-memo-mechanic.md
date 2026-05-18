# 2026-05-18: Land Governance as a Memo Mechanic

Correction: `VIA_NEGATIVA_CHECKLIST.md` was later moved to
`mechanics/shape-guard/docs/` by
[2026-05-18-shape-guard-memo-mechanic](2026-05-18-shape-guard-memo-mechanic.md).
Governance remains the active authority-boundary memory mechanic.

## Context

Governance, federation, installation, certification, precedent, and stay-order
docs were still flat under `docs/`. `VIA_NEGATIVA_CHECKLIST.md` was also flat
at the time, but it is now treated as shape-guard material rather than
governance authority-boundary memory.

They were not core memory doctrine and not neighbor-seam implementation docs.
They shared a repeated mechanic shape: authority checks, owner consent,
reviewable gate outcomes, forgetting or expiry posture, source-owner
stop-lines, and handoff routes to stronger owners.

Keeping them flat made the docs root heavier and blurred the difference
between memory posture and actual governance, release, proof, role, KAG,
source-owner, Tree-of-Sophia, or runtime authority.

## Decision

Move the governance family into a memo mechanic package:

- `mechanics/governance/docs/`

The package gets a route card, mechanic card, direction, parts map, owner map,
provenance bridge, landing log, roadmap, docs subroute, and legacy route.
`config/memo_mechanics.json`, generated mechanics index coverage, AGENTS mesh
coverage, docs-district retirement checks, tests, and release validation become
the machine-checkable companion surface.

## Alternatives

- Keep the docs flat. This preserved old paths, but kept a repeatable
  authority-boundary mechanic hidden in the broad docs root.
- Fold governance into adoption or retention. Those mechanics consume some
  governance pressure, but they do not own federation, stay-order, precedent,
  installation, or certification memory posture as one authority-boundary
  route.
- Move incident, service, office, deployment, KAG, agent, playbook, or eval
  seams at the same time. Those are adjacent candidates, but they need separate
  owner maps before moving.

## Consequences

- Active governance-family docs now route through `mechanics/governance/`.
- Old flat `docs/*.md` paths for these surfaces are legacy provenance only.
- Service, office, deployment incident, post-release, KAG, agent, playbook, and
  eval seams remain flat or route to their existing owners until a validated
  district or mechanic exists.
- Stronger owner claims stay routed away: center governance to
  `Agents-of-Abyss`, authored meaning to `Tree-of-Sophia`, proof to
  `aoa-evals`, dispatch behavior to `aoa-routing`, role authority to
  `aoa-agents`, scenario choreography to `aoa-playbooks`, source-owner consent
  to the source repository, and runtime governance to `abyss-stack`.

## Affected Surfaces

- `mechanics/governance/`
- `config/memo_mechanics.json`
- `config/agents_mesh.json`
- `generated/memo_mechanics.min.json`
- `generated/agents_mesh.min.json`
- `scripts/validate_docs_districts.py`
- `scripts/validate_memo_mechanics.py`
- `mechanics/governance/tests/test_governance_mechanic.py`
- `tests/test_memo_mechanics.py`
- `tests/test_agents_mesh.py`
- `tests/test_docs_districts.py`

## Verification Route

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python -m pytest -q mechanics/governance/tests/test_governance_mechanic.py tests/test_memo_mechanics.py tests/test_agents_mesh.py tests/test_docs_districts.py
python scripts/release_check.py
```
