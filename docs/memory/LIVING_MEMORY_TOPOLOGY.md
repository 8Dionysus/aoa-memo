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
