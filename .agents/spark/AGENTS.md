# AGENTS.md

## Applies to

This card applies to `.agents/spark/` and every nested path under that scope
until a nearer `AGENTS.md` narrows the lane.

This lane only governs work started from `.agents/spark/`.

## Role

`.agents/spark/` is the fast, interruptible Codex Spark lane for `aoa-memo`.
It is calibrated for GPT-5.3-Codex-Spark style work: short-loop memory-layer
audits, small source-backed edits, quick checks, and portable handoff packets.
It is the fast-loop lane for one bounded memory-layer surface at a time.

The root `AGENTS.md` remains authoritative for repository identity, ownership
boundaries, reading order, and release route. `.agents/AGENTS.md` owns the
agent-facing companion district. Spark is an agent lane, not memory doctrine,
not a mechanic package, not generated truth, not proof authority, not routing
logic, not role policy, not KAG substrate, and not runtime state.

The core execution rule is `done-or-handoff`.

## Conditional source route
When this task touches the path, consult root `AGENTS.md`, `.agents/AGENTS.md`, `DESIGN.AGENTS.md`,
`.agents/spark/README.md`, this card, `.agents/spark/registry.json`, and the
scenario `README.md` plus `PROMPT.md` for the lane being touched.

If a change touches a memory source surface, read the nearest source doc,
schema, example, generator, or mechanic `AGENTS.md` before editing.

Read `SPARK_EXTRAPOLATION_NOTEBOOK.md` when changing the lane contract,
scenario set, validator, tests, release-check wiring, or public Spark framing.
It records the studied `Agents-of-Abyss`, `aoa-techniques`, `aoa-skills`, and
OpenAI Codex Spark pattern.

Use `.agents/spark/SWARM.md` only when a Spark swarm is explicitly requested.

## Boundaries

- Choose exactly one registered scenario from `.agents/spark/registry.json`.
- Keep one bounded memory-layer surface per Spark loop.
- Start with a map: task, files, risks, and validation path.
- Prefer one small, reviewable patch per loop.
- End as `done` or `handoff`; do not depend on an in-session switch to a
  larger model.
- Do not run broad tests automatically. Run validation when the user,
  scenario, or repo law asks for it; otherwise name skipped checks honestly.
- Do not hand-edit generated surfaces as source truth.
- Do not turn memory into proof, verdict logic, route sovereignty, role
  authority, KAG ownership, playbook choreography, runtime state, or live
  receipt storage.
- Preserve memory-is-not-proof boundaries even when a recall route is useful.
- Do not store private traces, secrets, hidden telemetry, or unreduced
  personal data in Spark packets.
- Escalate or write a handoff when the task needs deeper architecture,
  cross-repo owner judgment, public status promotion, or broad synthesis.

Spark is strongest here for memory-surface audits, one-surface refinements,
recall-contract checks, generated parity checks, mechanic seam scouting,
concrete diff review, registry sync, small tests, and release-prep passes.

A done task means memory remains explicit and bounded.

## Scenario Law

Every scenario must be registered in `.agents/spark/registry.json` and must
provide:

- `README.md` with scope, done signal, stop-line, and handoff route
- `PROMPT.md` that can launch a standalone Spark session
- `templates/result.md`
- `templates/handoff.md`
- `examples/result.example.md`

## Validation

For Spark lane changes, use the scenario's declared validation route.
For release-facing lane changes, use the scenario's declared release validation route.
For ordinary memory-surface work inside a scenario, use the narrowest relevant
validator named by the scenario, source surface, or nearest `AGENTS.md`.

## Reporting contract

Always report the restated task and touched scope, scenario chosen, files
changed, whether the change was semantic, structural, or clarity-only,
validation run, validation skipped, remaining risk, and what still needs a
slower model or human review.

Spark should behave like a curator of bounded traces here, not like a
myth-maker of memory authority.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
