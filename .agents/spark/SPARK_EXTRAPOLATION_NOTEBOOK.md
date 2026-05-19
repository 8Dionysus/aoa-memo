# Spark Extrapolation Notebook

This notebook records the adaptation pass that upgrades `aoa-memo`
`.agents/spark/` from a two-file helper lane into a registry-backed Codex Spark
lane.

It is not the daily authority for Spark use. The active contract lives in
`AGENTS.md`, `README.md`, `registry.json`, scenario packets, the validator, and
tests.

## Source Studied

Primary pattern:

- `Agents-of-Abyss/.agents/AGENTS.md`
- `Agents-of-Abyss/.agents/spark/AGENTS.md`
- `Agents-of-Abyss/.agents/spark/README.md`
- `Agents-of-Abyss/.agents/spark/SWARM.md`
- `Agents-of-Abyss/.agents/spark/registry.json`
- `Agents-of-Abyss/.agents/spark/scenarios/**`
- `Agents-of-Abyss/.agents/spark/schemas/**`
- `Agents-of-Abyss/.agents/spark/scripts/validate_spark_lane.py`
- `Agents-of-Abyss/.agents/spark/tests/test_spark_lane.py`
- `Agents-of-Abyss/docs/decisions/2026-04-30-spark-session-lane-contract.md`
- `Agents-of-Abyss/docs/decisions/2026-05-13-codex-spark-agent-lane-home.md`

Sibling adaptations:

- `aoa-techniques/.agents/spark/**`
- `aoa-techniques/docs/decisions/2026-05-15-spark-registry-backed-technique-lane.md`
- `aoa-skills/.agents/spark/**`
- `aoa-skills/docs/decisions/2026-05-18-codex-spark-agent-lane-home.md`

Local constraints:

- `AGENTS.md`
- `CHARTER.md`
- `DESIGN.md`
- `DESIGN.AGENTS.md`
- `.agents/AGENTS.md`
- `.agents/spark/AGENTS.md`
- `.agents/spark/SWARM.md`
- `MEMORY_INDEX.md`
- `docs/BOUNDARIES.md`
- `docs/MEMORY_MODEL.md`
- `docs/ROOT_SURFACE_LAW.md`
- `mechanics/README.md`
- `docs/decisions/2026-05-18-spark-agent-lane-home.md`

## Pattern Preserved

The center pattern is not just prompt text.

1. `.agents/spark/` is the durable home.
2. Spark is Codex-model-facing agent material, not a mechanic package or root
   district.
3. A Spark loop chooses one registered scenario and one bounded scope.
4. The core rule is `done-or-handoff`.
5. Each scenario has `README.md`, `PROMPT.md`, result and handoff templates,
   and one result example.
6. The registry names scenario paths, prompt refs, packet refs, default
   validation, done signal, and stop-line.
7. Results and handoffs have explicit homes, but ordinary closeout stays in
   the conversation or PR unless a packet helps future sessions.
8. Validation checks registry shape, scenario files, packet markers,
   registered-vs-discovered parity, packet directories, and release-check
   wiring.

The important design move is registry-backed boundedness. The lane is useful
because a future Spark session can start, finish, or hand off without inventing
its own route.

## Web Calibration

OpenAI describes GPT-5.3-Codex-Spark as a research-preview, smaller
GPT-5.3-Codex variant designed for real-time coding in Codex. The official
Spark framing emphasizes targeted edits, reshaping logic, refining interfaces,
interruptible real-time collaboration, a lightweight default style, and not
automatically running tests unless asked.

OpenAI also frames mainline GPT-5.3-Codex as stronger for long-running tasks
that involve research, tool use, and complex execution. Local consequence:
Spark should not behave like a smaller copy of a long-running Codex agent. It
should preserve one-scenario, one-scope, done-or-handoff operation, with narrow
validation named explicitly.

References:

- [OpenAI: Introducing GPT-5.3-Codex-Spark](https://openai.com/index/introducing-gpt-5-3-codex-spark/)
- [OpenAI: Introducing GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/)
- [OpenAI Help: Codex rate card](https://help.openai.com/en/articles/20001106-codex-rate-card)
- [OpenAI Developers: Codex CLI](https://developers.openai.com/codex/cli)

## Memo Adaptation

`aoa-memo` cannot copy center, technique, or skill scenarios blindly. This
repository owns explicit memory and recall objects, not center doctrine,
technique canon, skill workflows, proof reports, route dispatch, role
authority, KAG substrate, playbook choreography, or runtime state.

Spark here should help with:

- read-only memory audits;
- one-surface memory refinements;
- recall-contract and temporal-posture checks;
- source-builder-generated parity checks;
- mechanic seam scouting before deeper part-local work;
- concrete diff review;
- Spark registry and lane-contract sync;
- small tests for existing memory contracts;
- release-prep checks before publication or landing.

Spark must not:

- make memory look like proof;
- smuggle private traces, raw logs, host paths, secrets, or unreduced personal
  context into public packets;
- promote generated companions into source authority;
- move mechanic law into the agent lane;
- invent validation commands not named by the owner surface;
- absorb neighboring owner meaning from `aoa-techniques`, `aoa-skills`,
  `aoa-evals`, `aoa-routing`, `aoa-agents`, `aoa-kag`, `aoa-playbooks`,
  `Tree-of-Sophia`, or `abyss-stack`.

## Local Shape

The adapted lane owns:

```text
.agents/spark/
  AGENTS.md
  README.md
  SWARM.md
  SPARK_EXTRAPOLATION_NOTEBOOK.md
  registry.json
  handoffs/
  results/
  scenarios/
    memory-audit/
    memory-refinement/
    recall-contract-check/
    generated-parity-check/
    mechanic-seam-scout/
    diff-review/
    registry-sync/
    test-factory/
    release-prep/
  schemas/
  scripts/validate_spark_lane.py
  tests/test_spark_lane.py
```

## Future Rule

If Spark scenarios start carrying durable memory doctrine, move that doctrine
to the owning docs, mechanic, schema, example, generator, validator, or sibling
repository. If the lane becomes model-agnostic, make a new decision before
renaming `.agents/spark/`.
