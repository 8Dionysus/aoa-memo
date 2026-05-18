# 2026-05-18: Land Antifragility as a Memo Mechanic

## Context

Failure lesson and recovery pattern docs were still flat under `docs/` even
though they already had mechanic traits: repeatable creation triggers, recall
rules, source-ref requirements, suppression posture, schemas, examples,
generated object surfaces, tests, and stronger-owner stop-lines.

Keeping them flat made the docs root heavier and blurred the difference
between memory posture and stronger proof, route, stats, source, playbook, or
runtime authority.

## Decision

Move the antifragility family into a memo mechanic package:

- `mechanics/antifragility/docs/`

The package gets a route card, mechanic card, direction, parts map, owner map,
provenance bridge, landing log, roadmap, docs subroute, and legacy route.
`config/memo_mechanics.json`, generated mechanics index coverage, AGENTS mesh
coverage, docs-district retirement checks, tests, and release validation become
the machine-checkable companion surface.

## Alternatives

- Keep the docs flat. This preserved old paths, but kept a repeatable memory
  mechanic hidden in the broad docs root.
- Fold antifragility into writeback. This would overmix capture/return lanes
  with failure-lesson and recovery-pattern recall posture.
- Route antifragility to `aoa-evals`, `aoa-stats`, or `aoa-routing`. Those
  owners may consume the memory, but they own stronger proof, summaries, and
  dispatch behavior, not the memo object's source-linked recall posture.

## Consequences

- Active failure-lesson and recovery-pattern docs now route through
  `mechanics/antifragility/`.
- Old flat `docs/*.md` paths for these surfaces are legacy provenance only.
- Schemas, examples, generated object surfaces, and tests remain in root
  technical districts until `mechanics/ARTIFACT_TOPOLOGY.md` warrants a
  package-local artifact move.
- Stronger owner claims stay routed away: proof to `aoa-evals`, derived
  summaries to `aoa-stats`, dispatch behavior to `aoa-routing`, scenario
  choreography to `aoa-playbooks`, source receipts to owner repositories, and
  runtime repair to `abyss-stack`.

## Affected Surfaces

- `mechanics/antifragility/`
- `config/memo_mechanics.json`
- `config/agents_mesh.json`
- `generated/memo_mechanics.min.json`
- `generated/agents_mesh.min.json`
- `generated/memory_object_*.json`
- `generated/memo_registry.min.json`
- `scripts/validate_memo.py`
- `scripts/validate_memo_mechanics.py`
- `tests/test_antifragility_failure_lessons.py`
- `tests/test_antifragility_recovery_patterns.py`
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
python -m pytest -q tests/test_antifragility_failure_lessons.py tests/test_antifragility_recovery_patterns.py
python scripts/release_check.py
```
