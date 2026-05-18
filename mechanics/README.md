# Memo Mechanics Atlas

This is the branch point for memo-side mechanics.

Use it when a memory-layer surface is not only doctrine, but a repeatable move
with inputs, outputs, owner split, stop-lines, validation, and legacy routing.

This atlas does not create stronger authority. It keeps `aoa-memo` honest
about what memory can preserve and where runtime, proof, routing, role, KAG,
playbook, skill, technique, stats, or source truth must route next.

## Root Mechanics Files

| File | Owns | Must not become |
|---|---|---|
| [AGENTS](AGENTS.md) | mechanics-tree route law and validation lane | package doctrine |
| [README](README.md) | this atlas and mechanic card contract | duplicate package map |

Generated indexes reflect source maps. They do not author mechanic truth.

## Mechanic Card Contract

Every `mechanics/<slug>/README.md` is an agent-operable card. It answers when
to use the mechanic, what memo owns, who owns stronger truth, what may enter,
what may leave, what must not be claimed, how to validate, and where to route
next.

Each package README must include these headings in order:

| Heading | Purpose |
|---|---|
| `## Mechanic card` | compact status and entry point |
| `### Trigger` | when the mechanic applies |
| `### Memo owns` | what `aoa-memo` may author here |
| `### Stronger owner split` | repositories or districts that own stronger truth |
| `### Inputs` | what may enter this mechanic |
| `### Outputs` | what may leave this mechanic |
| `### Must not claim` | package stop-lines |
| `### Validation` | exact package validation route |
| `### Next route` | where implementation, proof, memory, runtime, role, KAG, or source meaning goes next |

After the card, package README files should stay lightweight and route to
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, `PROVENANCE.md`,
`LANDING_LOG.md`, `ROADMAP.md`, `docs/`, and `legacy/`.

## Compass

| Mechanic | Memo question | Status | Start here | Must not claim |
|---|---|---|---|---|
| [adoption](adoption/README.md) | How does a memory candidate become reviewable for adoption without becoming proof or automatic promotion? | landed memo route | [PARTS](adoption/PARTS.md), [OWNER_MAP](adoption/OWNER_MAP.md), [PROVENANCE](adoption/PROVENANCE.md) | adopted truth, proof verdict, route sovereignty, or runtime write |
| [writeback](writeback/README.md) | How does a memory-layer writeback target, intake, chronicle, revision, rollback, or growth return stay source-linked and bounded? | landed memo route | [PARTS](writeback/PARTS.md), [OWNER_MAP](writeback/OWNER_MAP.md), [PROVENANCE](writeback/PROVENANCE.md) | live ledger, hidden worker, runtime storage, automatic promotion, or owner acceptance |
| [retention](retention/README.md) | How does retention evidence, watch, marker, or outcome stay reviewable without executing retention? | landed memo route | [PARTS](retention/PARTS.md), [OWNER_MAP](retention/OWNER_MAP.md), [PROVENANCE](retention/PROVENANCE.md) | retention execution, private trace retention, scheduler authority, or runtime policy |

## Package Route Standard

For a mechanic package, start with the package `README.md`. Then use only the
surface that matches the work:

| Surface | Use for |
|---|---|
| `AGENTS.md` | local route law, post-change review, closeout, validation |
| `DIRECTION.md` | current operating contour |
| `PARTS.md` | active functioning parts and source docs |
| `OWNER_MAP.md` | memo role and stronger owner split |
| `PROVENANCE.md` | active-first bridge to legacy placement and source receipts |
| `LANDING_LOG.md` | checked landings, validation anchors, and stop-lines |
| `ROADMAP.md` | next contour and condition-based future work |
| `docs/` | active mechanic-owned doctrine and support notes |
| `legacy/` | preserved placement history that should not burden active routes |

## Artifact Placement

Mechanics are not documentation-only packages. When a schema, example, config,
generated companion, script, test, or quest rule belongs to one mechanic, it may
remain in the repo-wide technical district only when it is still shared by
multiple memory surfaces. Package-local source docs live under the mechanic.

## Validation

Executable commands for this atlas live in [mechanics/AGENTS](AGENTS.md).

For release-bound mechanics changes, run:

```bash
python scripts/release_check.py
```
