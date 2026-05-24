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
6. **Reviewed corpus district**: it holds source-owned reviewed memory objects
   that need durable, addressable placement before generated read models.

A surface that is merely historical, staging-local, generated, experimental,
neighbor-owned, or future-looking must not sit in root by default.

## Docs-Root Principle

`docs/` root has its own smaller version of the same law.

A file may remain flat under `docs/` only when it is the docs route card, the
docs map itself, or a thin release-tool compatibility pointer that redirects to
the active `docs/root/` procedure. Current doctrine belongs in a named docs
district; mechanic docs belong in the owning mechanic package.

Staging receipts, candidate intake notes, historic landing notes, review
traces, decision rationale, and future protocol placeholders need named homes
before they become public docs. Do not add a new flat docs-root surface as a
shortcut.

## Allowed Root Surfaces

| Class | Allowed examples | Why root is justified | Guardrail |
|---|---|---|---|
| Layer law and public map | `README.md`, `CHARTER.md`, `DESIGN.md`, `ROADMAP.md` | they define the repository's identity, system form, and direction | must stay aligned with source docs and validators |
| Agent route law | `AGENTS.md`, `DESIGN.AGENTS.md`, `.agents/` | agent-facing work needs a stable local lane and a design form for that lane | must not replace source docs, schemas, examples, or validators |
| Public governance and legal | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE` | GitHub and contributors expect them there | must not become memory doctrine catalogs |
| Thin indexes | `MEMORY_INDEX.md`, `QUESTBOOK.md` | useful only while compact and route-oriented | must not become duplicate doctrine, a second roadmap, or a hidden ledger; generated companions must be builder-backed projections |
| Reviewed memory corpus | `memo/` | `aoa-memo` needs a source-owned home for reviewed memory object bundles and corpus intake receipts | object bundles must validate through `scripts/memory/validate_memo_corpus.py` and remain distinct from local repo memo ports |
| Tooling and machine districts | `.github/`, `config/`, `docs/`, `examples/`, `generated/`, `manifests/`, `mechanics/`, `quests/`, `schemas/`, `scripts/`, `tests/` | tooling and repo structure expect stable directories | each district needs local guidance plus the compact `generated/root-topology/root_technical_districts.min.json` atlas once root technical routing changes |
| Development requirements | `.gitignore`, `requirements-dev.txt` | development hygiene | must stay technical and small |

## Surfaces That Should Not Live In Root

| Surface kind | Better home | Reason |
|---|---|---|
| Maintained agent lane | `.agents/<lane>/` | agent lanes are not civic root law |
| Historical landing note | themed docs district or legacy/provenance home after a validated migration | landing history should not become a root peer |
| Generated artifact | `generated/` | generated surfaces must remain machine-facing and reproducible |
| Raw audit or review evidence | future evidence/provenance district or owner repo | evidence explains movement, not active doctrine |
| Runtime state or receipt stream | runtime owner or `.aoa/live_receipts/` when explicitly bounded | root docs must not become live state |
| Sibling-owner doctrine | owning repository | memo may route to it but should not absorb it |
| Experiment or scratchpad | untracked local notes, issue, or owner-local planning surface | the public root must not preserve every thought as law |

## Docs Surface Classes

Current docs surfaces should be read through these districts:

| Class | Home | Posture |
|---|---|---|
| Memory canon and object canon | `docs/memory/` | active memory doctrine |
| Boundary and operational posture | `docs/boundaries/` | active owner-boundary doctrine |
| Trust, lifecycle, temperature, provenance, and audit posture | `docs/posture/` | active temporal and evidence posture |
| Root law, release route, and preserved reference | `docs/root/` plus thin `docs/RELEASING.md` compatibility pointer | active route law plus reference; the flat release pointer must not carry independent policy |
| Writeback, checkpoint, readiness-boundary, and recurrence support mechanics | `mechanics/writeback/docs/*`, `mechanics/checkpoint/docs/*`, `mechanics/readiness-boundary/docs/*`, `mechanics/recurrence-support/docs/*` | active memo mechanic packages; do not turn them into runtime ledgers, dispatch, retry, proof, graph substrate, route dispatch, or role policy |
| Antifragility mechanic docs | `mechanics/antifragility/docs/*` | active antifragility memo mechanic; keep package map and validator aligned |
| Agon mechanic docs | `mechanics/agon/docs/AGON_*` | active Agon memo mechanic; keep package map and validator aligned |
| Titan mechanic docs | `mechanics/titan/docs/TITAN_*` | active Titan memo mechanic; keep package map and validator aligned |
| Adoption, writeback, and retention mechanics | `mechanics/adoption/docs/*`, `mechanics/writeback/docs/*`, `mechanics/retention/docs/*` | active memo mechanic packages; keep owner maps, legacy bridges, generated index, and validator aligned |
| Governance mechanic docs | `mechanics/governance/docs/*` | active governance authority-boundary memo mechanic; keep package map and validator aligned |
| Shape-guard mechanic docs | `mechanics/shape-guard/docs/*` | active shape/pruning memo mechanic; keep operation-first package map and validator aligned |
| Checkpoint mechanic docs | `mechanics/checkpoint/docs/*` | active checkpoint memory mechanic; keep package map, mechanic-local artifacts, generated companions, consumer refs, and validators aligned |
| Readiness-boundary mechanic docs | `mechanics/readiness-boundary/docs/*` | active readiness-boundary memo mechanic; keep package map, mechanic-local artifacts, generated refs, owner stop-lines, and validators aligned |
| Consumer handoff mechanic docs | `mechanics/consumer-handoff/docs/*` | active consumer handoff memo mechanic; keep package map, consumer refs, generated companions, and validators aligned |
| Operational gate mechanic docs | `mechanics/operational-gate/docs/*` | active operational admission memo mechanic; keep package map, mechanic-local artifacts, generated companions, and validators aligned |
| Recurrence support mechanic docs | `mechanics/recurrence-support/docs/*` | active route-return support memo mechanic; keep package map, mechanic-local artifacts, generated companions, Questbook refs, and validators aligned |
| Lineage harvest mechanic docs | `mechanics/lineage-harvest/docs/*` | active pattern-lineage harvest memo mechanic; keep package map, mechanic-local artifacts, generated companions, stronger-owner stop-lines, and validators aligned |
| Questbook mechanic docs | `mechanics/questbook/docs/*` | active public-obligation memo mechanic; root `QUESTBOOK.md` stays an index and root `quests/` stays the lane-first item store |
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

Before moving a docs surface into another district or mechanic:

1. identify the owning family and stop-lines
2. add or update the district or mechanic README and nearest `AGENTS.md`
3. update all source links, tests, validators, and generated refs that point to
   the old path
4. decide whether a decision record is needed
5. run the narrow validators before broad release validation

Do not move current doctrine as cosmetic cleanup. Move it only when the family,
nearest `AGENTS.md`, links, validators, and generated companions can move
together.

## Current Root Cleanup Decisions

| Existing surface | Decision | New home or status | Why |
|---|---|---|---|
| `DESIGN.md` | add | root system-form surface | the memory layer needs an explicit shape surface before topology cleanup |
| `DESIGN.AGENTS.md` | add | root agent-surface design surface | future AGENTS mesh work needs a design form |
| `MEMORY_INDEX.md` | add | root memory-canon index | the memory layer needs a compact public map for object kinds, support objects, recall modes, temperature vocabulary, source families, and generated companions without making `README.md` carry canon detail |
| `docs/README.md` | add | docs district map | flat docs need a navigable map before migration |
| `docs/decisions/` | add | decision rationale lane | topology choices need durable rationale without bloating active docs |
| `Spark/` | moved | `.agents/spark/` | maintained agent lanes should live under `.agents/`, not as root civic surfaces |
| `config/agents/agents_mesh.json` | add | config source for current route-card mesh | route cards need a machine-checkable source before docs districts move |
| `generated/agents/agents_mesh.min.json` | add | generated companion mirror | the mesh is inspectable without treating generated output as authority |
| `memo/` | add | reviewed memory corpus district | durable reviewed memory objects need a source-owned bundle home separate from local repo memo ports, examples, and generated read models |
| `manifests/AGENTS.md` and `quests/AGENTS.md` | add | top-level district route cards | both directories already hold durable public surfaces and should not be AGENTS coverage gaps |
| flat antifragility docs-root surfaces | moved | `mechanics/antifragility/docs/` | antifragility is an active memo mechanic with owner map, legacy bridge, schemas, examples, generated surfaces, tests, and validation |
| flat governance docs-root surfaces | moved | `mechanics/governance/docs/` | governance is an active authority-boundary memo mechanic with owner map, legacy bridge, authority stop-lines, tests, and validation |
| flat via-negativa checklist | moved | `mechanics/shape-guard/docs/VIA_NEGATIVA_CHECKLIST.md` | via-negativa is a general memory-shape guard, not governance authority memory |
| flat consumer handoff docs-root surfaces | moved | `mechanics/consumer-handoff/docs/` | agent, playbook, eval, KAG/ToS, KAG export, and orchestrator alignment surfaces are one repeatable handoff operation with stronger owner stop-lines |
| flat operational gate docs-root surfaces | moved | `mechanics/operational-gate/docs/` | deployment incident, office incident, service revision, and post-release boundary surfaces are one repeatable memory admission operation with release/runtime/proof stop-lines |
| flat recurrence-support docs-root surfaces | moved | `mechanics/recurrence-support/docs/` | recurrence support, witness trace, and reviewed closeout landing surfaces are one repeatable route-return support operation with dispatch/runtime/role/proof stop-lines |
| checkpoint support artifacts | moved | `mechanics/checkpoint/` | checkpoint gates, carry packets, approval/health records, improvement threads, and checkpoint-to-memory mappings are one repeatable memory operation with execution/runtime/role/route/proof stop-lines |
| flat readiness-boundary docs-root surface and artifacts | moved | `mechanics/readiness-boundary/` | memory readiness pressure, its contract schema/example, and its regression test are one repeatable admission-boundary operation with proof/runtime/KAG/route/role/live-ledger/object-family stop-lines |
| flat pattern-lineage docs-root surface | moved | `mechanics/lineage-harvest/docs/` | pattern-lineage memory is one repeatable lineage-harvest operation with federation/proof/KAG/ToS/stats/runtime/source-owner stop-lines |
| flat and transitional Agon surfaces | moved | `mechanics/agon/docs/AGON_*.md` | Agon is an active memo mechanic with owner map, legacy bridge, and validation |
| flat and transitional Titan surfaces | moved | `mechanics/titan/docs/TITAN_*.md` | Titan is an active memo mechanic with owner map, legacy bridge, and validation |
| flat adoption/writeback/retention docs-root surfaces | moved | `mechanics/adoption/docs/`, `mechanics/writeback/docs/`, `mechanics/retention/docs/` | these families are repeatable memo mechanics with owner maps and legacy bridges, not only documentation districts |
| flat root quest source files | moved | `quests/<lane>/<state>/` | Questbook keeps public obligations in the root item store, with `mechanics/questbook/` owning source contract, validation, and generated projections |
| mechanic-owned root technical artifacts | moved when single-mechanic-owned | `mechanics/<slug>/{schemas,examples,config,generated,scripts,tests,manifests}` | package-owned artifacts should sit with their mechanics; root technical districts keep only shared or cross-mechanic surfaces |
| root technical district atlas | add | `generated/root-topology/root_technical_districts.min.json` | root districts need a compact machine-readable map of role, route card, family ids, and local routing without making README or AGENTS cards carry the full allowlist |
| release-tool compatibility entrypoints | add | `docs/RELEASING.md`, `scripts/release_check.py` | workspace release tooling probes these legacy paths; they remain thin pointers to `docs/root/RELEASING.md` and `scripts/release/release_check.py` |

## Final Rule

The root is healthy when every file there can explain why it is visible before
the reader enters the districts.

The docs root is healthy when every flat docs file can explain why it is current
rather than historical, evidential, transitional, generated, or sibling-owned.
