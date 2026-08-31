# AGENTS.md

## Applies To

This card applies to `mechanics/recurrence-support/legacy/`.

## Role

This directory preserves placement provenance for recurrence-support surfaces.

It is not the active recurrence-support route, not a compatibility alias, not a
docs-root mirror, and not a place for new contracts.
In short, it is not the active route; use `legacy/INDEX.md` only for placement
history.

## Conditional route scope

- Above: the package `AGENTS.md`, `PROVENANCE.md`, and `OWNER_MAP.md` define
  the active route and stronger-owner boundary.
- Here: `INDEX.md` maps former paths to active surfaces, `DISTILLATION_LOG.md`
  records restoration decisions, and `raw/` contains historical snapshots.
- Below: `raw/` is evidence only. Do not edit it as current doctrine and do not
  cite it as an active route.

## Conditional source route
When this task touches the path, consult root `AGENTS.md`, `mechanics/AGENTS.md`, `../AGENTS.md`,
`../PROVENANCE.md`, and `legacy/INDEX.md`.

## Boundaries

- Keep legacy content historical and minimal.
- Do not add active doctrine, schema contracts, examples, generated outputs,
  quests, or validator logic here.
- Do not cite old flat docs-root paths from active surfaces except where
  mechanics validators explicitly allow provenance, decisions, legacy indexes,
  or former-path source maps.
- Route active recurrence-support work to `../docs/`.

## Closeout

Report whether this legacy surface changed and why active recurrence-support
docs were not changed instead.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
