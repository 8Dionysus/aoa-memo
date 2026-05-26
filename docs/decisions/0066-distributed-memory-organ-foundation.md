# Decision: Memory-organ foundation lands in owner surfaces

- Decision ID: AOA-MEM-D-0066

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-24
- Legacy path: docs/decisions/2026-05-24-distributed-memory-organ-foundation.md
- Surface classes: root/topology
- Mechanic parents: none
- Guard families: docs route
- Memory object classes: decision
- Posture: active rationale

## Context

`aoa-memo` is moving from early contract hardening toward a working memory
organ for OS Abyss. The current pressure is not to add more abstract doctrine,
but to make the durable loops legible: local source events, reviewed intake,
object population, generated read models, MCP/access-plane compatibility,
consumer recall, lifecycle pressure, and quality evaluation handoff.

The repo already has strong owner surfaces for memory operation, living
topology, object profiles, consumer handoff, lifecycle, retention,
quest activation, and generated quest read models. Creating one large
foundation document would make the anatomy easier to see in one place, but it
would also compete with those surfaces and increase agent context load.

## Decision

Land the memory-organ foundation as a distributed layout across existing owner
surfaces instead of creating a new central foundation document.

The operating anatomy belongs in `docs/memory/MEMORY_OPERATION_CYCLE.md`.
Source lanes, owner routes, and port status posture belong in
`docs/memory/LIVING_MEMORY_TOPOLOGY.md`. Stable object population slots belong
in `docs/memory/MEMORY_OBJECT_PROFILES.md`. Consumer recall pack contracts and
quality harness posture belong in the consumer-handoff mechanic, with quality
execution routed to `aoa-evals`. Lifecycle and consolidation pressures stay in
their lifecycle and retention surfaces. Activation work is tracked as captured
quests and generated quest read models.

The foundation slice records what must become operational without moving
runtime authority, proof authority, routing authority, or eval ownership into
`aoa-memo`.

## Alternatives

- Create `docs/memory/MEMORY_ORGAN_FOUNDATION.md` as a single high-level
  document. Rejected because it would duplicate existing owner surfaces and
  invite future agents to update the summary instead of the source-owned lane.
- Start with validator refactoring. Rejected for this slice because the
  immediate goal was organ activation topology, not validator architecture.
- Put the quality harness directly inside `aoa-memo`. Rejected because
  `aoa-memo` owns memory contracts and reviewed memory surfaces, while
  `aoa-evals` owns portable proof and evaluation execution.
- Leave the foundation only in the final response or changelog. Rejected
  because future agents need durable route rationale, not only release notes.

## Consequences

- Agents can inspect the memory organ through the same surfaces they must
  later update.
- The route stays compatible with the project preference for operational maps:
  role, input, output, owner, next route, tools, and verification.
- The layout avoids a new doctrine hub, but readers must follow the decision
  record and affected-surface list to understand why the foundation is split.
- Activation backlog is explicit, but the backlog is not evidence that the
  loops are already closed.
- MCP compatibility, workspace port status, object population, lifecycle
  pressure, and quality lenses now have named next slices without changing
  their stronger owner boundaries.

## Affected Surfaces

- `docs/memory/MEMORY_OPERATION_CYCLE.md`
- `docs/memory/LIVING_MEMORY_TOPOLOGY.md`
- `docs/memory/MEMORY_OBJECT_PROFILES.md`
- `mechanics/consumer-handoff/docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md`
- `mechanics/consumer-handoff/docs/MEMORY_EVAL_GUARDRAILS.md`
- `docs/posture/LIFECYCLE.md`
- `mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md`
- `QUESTBOOK.md`
- `quests/memo/captured/AOA-MEM-Q-0010.yaml` through
  `quests/memo/captured/AOA-MEM-Q-0015.yaml`
- `generated/quests/quest_catalog.min.json`
- `generated/quests/quest_dispatch.min.json`

## Verification

Use:

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/memory/validate_memory_operations.py
python scripts/memory/validate_memo.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/validate_memory_object_surfaces.py
python scripts/memory/validate_lifecycle_audit_examples.py
python scripts/root-topology/validate_docs_districts.py
python -m pytest -q tests/memory tests/root-topology/test_docs_districts.py
python scripts/release_check.py
```
