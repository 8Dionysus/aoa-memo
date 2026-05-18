# 2026-05-18: Add Shape Guard as an Operation-First Memo Mechanic

## Context

The governance mechanic landing moved `VIA_NEGATIVA_CHECKLIST.md` into
`mechanics/governance/docs/`.

That placement was too thematic. The checklist does not govern council,
federation, installation, certification, precedent, or stay-order memory. It
asks whether new memory objects, trust fields, recall families, mechanic
packages, or action-facing memory routes should exist at all.

For OS Abyss readiness, `aoa-memo` needs mechanics that can be used repeatedly
by tools and agents without turning topic clusters into authority. The missing
rule was operation-first validation: each mechanic package must name the
memory operation it performs, not only a subject area.

## Decision

Add `mechanics/shape-guard/` as the memo mechanic for via-negativa memory-shape
review.

Move `VIA_NEGATIVA_CHECKLIST.md` to
`mechanics/shape-guard/docs/VIA_NEGATIVA_CHECKLIST.md`.

Upgrade `config/memo_mechanics.json` and the generated mechanics index to v2 by
requiring every package to name:

- `operation`
- `os_abyss_role`

Require every package README to include `### Operation`, and validate that the
configured operation is cited by the package card.

Governance remains a mechanic, but it is narrowed to authority-boundary memory:
governance, federation, installation, certification, precedent, and stay-order
memory without decision authority.

## Alternatives

- Move `VIA_NEGATIVA_CHECKLIST.md` back to flat `docs/`. That would remove the
  governance error, but it would leave the anti-inflation operation without a
  package card, owner map, legacy bridge, generated index, or AGENTS mesh route.
- Fold via-negativa into antifragility. That matches the center-level AoA
  antifragility neighborhood, but in `aoa-memo` this checklist is broader than
  failure and recovery memory. It applies before adding any memory shape.
- Keep it in governance. That would preserve fewer links, but it would keep a
  general memory-shape operation inside an authority-boundary topic.

## Consequences

- Memo mechanics now have an explicit operation field in config, generated
  companions, package cards, and validator expectations.
- `shape-guard` becomes the local entry route when new memory forms risk proof,
  health, trust, action, owner-adoption, or topic-bucket inflation.
- Governance no longer owns the via-negativa checklist.
- The generated mechanics index schema moves from
  `aoa_memo_mechanics_index_v1` to `aoa_memo_mechanics_index_v2`.
- Future mechanics growth should fail review when it cannot name a repeatable
  memory operation and stronger-owner route.

## Affected Surfaces

- `mechanics/README.md`
- `mechanics/AGENTS.md`
- `mechanics/shape-guard/`
- `mechanics/governance/`
- `config/memo_mechanics.json`
- `generated/memo_mechanics.min.json`
- `config/agents_mesh.json`
- `generated/agents_mesh.min.json`
- `scripts/memo_mechanics_common.py`
- `scripts/validate_memo_mechanics.py`
- `scripts/validate_memo_mechanics_index.py`
- `mechanics/shape-guard/tests/test_shape_guard_mechanic.py`
- `mechanics/governance/tests/test_governance_mechanic.py`
- `tests/test_memo_mechanics.py`
- `tests/test_agents_mesh.py`

## Verification Route

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python -m pytest -q mechanics/shape-guard/tests/test_shape_guard_mechanic.py mechanics/governance/tests/test_governance_mechanic.py tests/test_memo_mechanics.py tests/test_agents_mesh.py
python scripts/release_check.py
```
