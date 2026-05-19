# AGENTS.md

## Guidance for `.agents/`

`.agents/` is the agent-facing companion district for `aoa-memo`.

It may hold maintained agent lanes, exported skills, and local guidance that
helps agents work with memory-layer surfaces. It does not own memory truth.
Memory truth stays in source docs, schemas, examples, generated-source maps,
and validators.

## Route Stack

- Above: root `AGENTS.md` owns repository identity, owner boundaries, and
  release route.
- Here: `.agents/` owns agent-facing companion lanes only.
- Below: `skills/` holds exported skill companions and `spark/` narrows the
  fast-loop lane. Neither lane owns memory doctrine.

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
python .agents/spark/scripts/validate_spark_lane.py
python -m unittest discover -s .agents/spark/tests -p 'test*.py'
python -m pytest -q tests/root-topology/test_topology_spine.py
python scripts/release/release_check.py
```
