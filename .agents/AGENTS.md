# AGENTS.md

## Guidance for `.agents/`

`.agents/` is the agent-facing derived district for `aoa-memo`.

It currently declares no active agent lane. It does not own memory or skill truth. Memory
truth stays in source docs, schemas, examples, generated-source maps, and
validators; skill truth stays under top-level `skills/`, while global Codex
exposure comes from the OS user profile.

## Conditional route scope

- Above: root `AGENTS.md` owns repository identity, owner boundaries, and
  release route.
- Here: `.agents/` owns derived agent-facing lanes only.
- Below: future `.agents/<lane>/` directories may narrow an admitted local
  lane, but no former Spark lane is currently active. The owner skill remains
  under top-level `skills/`.

## Current Lanes

| Lane | Use |
|---|---|
| *(none currently)* | No repository-local lane is currently admitted. |

## Boundaries

- Do not treat agent companion files as source memory doctrine.
- Do not recreate owner or shared skill copies under `.agents/skills`; the OS
  user profile is the only active Codex exposure for the owner bundle.
- Do not store private traces, secrets, hidden telemetry, or unreduced personal
  data here.
- Do not let agent lane language make memory look like proof, routing logic,
  role authority, KAG substrate, or runtime state.
- Keep maintained agent lanes under `.agents/<lane>/`, not as root civic
  surfaces.

## Verify

For `.agents/` route changes, use the nearest `VALIDATION.md` route; reusable lanes remain in `config/validation_lanes.json`.
