# Consolidation and forgetting Validation

This file owns the focused invocation(s) shown here; the package route and the memory-operations validator add wider checks.

Shared executable routes remain owned by [`docs/memory/VALIDATION.md`](../../../../docs/memory/VALIDATION.md), [`mechanics/VALIDATION.md`](../../../VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python -m pytest -q mechanics/retention/parts/consolidation-and-forgetting/tests
python -m ruff check mechanics/retention/parts/consolidation-and-forgetting/scripts/active_organ_lifecycle.py mechanics/retention/parts/consolidation-and-forgetting/scripts/distributed_erasure.py mechanics/retention/parts/consolidation-and-forgetting/tests/test_active_organ_lifecycle.py mechanics/retention/parts/consolidation-and-forgetting/tests/test_distributed_erasure.py
```

Then follow the package-specific route in [`../../VALIDATION.md`](../../VALIDATION.md) for any changed source docs, schemas, examples, generated companions, scripts, tests, manifests, or owner routes.

The cross-owner Phase 10 failure-injection verdict lives in the
`aoa-evals` active-organ offline replay bundle. Its deterministic reference
runner must pin this owner script and all three schemas by digest and must
report no runtime mutation, deployment, or landing. That result proves only
the source-local mechanism; durable worker admission stays with
`abyss-stack`, projection work with `aoa-kag`, and future control-plane
admission with `aoa-sdk`.

The Phase 11 cross-owner reference verdict also lives in that bundle. Its
runner must validate the immutable memo C14-C17 base schema, memo recovery
probe, and exact owner-extension schemas from `aoa-memo`,
`aoa-session-memory`, `aoa-kag`, `abyss-stack`, `abyss-machine`, and the
synthetic eval/model owner. The A/B/C comparison and fault injection must keep
live deletion, raw-session deletion, model unlearning, runtime promotion, and
landing false. A complete synthetic closure may pass only the bounded
reference gate; any residue or extension/probe failure must block
private-memory deployment.
