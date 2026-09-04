# AGENTS.md

## Applies to

This card applies to `aoa-memo/kag/` and every nested path until a nearer card
narrows the lane.

## Role

`kag/` is the local KAG provider home for `aoa-memo`. It exposes compact,
source-linked records over `memory registry and reviewed memory corpus route` for `aoa-kag` registry,
composition, and MCP consumers.

## Conditional source route
When this task touches the path, consult root `AGENTS.md`, this card, `kag/README.md`, `kag/manifest.json`,
`generated/memory/memo_registry.min.json`, and `memo/README.md` before
changing provider records.

## Boundaries

Keep authored meaning with `aoa-memo` source surfaces. Keep shared KAG schema,
registry, composition, and provider validation with `aoa-kag`. Keep runtime
serving state with `abyss-stack` or the runtime owner named by the consumer.

## Validation

Use the owner validator named in `manifest.json`, then validate this provider
through the `aoa-kag` local subtree validator.

## Closeout

Report provider records changed, source-return route changed, owner validation,
`aoa-kag` validation, and the next MCP consumer route.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
