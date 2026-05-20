# Memory Operation Modes

## Purpose

Operation modes describe how a consumer may interact with memory during a task.
They keep read, write, generation, and review posture explicit without turning
access into role authority.

## Modes

| Mode | Use | Write posture |
|---|---|---|
| `read_only` | inspect existing memory and generated read models | no writes |
| `write_candidate_only` | capture source-linked candidates for review | candidate writes only |
| `generate_without_read` | produce derived output without reading memory | no memory reads or writes |
| `read_write_under_review` | read memory and produce reviewable writebacks | reviewed candidate writes |
| `frozen_read_mostly` | inspect stable surfaces with rare owner-approved changes | owner-approved write only |

## Contract

The schema-backed posture surface is:

- `schemas/recall-posture/memory_operation_mode.schema.json`
- `examples/recall/memory_operation_modes.example.json`

Consumers should choose one mode before reading or writing memory. The mode
does not grant actor rights; it only names the memo-side access posture.
