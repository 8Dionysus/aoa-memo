# Reviewed corpus bridge for the ToS lineage KAG donor

## Memory
The KAG/ToS bridge candidate is now a reviewed corpus object. `aoa-kag` should consume the donor through the object-facing read models, where this object appears as `source_kind: reviewed_corpus`, rather than treating the bridge teaching fixture as durable memo truth.

## Source Route
- `mechanics/consumer-handoff/docs/KAG_SOURCE_EXPORT.md`
- `mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md#end-to-end-flow`
- `mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/bridge.kag-lift.example.json`
- `repo:aoa-kag/docs/decisions/2026-05-22-owner-route-catalog-refresh.md`
- `repo:aoa-kag/generated/federation_export_registry.min.json`

## Review Posture
This bridge is confirmed as reviewed memo corpus, but its KAG lift posture remains `candidate`. The object is safe for lineage and source-route recall; it is not normalized graph truth, proof, routing activation, or Tree-of-Sophia source meaning.

## Next Routes
- Route graph normalization and federation activation to `aoa-kag`.
- Route source-authored meaning to `Tree-of-Sophia`.
- Route proof of recall or bridge fidelity to `aoa-evals`.
- Keep memo read-model publication in `aoa-memo`.
