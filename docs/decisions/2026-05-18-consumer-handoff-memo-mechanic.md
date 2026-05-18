# 2026-05-18: Add Consumer Handoff as an Operation-First Memo Mechanic

## Context

After Agon, Titan, adoption, governance, shape-guard, writeback, and retention
were moved into operation-first memo mechanics, the remaining flat docs still
contained a visible neighbor-seam cluster:

- agent memory posture
- playbook memory scopes
- memory eval guardrails
- KAG/ToS bridge contract
- KAG source export
- orchestrator memory alignment

Keeping those files flat made them look like ordinary docs-root doctrine.
Moving them into a generic neighbor folder would have repeated the old mistake:
the shared noun is not the owner. The repeatable operation is safer and more
precise: publish memo-owned handoff surfaces so stronger consumer layers can
inspect, scope, evaluate, bridge, or orchestrate memory without absorbing memo
authority.

## Decision

Add `mechanics/consumer-handoff/` as the memo mechanic for bounded downstream
handoff surfaces.

Move these active docs from flat `docs/` into
`mechanics/consumer-handoff/docs/`:

- `AGENT_MEMORY_POSTURE_SEAM.md`
- `PLAYBOOK_MEMORY_SCOPES.md`
- `MEMORY_EVAL_GUARDRAILS.md`
- `KAG_TOS_BRIDGE_CONTRACT.md`
- `KAG_SOURCE_EXPORT.md`
- `ORCHESTRATOR_MEMORY_ALIGNMENT.md`

Keep their old flat paths only in `config/memo_mechanics.json`, this decision
record, and `mechanics/consumer-handoff/legacy/INDEX.md` as provenance.

Update the memo mechanics index, AGENTS mesh, generated registries, examples,
quest catalog refs, validators, and tests to treat the mechanic paths as the
active surfaces.

## Alternatives

- Leave the files flat. That would preserve path stability, but it would keep
  repeatable consumer handoffs in docs root after a validated mechanic route
  exists.
- Create a generic `docs/seams/` district. That would reduce root clutter, but
  it would not provide operation-first package cards, owner maps, legacy
  bridges, or mechanics validation.
- Split by consumer owner immediately. That would create many thin packages
  before the repeated memo operation is clearer than the downstream owner name.

## Consequences

- Consumer handoff becomes the local entry route when memo publishes surfaces
  for agents, playbooks, evals, KAG/ToS, KAG export, or orchestrator-facing
  quest families.
- `aoa-memo` stays responsible for memory descriptors, scopes, recall modes,
  bridge/export notes, and guardrail case descriptions.
- Stronger owners still own actor rights, scenario choreography, proof,
  graph normalization, Tree-of-Sophia source meaning, route dispatch, and
  runtime execution.
- Generated and example refs now point to the mechanic path, so stale flat
  route references should fail mechanics validation.

## Affected Surfaces

- `mechanics/consumer-handoff/`
- `mechanics/README.md`
- `config/memo_mechanics.json`
- `generated/memo_mechanics.min.json`
- `config/agents_mesh.json`
- `generated/agents_mesh.min.json`
- `generated/memo_registry.min.json`
- `generated/memory_catalog*.json`
- `generated/memory_capsules.json`
- `generated/memory_sections.full.json`
- `generated/memory_object_*.json`
- `generated/quest_catalog.min*.json`
- `generated/quest_dispatch.min*.json`
- `README.md`
- `docs/README.md`
- `docs/ROOT_SURFACE_LAW.md`
- `docs/MEMORY_MODEL.md`
- `quests/AOA-MEM-Q-0004.yaml`
- `quests/AOA-MEM-Q-0005.yaml`
- `quests/AOA-MEM-Q-0006.yaml`
- `scripts/validate_memo.py`
- `tests/test_consumer_handoff_mechanic.py`
- `tests/test_memo_mechanics.py`
- `tests/test_playbook_memory_scopes.py`

## Verification Route

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python -m pytest -q tests/test_consumer_handoff_mechanic.py tests/test_memo_mechanics.py tests/test_agents_mesh.py tests/test_playbook_memory_scopes.py tests/test_downstream_feed_contracts.py tests/test_memo_validators.py
python scripts/release_check.py
```
