# Decision: Move Spark Agent Lane Under `.agents`

Date: 2026-05-18

## Status

Accepted.

## Context

`aoa-memo` carried a maintained `Spark/` lane at repository root. That made the
root less convex: the lane is useful for fast-loop memory-layer work, but it is
not public layer law, platform governance, a schema district, or memory
doctrine.

The new topology spine already establishes that maintained agent lanes belong
under `.agents/<lane>/` and that root surfaces should stay limited to public
entry, layer authority, governance, thin indexes, tooling districts, and agent
route law.

## Decision

Move root `Spark/` to `.agents/spark/`.

Keep the lane's current scope: one bounded memory-layer surface at a time,
with explicit provenance, temporal posture, and validation.

Add `.agents/AGENTS.md` so the agent-facing companion district has its own
local route card.

## Alternatives Considered

### Keep `Spark/` at root

Rejected. The lane is maintained agent guidance, not a root civic surface.
Keeping it at root would preserve avoidable topology noise.

### Delete the Spark lane

Rejected. The lane still has a useful bounded role for short-loop memory
surface work.

### Move Spark while starting a full AGENTS mesh

Rejected for this slice. The AGENTS mesh should be a separate validated
generated companion when the repo is ready to register all local cards.

## Consequences

- Root is less noisy.
- `.agents/` now has a local route card.
- Spark lane references must use `.agents/spark/`.
- Future AGENTS mesh work can treat `.agents/spark/` as the durable lane home.

This change does not move flat `docs/` surfaces and does not introduce a
generated AGENTS mesh.

## Boundaries

Spark remains a fast-loop helper. It does not own memory truth, proof, routing,
role policy, KAG substrate, or runtime state.

## Verification Route

Use:

```bash
python -m pytest -q tests/test_topology_spine.py
python scripts/release_check.py
```
