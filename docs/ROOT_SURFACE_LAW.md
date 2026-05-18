# Root Surface Law

This document decides what may live in the root of `aoa-memo` and what may
remain flat under `docs/`.

The root is not a warehouse. It is the public front of the memory layer: a
small set of surfaces that let humans, agents, contributors, validators, and
neighboring repositories orient without digging.

## Root Principle

A root surface is allowed only when it serves at least one durable role:

1. **Layer authority**: it names, authorizes, designs, or routes the memory
   layer.
2. **Public governance**: platforms and contributors expect it at root.
3. **Thin public index**: it routes to deeper districts without duplicating
   them.
4. **Machine/developer district**: it is a top-level technical directory
   expected by tooling.
5. **Agent lane**: it belongs to the agent-facing lane and is governed by that
   lane.

A surface that is merely historical, wave-local, generated, experimental,
neighbor-owned, or future-looking must not sit in root by default.

## Docs-Root Principle

`docs/` root has its own smaller version of the same law.

A file may remain flat under `docs/` only when it is current memory doctrine,
current route law, current cross-repo boundary, or a compatibility route that
protects a known public entrypoint.

Wave receipts, candidate intake notes, historic landing notes, review traces,
decision rationale, and future protocol placeholders need named homes once a
safe district exists. Until that migration is validated, flat docs remain
active surfaces and must not be moved casually.

## Allowed Root Surfaces

| Class | Allowed examples | Why root is justified | Guardrail |
|---|---|---|---|
| Layer law and public map | `README.md`, `CHARTER.md`, `DESIGN.md`, `ROADMAP.md` | they define the repository's identity, system form, and direction | must stay aligned with source docs and validators |
| Agent route law | `AGENTS.md`, `DESIGN.AGENTS.md`, `.agents/` | agent-facing work needs a stable local lane and a design form for that lane | must not replace source docs, schemas, examples, or validators |
| Public governance and legal | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE` | GitHub and contributors expect them there | must not become memory doctrine catalogs |
| Thin indexes | `QUESTBOOK.md` | useful only while compact and route-oriented | must not become a second roadmap or hidden ledger |
| Tooling and machine districts | `.github/`, `config/`, `docs/`, `examples/`, `generated/`, `manifests/`, `quests/`, `schemas/`, `scripts/`, `tests/` | tooling and repo structure expect stable directories | each district needs local guidance before it becomes complex |
| Development requirements | `.gitignore`, `requirements-dev.txt` | development hygiene | must stay technical and small |

## Surfaces That Should Not Live In Root

| Surface kind | Better home | Reason |
|---|---|---|
| Maintained agent lane | `.agents/<lane>/` | agent lanes are not civic root law |
| Wave landing note | themed docs district or legacy/provenance home after a validated migration | landing history should not become a root peer |
| Generated artifact | `generated/` | generated surfaces must remain machine-facing and reproducible |
| Raw audit or review evidence | future evidence/provenance district or owner repo | evidence explains movement, not active doctrine |
| Runtime state or receipt stream | runtime owner or `.aoa/live_receipts/` when explicitly bounded | root docs must not become live state |
| Sibling-owner doctrine | owning repository | memo may route to it but should not absorb it |
| Experiment or scratchpad | untracked local notes, issue, or owner-local planning surface | the public root must not preserve every thought as law |

## Docs-Root Surface Classes

Current flat `docs/*.md` surfaces should be read through these classes:

| Class | Examples | Posture |
|---|---|---|
| Core memory doctrine | `BOUNDARIES`, `MEMORY_MODEL`, `MEMORY_OBJECT_PROFILES`, `MEMORY_TRUST_POSTURE`, `MEMORY_TEMPERATURES`, `LIFECYCLE`, `NARRATIVE_CORE_CONTRACT`, `PROVENANCE_THREADS`, `OPERATIONAL_BOUNDARY` | active docs-root surfaces |
| Neighbor seam docs | `AGENT_MEMORY_POSTURE_SEAM`, `PLAYBOOK_MEMORY_SCOPES`, `ROUTING_MEMORY_ADOPTION`, `KAG_*`, `MEMORY_EVAL_GUARDRAILS` | active docs-root surfaces until a seam district exists |
| Writeback and recurrence docs | `WITNESS_TRACE_CONTRACT`, `RUNTIME_WRITEBACK_SEAM`, `GROWTH_REFINERY_WRITEBACK`, `QUEST_CHRONICLE_WRITEBACK`, `RECURRENCE_MEMORY_SUPPORT_SURFACES` | active docs-root surfaces; do not turn them into runtime ledgers |
| Agon docs | `docs/agon/AGON_*` | active Agon memo district; keep map and validator aligned |
| Titan docs | `TITAN_*` | candidate district material; do not bulk-move without a map and validator |
| Adoption, governance, retention, rollback docs | `ADOPTION_*`, `GOVERNANCE_*`, `*_RETENTION_*`, `ROLLBACK_*` | candidate district material; preserve owner stop-lines |
| Decisions | `docs/decisions/` | rationale only; active docs still define what |

## Decision Procedure Before Adding a Root File

Ask these questions in order:

1. Does the file define memory-layer identity, system form, governance, public
   platform posture, or a thin index?
2. Would a human reasonably expect to find this file at root before entering
   `docs/`, `schemas/`, `examples/`, or generated companions?
3. Would an agent make safer decisions because this file is at root rather than
   in a deeper district?
4. Does a generated, example, schema, decision, quest, manifest, trace, or
   owner-local home already fit better?
5. Can the file stay compact over time without becoming a duplicate doctrine
   surface?

If the answer to any of questions 1-3 is no, or question 4 is yes, do not place
the file at root.

## Migration Procedure Before Moving Flat Docs

Before moving a flat `docs/*.md` surface into a district:

1. identify the owning family and stop-lines
2. add or update the district README and nearest `AGENTS.md`
3. update all source links, tests, validators, and generated refs that point to
   the old path
4. decide whether a decision record is needed
5. run the narrow validators before broad release validation

Do not move Agon, Titan, adoption, retention, rollback, or writeback surfaces
as a cosmetic cleanup. They are current memory-layer seams until a validated
district route replaces their flat path.

## Current Root Cleanup Decisions

| Existing surface | Decision | New home or status | Why |
|---|---|---|---|
| `DESIGN.md` | add | root system-form surface | the memory layer needs an explicit shape surface before topology cleanup |
| `DESIGN.AGENTS.md` | add | root agent-surface design surface | future AGENTS mesh work needs a design form |
| `docs/README.md` | add | docs district map | flat docs need a navigable map before migration |
| `docs/decisions/` | add | decision rationale lane | topology choices need durable rationale without bloating active docs |
| `Spark/` | moved | `.agents/spark/` | maintained agent lanes should live under `.agents/`, not as root civic surfaces |
| `config/agents_mesh.json` | add | config source for current route-card mesh | route cards need a machine-checkable source before docs districts move |
| `generated/agents_mesh.min.json` | add | generated companion mirror | the mesh is inspectable without treating generated output as authority |
| `manifests/AGENTS.md` and `quests/AGENTS.md` | add | top-level district route cards | both directories already hold durable public surfaces and should not be AGENTS coverage gaps |
| flat Agon docs-root surfaces | moved | `docs/agon/AGON_*.md` | Agon is the first validated thematic docs district |

## Final Rule

The root is healthy when every file there can explain why it is visible before
the reader enters the districts.

The docs root is healthy when every flat docs file can explain why it is current
rather than historical, evidential, transitional, generated, or sibling-owned.
