# Decision: Spark Registry-Backed Memo Lane

- Decision ID: AOA-MEM-D-0059

Date: 2026-05-19

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-19
- Legacy path: docs/decisions/2026-05-19-spark-registry-backed-memo-lane.md
- Surface classes: generated/readout, agents/mesh
- Mechanic parents: none
- Guard families: AGENTS/mesh
- Memory object classes: none
- Posture: active rationale

## Context

`aoa-memo` had already moved its maintained Spark lane under `.agents/spark/`,
but the lane still contained only a local route card and swarm recipe. That
kept the root convex, but it did not give repeated Codex Spark work a
machine-checkable entry shape.

`Agents-of-Abyss` proved the stronger pattern: a Spark lane is agent-facing
launch, result, handoff, validation, and scenario material with a
`done-or-handoff` contract. `aoa-techniques` and `aoa-skills` adapted that
pattern into their own canon boundaries instead of copying center doctrine.

OpenAI's public Spark framing also matters: GPT-5.3-Codex-Spark is designed
for real-time, interruptible, targeted coding work. It should not be treated as
a smaller clone of a long-running Codex agent.

## Decision

Build `.agents/spark/` as a registry-backed Codex Spark lane for `aoa-memo`.

The lane owns:

- `.agents/spark/README.md`
- `.agents/spark/SPARK_EXTRAPOLATION_NOTEBOOK.md`
- `.agents/spark/registry.json`
- scenario packets under `.agents/spark/scenarios/`
- result and handoff homes under `.agents/spark/results/` and
  `.agents/spark/handoffs/`
- schemas under `.agents/spark/schemas/`
- `.agents/spark/scripts/validate_spark_lane.py`
- `.agents/spark/tests/test_spark_lane.py`

The registered scenarios are memo-specific:

- `memory-audit`
- `memory-refinement`
- `recall-contract-check`
- `generated-parity-check`
- `mechanic-seam-scout`
- `diff-review`
- `registry-sync`
- `test-factory`
- `release-prep`

## Consequences

- Spark sessions in this repo choose one registered scenario and finish as
  `done` or `handoff`.
- New scenarios must be registered and validated.
- `scripts/release_check.py` runs Spark lane validation and Spark lane tests.
- Ordinary Spark scenario work should stay lightweight and run the explicit
  narrow validation named by the user, scenario, or repo law.
- Spark remains subordinate to memory source docs, schemas, examples,
  mechanics, generated-source builders, validators, and sibling-owner
  repositories.
- Scenario shape is validated; scenario judgment still requires human or agent
  review in the actual task.

## Affected Surfaces

- `.agents/AGENTS.md`
- `.agents/spark/AGENTS.md`
- `.agents/spark/README.md`
- `.agents/spark/SWARM.md`
- `.agents/spark/SPARK_EXTRAPOLATION_NOTEBOOK.md`
- `.agents/spark/registry.json`
- `.agents/spark/scenarios/**`
- `.agents/spark/scripts/validate_spark_lane.py`
- `.agents/spark/tests/test_spark_lane.py`
- `DESIGN.AGENTS.md`
- `scripts/release_check.py`
- `generated/agents_mesh.min.json`

## Verification Route

Use:

```bash
python .agents/spark/scripts/validate_spark_lane.py
python -m unittest discover -s .agents/spark/tests -p 'test*.py'
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/release_check.py
```
