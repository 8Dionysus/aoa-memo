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
- broad reading order
- GitHub landing route
- default validation path
- post-change reporting expectations

It should stay compact enough to be read first.

### District Cards

Local `AGENTS.md` cards own:

- local source classes
- local risk and stop-lines
- exact local checks
- local generated/source alignment rules

They should route to source docs and validators rather than duplicating long
doctrine blocks.

### Source Surfaces

Docs, schemas, examples, and scripts own memory-layer meaning within their
domain:

- docs own doctrine, boundary, lifecycle, bridge, writeback, and recall posture
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

- `.agents/` for agent-facing companion assets and future maintained lanes
- `docs/` for memory doctrine and route maps
- `mechanics/` for repeatable adoption, writeback, and retention mechanics
  with owner maps and legacy bridges
- `schemas/` for contracts
- `examples/` for public-safe object and support examples
- `generated/` for compact companions
- `scripts/` for validators, builders, and publication helpers
- `tests/` for regression surfaces
- `config/` for build or registry inputs
- `manifests/` for recurrence or component manifests
- `quests/` for tracked memory-layer obligations

The current repository now has a source-backed AGENTS mesh mirror:

- `config/agents_mesh.json` is the source map for current route cards
- `generated/agents_mesh.min.json` is the compact generated companion
- `scripts/validate_agents_mesh.py` checks route-card coverage and local card
  contracts
- `scripts/build_agents_mesh_index.py --check` and
  `scripts/validate_agents_mesh_index.py` keep the mirror reproducible

The mesh validates the current `aoa-memo` card form rather than importing a
sibling repository's heading template.

## Reading Order Shape

For agent editing, the intended order is:

1. root `AGENTS.md`
2. nearest nested `AGENTS.md` for every touched path
3. route-mode or source surface named by the root card
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

The current broad validation path remains:

```bash
python scripts/release_check.py
```

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
