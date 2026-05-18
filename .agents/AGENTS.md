# AGENTS.md

## Guidance for `.agents/`

`.agents/` is the agent-facing companion district for `aoa-memo`.

It may hold maintained agent lanes, exported skills, and local guidance that
helps agents work with memory-layer surfaces. It does not own memory truth.
Memory truth stays in source docs, schemas, examples, generated-source maps,
and validators.

## Current Lanes

| Lane | Use |
|---|---|
| `skills/` | exported skill companions used by agents working in this repository |
| `spark/` | fast-loop Spark lane for one bounded memory-layer surface at a time |

## Boundaries

- Do not treat agent companion files as source memory doctrine.
- Do not store private traces, secrets, hidden telemetry, or unreduced personal
  data here.
- Do not let agent lane language make memory look like proof, routing logic,
  role authority, KAG substrate, or runtime state.
- Keep maintained agent lanes under `.agents/<lane>/`, not as root civic
  surfaces.

## Verify

For `.agents/` route changes, run:

```bash
python -m pytest -q tests/test_topology_spine.py
python scripts/release_check.py
```
