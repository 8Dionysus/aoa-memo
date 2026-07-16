# AGENTS.md

## Guidance for `.agents/`

`.agents/` is the agent-facing derived district for `aoa-memo`.

It holds maintained agent lanes and the exact generated projection of admitted
owner skills. It does not own memory or skill truth. Memory truth stays in
source docs, schemas, examples, generated-source maps, and validators; skill
truth stays under top-level `skills/`.

## Route Stack

- Above: root `AGENTS.md` owns repository identity, owner boundaries, and
  release route.
- Here: `.agents/` owns derived agent-facing lanes only.
- Below: `skills/aoa-memo/` is the generated Codex projection declared by
  `skills/port.manifest.json`; `spark/` narrows the fast-loop lane. Neither
  lane owns memory doctrine.

## Current Lanes

| Lane | Use |
|---|---|
| `skills/aoa-memo/` | exact generated projection of canonical `skills/aoa-memo/` |
| `spark/` | fast-loop Spark lane for one bounded memory-layer surface at a time |

## Boundaries

- Do not treat agent companion files as source memory doctrine.
- Do not edit the generated owner skill projection directly or copy the shared
  skill catalog into this repository.
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
