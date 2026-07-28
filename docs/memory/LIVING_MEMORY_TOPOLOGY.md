# Living Memory Topology

## Purpose

This document names the living topology for memory as OS Abyss scales.

Memory is not one growing pile. It is a set of bounded places with routes:
repo-local working memory, project memory, agent memory, runtime exports,
derived read models, and canonized `aoa-memo` objects.

## Topology

| Place | Owns | Routes to `aoa-memo` by |
|---|---|---|
| repo-local `memo/` port | local project notes, candidates, receipts, and handoff packets | reviewed intake packet or source-linked candidate |
| agent-local memory | role-specific preferences, limits, and handoff posture | reviewed agent memory candidate |
| runtime/host memory | live state, logs, checkpoints, and operational receipts | bounded export, never raw live store |
| `aoa-memo/memo/` | reviewed memory object corpus, corpus intake receipts, and corpus support lanes | `memo/objects/<kind-dir>/<year>/<slug>/object.json` plus `MEMO.md` |
| `aoa-memo` | memory doctrine, schemas, mechanics, recall contracts, lifecycle, provenance, and read models | source refs plus review posture |
| generated read models | compact catalog, capsules, sections, route cards, and mechanic indexes | builder and validator; object rows mark `source_kind` as `reviewed_corpus` or `teaching_fixture` |
| `aoa-kag` and graph consumers | derived retrieval and graph substrate | graph bridge contract with backward refs |

## Source Intake Matrix

These lanes name the regular sources that should produce memory candidates as
OS Abyss keeps moving. The stronger owner keeps raw truth; `aoa-memo` only owns
durable reviewed memory after a reviewed handoff.

| Lane | Recurring trigger | Raw or stronger truth owner | Candidate shape | First reviewed object slots | Next stronger route |
|---|---|---|---|---|---|
| center route memory | center doctrine, layer-map, federation route, or program direction changes | `Agents-of-Abyss` | source-linked route decision or state capsule | `anchor`, `decision`, `audit_event`, `state_capsule` | center law and federation rules |
| source-linked knowledge memory | ToS source, lineage, concept bridge, or authored-meaning handoff changes | `Tree-of-Sophia` | lineage bridge or source-route claim | `bridge`, `claim`, `episode`, `audit_event` | ToS authored meaning |
| seed and planting memory | seed staging, planting, replay, survival, or discard events | `Dionysus` | planting trace episode or bridge | `episode`, `pattern`, `bridge`, `audit_event` | seed protocol and target owner acceptance |
| session evidence memory | long session, compaction boundary, rehydrate packet, reviewed distillation | `.aoa` archive | reviewed distillation candidate, not raw transcript | `episode`, `claim`, `pattern`, `audit_event` | `.aoa` raw evidence |
| runtime access memory | MCP access-plane change, runtime closure, service route drift | `abyss-stack` | reviewed runtime or access-plane intake packet | `decision`, `state_capsule`, `audit_event`, `bridge` | runtime and infrastructure truth |
| host state memory | sanitized host state, runtime health, degraded or recovered service | host policy and `abyss-machine` surfaces | host-local sanitized state capsule or audit event | `state_capsule`, `episode`, `audit_event` | live host state and private-data boundary |
| agent role memory | role posture, recall rights pressure, orchestrator class needs | `aoa-agents` | memory posture claim or bridge | `claim`, `bridge`, `decision`, `audit_event` | role rights and identity |
| playbook recurrence memory | reviewed run, closeout, handoff, scenario memory scope | `aoa-playbooks` | reviewed-run episode, recurrence pattern, closure claim | `episode`, `pattern`, `claim`, `audit_event` | scenario choreography and run acceptance |
| proof-memory handoff | eval report creates durable memory pressure | `aoa-evals` | proof-outcome memory candidate | `audit_event`, `claim`, `pattern` | verdict logic and scoring |
| graph-memory handoff | KAG lift candidate, projection health, ToS bridge readiness | `aoa-kag` plus source owners | bridge memory candidate | `bridge`, `claim`, `audit_event` | derived substrate and source meaning |

## Owner-Route Matrix

| Place | Regular memory it produces | Local memory posture | Durable reviewed owner | Main consumers | Stronger than memo |
|---|---|---|---|---|---|
| `Agents-of-Abyss` | ecosystem route law, layer-map changes, federation decisions | local port when present | `aoa-memo` after reviewed intake | router, review, playbooks, stats, agents | center doctrine and federation law |
| `Tree-of-Sophia` | source-linked lineage, concept bridges, authored-meaning handoffs | local port when present | `aoa-memo` bridge or claim objects | KAG, source-route recall, review | authored source meaning |
| `Dionysus` | seed lineage, planting trace, early-form survival or discard memories | local port when present | `aoa-memo` episode, pattern, bridge, or audit event | playbooks, routing, center review | seed protocol and target owner acceptance |
| `.aoa` | raw Codex session evidence, compaction intervals, indexes, rehydrate packets | route-only evidence and reviewed distillation candidates | `aoa-memo` only after reviewed distillation | future agents, review, evals | raw transcript and archive evidence |
| `abyss-stack` | MCP access-plane evidence, runtime closure, service boundaries | local port candidates and exports | `aoa-memo` after reviewed intake | MCP, runtime, stats, evals, review | live runtime and infrastructure truth |
| `abyss-machine` | host-local sanitized state, runtime health, machine events | host-local sanitized port | `aoa-memo` after reviewed intake | runtime review, stats, agents | live host and private-data boundary |
| `aoa-agents` | role posture, memory rights pressure, orchestrator recall needs | local port when present | `aoa-memo` for memory objects only | router, review, bounded execution | role rights, identity, handoff authority |
| `aoa-playbooks` | reviewed runs, scenario handoffs, recurrence closeout | local port when present | `aoa-memo` for recalled traces | review, bounded execution, recurrence | scenario choreography |
| `aoa-evals` | proof reports, guardrail outcomes, bounded quality findings | route-only unless a port is added | `aoa-memo` for memory of proof outcomes only | review, quality harness, stats | verdict logic and scoring |
| `aoa-sdk` | return hints, dispatch entrypoints, route compression pressure, typed workspace discovery, and compatibility drift evidence | route-only unless a port is added | `aoa-memo` for route and compatibility memory evidence only | router, SDK, tools, MCP, agents | dispatch behavior, navigation policy, and typed SDK behavior |
| `aoa-kag` | derived substrate readiness, graph-lift pressure, projection health | route-only unless a port is added | `aoa-memo` bridge memory only | KAG consumers, ToS bridge review | normalized graph substrate |
| `aoa-stats` | derived memory movement summaries, trend views, corpus counts | route-only unless a port is added | `aoa-memo` for source events, not stats truth | review, roadmap, activation backlog | observability interpretation |

## Naming Topology

Names should reveal the route:

- `candidate` means reviewable input, not accepted memory
- `source` means stronger owner or source evidence
- `reviewed` means a route accepted the candidate for memo-side recall
- `current` means preferred active recall posture
- `superseded`, `retracted`, `archived`, and `frozen` mean lifecycle posture
- `bridge`, `handoff`, `export`, and `read_model` mean derived or consumer
  surfaces, not source truth

## Scaling Rule

Most local memory should start near the place that produced it. Durable,
cross-place memory should flow into `aoa-memo` only through a reviewed bridge.
Inside `aoa-memo`, reviewed durable memory lands as a corpus object bundle under
`memo/objects/`.

This keeps growth cheap locally while preserving one inspectable canon for
objects that need ecosystem recall.

## Port Status Surface

Port status should be reproducible, not guessed. A workspace map, MCP brief, or
future generated companion may render it, but it should expose the same fields:

| Field | Meaning |
|---|---|
| place | repo, host, or session evidence place |
| port_level | `none`, `route_only`, `stub_port`, `full_port`, or `mature_port` |
| owner | local owner of the port or route |
| stronger_memory_owner | usually `aoa-memo` for durable reviewed memory |
| privacy_posture | public-safe, host-local-sanitized, private, or route-only |
| local_candidates | candidate count inside the local port |
| pending_exports | exports not yet landed or rejected |
| ready_exports | exports ready for reviewed intake |
| landed_exports | exports already landed into `aoa-memo` |
| blocked_exports | exports blocked, rejected, quarantined, or archive-only |
| stale_or_broken | explicit issue list, not inferred silence |
| access_plane_status | current MCP/access-plane compatibility with generated surfaces |
| next_route | validate, prepare export, reviewed landing, quarantine, archive, or owner handoff |

The first authoritative inputs are local `memo/index.min.json` files,
workspace memory-map projections, and `aoa_memo` MCP brief or pending-export
outputs. None of them replaces reviewed memory objects.

## Operational Readouts

`aoa-memo` publishes memo-owned readouts over stronger owner surfaces:

| Readout | Source owner | Memo role | Validation |
|---|---|---|---|
| `generated/memory/source_intake_wave.min.json` | source repositories plus reviewed corpus objects | shows the first real source-lane intake wave across runtime access, graph-memory handoff, consumer recall, and local port evidence | operational-readout route in `docs/memory/AGENTS.md` |
| `generated/memory/workspace_memo_port_status.min.json` | `8Dionysus` workspace memory map | imports current port levels, export counts, issues, and next routes for memo-side recall | operational-readout route in `docs/memory/AGENTS.md` |

These readouts do not replace the workspace map, MCP runtime, local memo ports,
or reviewed object corpus. They make the current route easier for a distant
agent to inspect from `aoa-memo`.
