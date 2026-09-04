# Agent Surface Design

## Role

`DESIGN.AGENTS.md` describes the desired form of agent-facing guidance within
`aoa-memo`.

It is not a replacement for root `AGENTS.md`, local `AGENTS.md` cards, source
docs, schemas, examples, validators, or generated-surface source maps.

It answers one question:

What shape should agent guidance take so memory-layer work stays bounded,
public-safe, and source-routed?

## Design Thesis

Agent guidance in `aoa-memo` should make the nearest owner route easy to find.

The root card names repository identity and broad stop-lines. Local cards name
directory-specific risk. Source docs, schemas, examples, and generators own the
actual memory contract. Generated companions remain weaker than those authored
surfaces.

The agent layer exists to prevent memory work from drifting into proof,
routing, role policy, runtime machinery, or hidden context residue.

## Agent Surface Classes

### Root Card

Root `AGENTS.md` owns:

- repository identity
- owner lane and route-away boundaries
- conditional source routes
- release/governance landing pointer
- named validation lanes
- post-change reporting expectations

It should stay compact enough to be read first.

### District Cards

Local `AGENTS.md` cards own:

- local source classes
- local risk and stop-lines
- local validation selection and route
- local generated/source alignment rules

They should route to source docs and validators rather than duplicating long
doctrine blocks.

### Source Surfaces

Docs, schemas, examples, and scripts own memory-layer meaning within their
domain:

- docs own doctrine, boundary, lifecycle, bridge, writeback, and recall posture
- `MEMORY_INDEX.md` owns the compact public memory-canon map and routes to
  stronger doctrine instead of replacing it
- schemas own machine-readable contracts
- examples teach public-safe instance shape
- scripts build and validate derived surfaces

Agent guidance should point to them, not replace them.

### Generated Companions

Generated files help agents inspect compactly.

They do not become memory truth. When generated output changes, agents should
find the source surface or generator that produced it.

## Desired Mesh Shape

The long-term mesh should make these lanes explicit:

- `skills/` for canonical admitted procedures owned specifically by
  `aoa-memo`, with usefulness established manually before durable automation
- the OS-level `os-user-default` profile for one managed Codex exposure of the
  owner bundle, never for a second owner or copied shared catalog
- `.agents/` for agent-facing derived companions and maintained lanes
- `MEMORY_INDEX.md` for compact memory-canon routing before deeper doctrine
- `stats/` for memo-owned statistical questions, contracts, and reference
  packets governed by the shared `aoa-stats` grammar
- `docs/` for memory doctrine and route maps
- `mechanics/` for repeatable adoption, consumer handoff, operational gate,
  recurrence support, lineage harvest, questbook, writeback, and retention
  mechanics with owner maps, active docs subroutes, provenance bridges, and
  artifact placement law
- `schemas/` for contracts
- `examples/` for public-safe object and support examples
- `generated/` for compact companions
- `scripts/` for validators, builders, and publication helpers
- `tests/` for regression surfaces
- `config/` for build or registry inputs
- `manifests/` for recurrence or component manifests
- `quests/` for tracked memory-layer obligations, governed by Questbook

The current repository now has a source-backed AGENTS mesh mirror:

- `config/agents/agents_mesh.json` is the source map for current route cards
- `generated/agents/agents_mesh.min.json` is the compact generated companion
- `scripts/agents/validate_agents_mesh.py` checks route-card coverage and local card
  contracts
- `scripts/agents/build_agents_mesh_index.py --check` and
  `scripts/agents/validate_agents_mesh_index.py` keep the mirror reproducible

The mesh validates the current `aoa-memo` card form rather than importing a
sibling repository's heading template.

The owner skill home and runtime exposure are deliberately asymmetric:
`skills/aoa-memo/` is canonical source, while `skills/port.manifest.json`
admits it to one OS-managed user copy. Shared or owner bundles must not be
vendored into `.agents/`.

Retired agent lanes and former mechanic staging trees are recoverable only
through the pinned Git history recorded in `docs/decisions/`.

## Conditional source route
When a task touches agent-surface form, follow this conditional route:

1. root `AGENTS.md`
2. nearest nested `AGENTS.md` for every touched path
3. route-mode, `MEMORY_INDEX.md`, or source surface named by the root card
4. nearest local README, docs map, schema, example, generator, or validator
5. narrowest relevant check before broad release validation

When a change affects agent-surface form itself, read this file after root
`AGENTS.md` and before editing local cards.

## Stop-Lines

Agent guidance must not:

- turn memory into proof
- hide role rights inside memo wording
- move routing logic into memo surfaces
- make KAG exports behave like graph ownership
- make runtime writeback seams behave like live stores
- treat generated companions as source truth
- store private traces, secrets, or unreduced personal data
- let mythic or growth language outrun provenance and review

## Local Card Content

A durable local `AGENTS.md` card should usually say:

- what path it applies to
- what the path owns
- which source surfaces are stronger than the card
- what not to do in that path
- which validators or tests apply
- what closeout should report

It should avoid:

- duplicating root law
- carrying historical session narrative
- listing every possible command when a closer validator owns the lane
- promoting generated summaries into doctrine

## Public-Safe Posture

`aoa-memo` is a public memory-layer repository. Agent-facing surfaces must
assume public review unless a stronger owner says otherwise.

Examples, fixtures, decisions, docs, and generated outputs should remain
sanitized and reviewable. Raw private traces, credentials, local host secrets,
and unreduced personal context do not belong here.

## Decision Review

When agent-facing topology changes in a way future contributors will need to
understand, add a decision record under `docs/decisions/`.

Decision records explain why a route, placement, mesh expectation, validator,
or owner split exists. They do not replace the active route cards or source
docs.

## Validation Direction

Reusable machine command sequences are authoritative in
`config/validation_lanes.json`; focused human procedure is on demand in the
same-directory `VALIDATION.md` owned by the selected route card. One validation
file carries one owner route: it does not embed child route files or concatenate
unrelated procedure. Active agent cards name the applicable lane or route and
preserve semantic owner boundaries, but do not carry runnable command blocks
or unconditional README inventories. This design surface only names what
agent-facing validation should prove.

The AGENTS mesh generated companion checks:

- registered cards exist
- root and local cards preserve source-owner boundaries
- generated mesh output is reproducible
- `.agents/` lanes do not live as root civic surfaces by accident

Tests also pin this design file, required route links, the decision lane, and
the mesh validator path.

## One-Line Rule

Agent guidance in `aoa-memo` should help an agent find the memory source,
respect the boundary, and stop before pretending memory became another layer.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
