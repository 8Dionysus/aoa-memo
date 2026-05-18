# AGENTS.md

## Applies To

This card applies to `mechanics/` and every nested path until a nearer
`AGENTS.md` narrows the lane.

## Role

`mechanics/` is the home for memo-side mechanics: repeatable memory-layer
operations that have inputs, outputs, owner splits, stop-lines, validation, and
legacy bridges.

It is not the home for constitutional law, proof verdicts, runtime workers,
role rights, routing implementation, KAG substrate truth, or private memory.

## Read Before Editing

Read:

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
- `docs/AGENTS.md`
- `docs/`
- `legacy/AGENTS.md`
- `legacy/README.md`
- `legacy/INDEX.md`

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
- A mechanic package must name an operation, not only a topic, owner, wave, or
  file family.
- Keep old flat `docs/*.md` paths out of active references once a mechanic owns
  the surface.
- If a move becomes runtime, proof, role authority, route implementation, KAG
  substrate, playbook choreography, or source doctrine, route to the stronger
  owner.

## Validation

For mechanic topology changes, run:

```bash
python scripts/validate_memo_mechanics.py
python scripts/validate_memo_mechanic_parts.py
python scripts/build_memo_mechanic_cards.py --check
python scripts/validate_memo_mechanic_cards.py
python scripts/build_memo_mechanic_owner_routes.py --check
python scripts/validate_memo_mechanic_owner_routes.py
python scripts/build_memo_mechanic_landing_logs.py --check
python scripts/validate_memo_mechanic_landing_logs.py
python scripts/build_memo_mechanic_readiness.py --check
python scripts/validate_memo_mechanic_readiness.py
python scripts/validate_mechanic_artifact_topology.py
python scripts/build_mechanic_artifact_inventory.py --check
python scripts/validate_mechanic_artifact_inventory.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report changed mechanic packages, whether active docs, owner maps, provenance,
legacy bridges, generated companions, and validators changed, and whether any
old flat docs-root reference remains.
