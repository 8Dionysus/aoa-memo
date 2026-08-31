# AGENTS.md

## Applies To

This card applies to `mechanics/` and every nested path until a nearer
`AGENTS.md` narrows the lane.

## Role

`mechanics/` is the home for memo-side mechanics: repeatable memory-layer
operations that have inputs, outputs, owner splits, stop-lines, validation, and
provenance.

It is not the home for constitutional law, proof verdicts, runtime workers,
role rights, routing implementation, KAG substrate truth, or private memory.

## Conditional route scope

- Above: root `AGENTS.md` owns repo identity, owner boundaries, and broad
  landing/verification route.
- Here: `mechanics/README.md` is the mechanics atlas and
  `mechanics/ARTIFACT_TOPOLOGY.md` owns root-to-mechanic artifact placement
  law. This file owns shared package law and executable mechanics validators.
- Below: each `mechanics/<slug>/AGENTS.md` narrows the operation; its `docs/`,
  and `parts/` cards narrow active doctrine and functioning parts. Historical
  `legacy/` material is provenance only and is outside the active AGENTS mesh.

## Conditional source route
When a task touches this path, consult only the relevant entries:

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `mechanics/README.md`
5. `mechanics/ARTIFACT_TOPOLOGY.md` when root technical artifacts may move
6. the nearest `mechanics/<slug>/AGENTS.md`
7. the package `README.md`, `DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and
   `PROVENANCE.md`

Use `docs/README.md` when a public docs route points into a mechanic, but do
not treat docs maps as stronger than package-local mechanic cards.

## Package Law

Every memo mechanic package must contain:

- `AGENTS.md`
- `README.md`
- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `parts/AGENTS.md`
- `parts/README.md`
- `docs/AGENTS.md`
- `docs/`

The package `README.md` is the mechanic card. It must include:

- `## Mechanic card`
- `### Operation`
- `### Trigger`
- `### Memo owns`
- `### Stronger owner split`
- `### Inputs`
- `### Outputs`
- `### Must not claim`
- `### Validation`
- `### Next route`

## Boundaries

- Active mechanic docs live under `mechanics/<slug>/docs/`.
- `legacy/` preserves old placement and route history; it is not active law.
- `mechanics/ARTIFACT_TOPOLOGY.md` governs when a root technical artifact can
  move into a mechanic-local artifact home.
- Generated companions summarize source maps and must be rebuilt from source.
- A mechanic package must name an operation, not only a topic, owner, stage, or
  file family.
- A mechanic package must materialize active rows from `PARTS.md` under
  `parts/<part-slug>/` with `README.md`, `CONTRACT.md`, and `VALIDATION.md`.
- Keep old flat `docs/*.md` paths out of active references once a mechanic owns
  the surface.
- If a move becomes runtime, proof, role authority, route implementation, KAG
  substrate, playbook choreography, or source doctrine, route to the stronger
  owner.

## Validation

Use the narrow validator matching the changed mechanics surface through its owning `VALIDATION.md` route:

- For package-local or part-local artifact homes, use the owning mechanic `VALIDATION.md` route.
- For `mechanics/ARTIFACT_TOPOLOGY.md` or root-artifact moves, use the root-topology validation route.
- For `PARTS.md` files or `parts/` contracts, use the owning mechanic `VALIDATION.md` route.
- For package mechanic cards, use the mechanic-card validation route.
- For `OWNER_MAP.md` files or package cards, use the owning mechanic validation route.
- For landing receipts, use the mechanic landing-log validation route.
- For package cards, owner maps, landing logs, validation routes, or local artifacts, use the owning mechanic validation route.
- For mechanic topology changes, use the nearest mechanic `VALIDATION.md` route.
Use the nearest mechanic `VALIDATION.md` route before closeout; reusable lanes remain in `config/validation_lanes.json`.
## Closeout

Report changed mechanic packages, whether active docs, owner maps, provenance,
generated companions, and validators changed, and whether any old flat
docs-root reference remains.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
