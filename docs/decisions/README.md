# Decisions

This directory holds durable decision records for `aoa-memo`.

Use it when a future contributor will need the rationale for a route,
topology, source-of-truth split, validator, public contract, or workflow
expectation.

## What Belongs Here

- structural placement decisions
- root or docs-root route-law decisions
- AGENTS mesh or agent-lane decisions
- validator-authority decisions
- public-contract and source-of-truth split decisions
- cross-repo boundary decisions that need local rationale

## What Stays Elsewhere

| Material | Home |
|---|---|
| active memory doctrine | current docs such as `MEMORY_MODEL`, `BOUNDARIES`, and `OPERATIONAL_BOUNDARY` |
| schemas and machine contracts | `schemas/` |
| public-safe examples | `examples/` |
| generated companions | `generated/` |
| release history | `CHANGELOG.md` |
| future work | `ROADMAP.md` or `QUESTBOOK.md` |
| raw evidence or private traces | not in this public repo unless sanitized and routed |

## Index

| Decision | Scope |
|---|---|
| [2026-05-18-memory-topology-spine](2026-05-18-memory-topology-spine.md) | add topology-spine surfaces before moving flat docs |
| [2026-05-18-spark-agent-lane-home](2026-05-18-spark-agent-lane-home.md) | move maintained Spark lane from root to `.agents/spark/` |
| [2026-05-18-agents-mesh-source-backed-route-cards](2026-05-18-agents-mesh-source-backed-route-cards.md) | add source-backed AGENTS mesh for current route cards |
| [2026-05-18-agon-docs-district](2026-05-18-agon-docs-district.md) | move flat Agon memo docs into `docs/agon/` |
| [2026-05-18-titan-docs-district](2026-05-18-titan-docs-district.md) | move flat Titan memo docs into `docs/titan/` |
| [2026-05-18-adoption-writeback-retention-mechanics](2026-05-18-adoption-writeback-retention-mechanics.md) | move adoption, writeback, and retention docs-root surfaces into memo mechanics |
| [2026-05-18-mechanics-subroutes-artifact-topology](2026-05-18-mechanics-subroutes-artifact-topology.md) | add docs/legacy mechanic subroutes and artifact placement law |
| [2026-05-18-agon-titan-memo-mechanics](2026-05-18-agon-titan-memo-mechanics.md) | supersede Agon/Titan docs districts with memo mechanic packages |
| [2026-05-18-antifragility-memo-mechanic](2026-05-18-antifragility-memo-mechanic.md) | move failure-lesson and recovery-pattern docs into an antifragility memo mechanic |
| [2026-05-18-governance-memo-mechanic](2026-05-18-governance-memo-mechanic.md) | move governance, federation, installation, certification, precedent, and stay-order docs into a governance authority-boundary memo mechanic |
| [2026-05-18-shape-guard-memo-mechanic](2026-05-18-shape-guard-memo-mechanic.md) | add shape-guard as the via-negativa operation-first memo mechanic |
| [2026-05-18-consumer-handoff-memo-mechanic](2026-05-18-consumer-handoff-memo-mechanic.md) | move agent, playbook, eval, KAG/ToS, KAG export, and orchestrator alignment docs into a consumer-handoff memo mechanic |

## Review Rule

Before adding a decision, ask whether the note explains a real choice. If the
answer is only "this file changed", the changelog or PR summary is enough.
