# Reviewed Memory Consumer Handoff Spine

## Context

`aoa-memo` now has a reviewed `memo/objects/` corpus and generated
object-facing read models. The next memory-architecture layer needs neighboring
organs to consume reviewed memory without turning those organs into memory
authority or turning memo into proof, graph, stats, role, or scenario truth.

The immediate consumers are `aoa-evals`, `aoa-kag`, `aoa-stats`,
`aoa-playbooks`, and `aoa-agents`.

## Decision

Reviewed memory grows first as source-owned `memo/objects/` bundles, then as
generated read models, then as bounded consumer handoffs.

Consumer repositories should receive object ids, source refs, provenance
threads, lifecycle posture, recall status, and generated read-model handles.
They should not receive authority to rewrite or silently promote memo truth.

`aoa-stats` is explicitly added to the consumer-handoff owner split as the
owner of derived memory-movement summaries and trend aggregation. `aoa-memo`
may expose reviewed objects, indexes, receipts, and landing records as inputs,
but it does not own stats interpretation.

## Alternatives

- Let each consumer repository search and summarize `aoa-memo` directly.
  Rejected because it would duplicate authority and make recall behavior depend
  on local search accidents.
- Make MCP the shared memory writer. Rejected because MCP is an access plane,
  not durable memory authority.
- Add a broad neighbor-seams bucket. Rejected because each consumer operation
  needs its own stronger-owner boundary.

## Consequences

- Durable memory remains in `aoa-memo/memo/objects/`.
- Generated memory-object catalogs, capsules, and sections become the first
  shared read models for downstream consumers.
- `aoa-evals`, `aoa-kag`, `aoa-stats`, `aoa-playbooks`, and `aoa-agents` can
  build consumer-specific surfaces without claiming memory ownership.
- Future typed consumer examples should be added only after repeated consumer
  use proves a stable contract.

## Affected Surfaces

- `memo/objects/`
- `generated/memory-objects/`
- `mechanics/consumer-handoff/`
- `docs/memory/MEMORY_OPERATION_CYCLE.md`
- downstream consumer repositories that read reviewed memory objects

## Verification

Use:

```bash
python scripts/memory/validate_memo_corpus.py
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memo.py
python scripts/release/release_check.py
```
