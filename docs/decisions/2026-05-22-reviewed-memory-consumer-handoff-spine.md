# Reviewed Memory Consumer Handoff Spine

- Decision ID: AOA-MEM-D-0065

## Index Metadata

- Surface classes: reviewed corpus, consumer handoff
- Mechanic parents: consumer-handoff
- Guard families: reviewed corpus/intake
- Memory object classes: none
- Posture: active rationale

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

Consumer repositories with a local `memo/` port may create candidates,
receipts, exports, and local records only inside that repo-local port. Route-only
consumers must not invent hidden local write paths. Session evidence remains in
`.aoa` or another owner evidence surface until reviewed intake lands as a
source change in `aoa-memo`.

The `aoa_memo` MCP plane may help with brief, search, status, validation, local
candidate preparation, intake packet preparation, reviewed-intake inspection,
and landing-plan dry runs. It does not become durable reviewed memory
authority. `aoa_memo_landing_plan` can prepare a source patch plan; the actual
durable landing is still a reviewed `aoa-memo/memo/objects/` source change.

The stable route is: retrieve reviewed objects or generated read models, capture
new evidence locally, export reviewed candidates from local ports when present,
land accepted reviewed intake in `aoa-memo`, then retrieve the resulting object
ids and generated surfaces.

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
- Consumers can retrieve reviewed memory through generated read models or the
  MCP access plane, but any new durable memory follows local candidate/export
  lanes into reviewed intake and checked source patches.
- Future typed consumer examples should be added only after repeated consumer
  use proves a stable contract.

## Affected Surfaces

- `memo/objects/`
- `generated/memory-objects/`
- `mechanics/consumer-handoff/`
- `docs/memory/MEMORY_OPERATION_CYCLE.md`
- `docs/memory/LOCAL_MEMO_PORT_STANDARD.md`
- repo-local `memo/` ports in downstream consumers
- `.aoa` session evidence surfaces
- `aoa_memo` MCP access-plane tools
- downstream consumer repositories that read reviewed memory objects

## Verification

Use:

```bash
python scripts/memory/validate_memo_corpus.py
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/memory/validate_memo.py
python scripts/release/release_check.py
```
