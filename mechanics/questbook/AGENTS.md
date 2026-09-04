# AGENTS.md

## Applies to

`mechanics/questbook/` and its active mechanic surfaces.

## Role

Questbook owns memo-side public obligation mechanics: root `QUESTBOOK.md`,
the lane-first `quests/` item store, source contracts, lifecycle placement,
generated quest projections, and owner-routing stop-lines.

It does not own source quest state, playbook choreography, proof outcomes,
runtime scheduling, role rights, or hidden memory.

## Local delta

The `questbook` mechanic identity remains local; shared package, docs, parts, and
legacy hierarchy is inherited from `mechanics/AGENTS.md`. Its package card,
DIRECTION.md, PARTS.md, OWNER_MAP.md, and PROVENANCE.md remain the semantic
anchors for this operation.

For quest source or projection semantics, the local route is
`docs/QUEST_SOURCE_CONTRACT.md`, root `QUESTBOOK.md`, and root `quests/`
through the package and projection part cards.

## Boundaries

- Root `QUESTBOOK.md` is a compact public index, not a second roadmap.
- Root `quests/` is the public lane-first item store, not a package-local
  artifact directory and not private scratch work.
- Generated quest catalog and dispatch files are root-published read models
  from quest source files; rebuild them rather than editing by hand. Their
  part contract is `parts/quest-read-model-projections/`.
- Do not turn memo quest records into proof, route dispatch, playbook
  scenario state, runtime retention, role authority, or source-owner
  acceptance.

## Verification

Use the nearest `VALIDATION.md` route for `questbook` work after the touched
surface is known; reusable lanes remain in `config/validation_lanes.json`.

## Closeout

Report changed quest lanes, lifecycle states, generated projections rebuilt or
not rebuilt, owner boundaries affected, checks run, skipped checks, and the
next owner route when a quest is only carrying another repository's work.
