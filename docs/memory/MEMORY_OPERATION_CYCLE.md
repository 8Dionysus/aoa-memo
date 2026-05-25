# Memory Operation Cycle

## Purpose

This document gives `aoa-memo` one compact operational map for memory movement.
It lets an agent see how a candidate becomes reviewed memory, how reviewed
memory becomes a read model, and how stale or unsafe memory leaves the active
path.

## Cycle

1. Candidate intake records a source-linked object, export, note, or evidence
   packet without claiming current truth.
2. Write-path guardrails mark trust, ingestion risk, derivation lineage, review
   route, and action-safety separation.
3. Review decides whether the candidate stays pending, becomes a reviewed
   `memo/objects/` bundle through an export with `allowed_result:
   reviewed_write`, is rejected, is quarantined, or is routed to a stronger
   owner.
4. Consolidation links duplicates, contradictions, supersessions, retractions,
   archives, and freezes.
5. Generated read models expose compact catalog, capsule, section, mechanic,
   and route-card surfaces. Object-facing read models are built from reviewed
   corpus bundles plus teaching fixtures and mark `source_kind` for consumers.
6. Consumer handoff gives evals, KAG, stats, agents, playbooks, routing,
   runtime, or source owners bounded surfaces with provenance still visible.
7. Recurrence and retention checks return cooled, stale, contradicted, or
   newly useful memory to review.

## Memory Organ Map

The stable organ map is the route a future memory event should be able to walk
without inventing a new path.

| Contour | Role | Owner | Input | Output | Next route | Check |
|---|---|---|---|---|---|---|
| capture | preserve source-backed material before interpretation | source repo, host, `.aoa`, or local port | source docs, run logs, session segments, host receipts, reviewed-run notes | source refs, raw evidence refs, candidate seed | candidate shaping or stronger owner review | source evidence remains reachable |
| candidate | shape one bounded memory question without claiming current truth | local `memo/` port owner | captured refs, candidate text, trust and risk markers | local candidate packet | validation receipt, export, quarantine, or owner handoff | candidate names source refs and review route |
| review | decide whether a candidate may become durable memo memory | origin owner plus `aoa-memo` reviewer | candidate, receipts, export packet, source refs | accepted, rejected, quarantined, archive-only, or owner-handoff result | reviewed corpus landing or local retention | reviewed result is explicit |
| corpus | store durable reviewed memory objects | `aoa-memo/memo/` | accepted `reviewed_write` export or source-owned reviewed object patch | object bundle plus landing receipt | generated read models and consumer handoff | corpus validator passes |
| read model | expose compact inspect, capsule, and expand surfaces | `aoa-memo` generated district | reviewed corpus objects, teaching fixtures, doctrine surfaces | generated catalogs, capsules, sections, route-card companions | access plane, consumers, eval packs | source refs and `source_kind` stay visible |
| access plane | retrieve and operate local memory without becoming authority | runtime owner, currently `abyss-stack` MCP service | read models, local port indexes, pending exports | brief, search hits, status, dry-run landing plan | source owner, local port, reviewed landing | MCP output remains evidence or plan |
| consumer recall | let downstream organs use bounded memory | downstream owner repo | object ids, catalog rows, capsules, recall contracts | owner-local route hints, quest refs, eval cases, KAG donor refs, stats summaries | stronger owner action or memo writeback candidate | consumer stop-lines stay visible |
| lifecycle | keep time visible after memory changes | `aoa-memo` lifecycle posture plus stronger owner evidence | stale objects, duplicates, contradictions, supersession, source withdrawal | superseded, retracted, archived, frozen, demoted, split, or merge-review posture | audit event and regenerated read model | current recall posture changes visibly |
| quality | make memory behavior testable without moving proof into memo | `aoa-memo` for cases, `aoa-evals` for verdicts | recall packs, object refs, stale or contradiction cases | guardrail case pack or bounded eval report | consumer hardening or reviewed memory update | scoring remains outside memo |
| consolidation | return cooled, contradicted, duplicate, or newly useful memory to review | retention mechanic with stronger owners | lifecycle pressure, usage evidence, conflict refs, source feedback | consolidation operation, audit event, revised recall posture | corpus update, archive, or stronger owner | retention operation preserves provenance |

## Minimal State Machine

| State | Meaning | Next route |
|---|---|---|
| captured | source-backed input exists, review not complete | write-path guard |
| candidate | shaped as a memory candidate | owner review |
| reviewed | accepted for memo-side recall and landed as corpus object | generated read models |
| current | preferred active recall posture | eval and consumer handoff |
| superseded | replaced by a newer or stronger object | consolidation record |
| retracted | withdrawn for safety, error, or source withdrawal | audit event |
| archived | retained for history, not active recall | retention route |
| frozen | intentionally stable and rarely changed | owner route |

## Operator Map

| Need | Route |
|---|---|
| Is this safe to write? | `mechanics/operational-gate/docs/MEMORY_WRITE_PATH_GUARDRAILS.md` |
| How should memory age or leave active recall? | `mechanics/retention/docs/CONSOLIDATION_FORGETTING_OPERATION.md` |
| Which access posture should a consumer use? | `docs/posture/MEMORY_OPERATION_MODES.md` |
| How should local project memory connect back? | `docs/memory/LOCAL_MEMO_PORT_STANDARD.md` |
| How does reviewed memory land inside aoa-memo? | `memo/OBJECT_SHAPE.md` and `scripts/memory/land_reviewed_memo_intake.py` |
| How do KAG or graph consumers preserve truth? | `mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md` |
| How do runtime or host exports enter? | `mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md` |
| Which MCP route may an agent use? | the MCP access plane below, then the source route named by the returned evidence |

## Operational Cards

Use these cards before a live memory landing, export, or recall handoff.

| Card | Role | Input | Output | Owner | Next route | Consumer |
|---|---|---|---|---|---|---|
| capture | preserve source evidence | source refs, raw refs, local notes | captured refs and candidate seed | source owner | candidate | reviewer |
| candidate | shape one memory question | captured refs, risk markers | local candidate packet | local port owner | review | MCP and reviewer |
| review | accept, reject, quarantine, or route outward | candidate, export, receipts | reviewed result | origin owner plus memo reviewer | corpus | memo corpus |
| corpus | store durable object | reviewed result | object bundle and landing receipt | `aoa-memo` | read model | generated consumers |
| read model | expose compact recall | corpus object or doctrine source | catalog, capsule, section row | `aoa-memo` | access or consumer | tools and agents |
| access | retrieve without authority inflation | read models, port indexes | brief, search, status, dry-run plan | runtime MCP owner | owner route | agents |
| consumer | use memory inside owner bounds | object ids, capsules, contracts | owner-local recall or handoff | consumer repo | stronger owner or writeback | router, review, execution |
| lifecycle | update temporal posture | stale, conflict, or withdrawal evidence | lifecycle change and audit event | `aoa-memo` plus source owner | read-model refresh | all consumers |
| quality | test memory behavior | recall cases and object refs | bounded eval report | `aoa-evals` | candidate or lifecycle card | reviewer |

## MCP Access Plane

`aoa_memo` MCP is an access plane, not durable memory authority.

- `aoa_memo_brief`, `aoa_memo_search`, and `aoa_memo_pending_exports` help
  agents retrieve reviewed recall context and local-port status.
- `aoa_memo_validate_port` and `aoa_memo_validate_candidate` check local port
  and candidate shape before promotion pressure moves.
- `aoa_memo_create_candidate`, `aoa_memo_prepare_intake_packet`, and
  `aoa_memo_review_intake` may write local-port candidates, exports, or
  forwarding receipts only through the owning repository's `memo/` port.
- `aoa_memo_landing_plan` prepares a landing plan and should run as
  `run_dry_run: true` unless the `aoa-memo` owner route is preparing a reviewed
  source patch.
- Durable reviewed memory still lands through source-owned `aoa-memo` object
  bundles or `scripts/memory/land_reviewed_memo_intake.py`; MCP output is
  evidence or a plan, not memory truth.

## Access-Plane Currentness Readout

`generated/memory/access_plane_currentness.min.json` records the memo-owned
currentness slice for the `aoa_memo` access plane.

The readout compares live MCP brief/search/status/port probes against current
generated memory-object, quest, and workspace-memory-map surfaces. It names
known gaps as routed gaps rather than treating MCP search coverage as durable
truth. `abyss-stack` remains the runtime owner for MCP implementation, and
`8Dionysus` remains the owner for workspace overlay map generation.

Regenerate or check it with:

```bash
python scripts/memory/build_memory_operational_readouts.py --write --live
python scripts/memory/build_memory_operational_readouts.py --check --live
```

## Calibration

Good memory operations are boringly inspectable. A later agent should be able to
open one object or packet and see source refs, review posture, lifecycle, owner
route, generated surface, and next validator without reconstructing the whole
system from scattered prose.
