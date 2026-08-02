# Consumer Handoff Parts

## Active Parts

| Part | Source Docs | Contract |
|---|---|---|
| Agent posture handoff | [AGENT_MEMORY_POSTURE_SEAM](./docs/AGENT_MEMORY_POSTURE_SEAM.md) | names memo-side fields that agent rights may apply to without becoming role policy |
| Playbook scope handoff | [PLAYBOOK_MEMORY_SCOPES](./docs/PLAYBOOK_MEMORY_SCOPES.md) | tells playbooks how to request bounded recall modes and scopes |
| Eval guardrail handoff | [MEMORY_EVAL_GUARDRAILS](./docs/MEMORY_EVAL_GUARDRAILS.md) | names memory quality risk cases for downstream proof owners |
| KAG/ToS bridge handoff | [KAG_TOS_BRIDGE_CONTRACT](./docs/KAG_TOS_BRIDGE_CONTRACT.md) | defines chunk-face, graph-face, and ToS bridge posture without graph ownership |
| KAG source export | [KAG_SOURCE_EXPORT](./docs/KAG_SOURCE_EXPORT.md) | describes the source-owned tiny donor export for KAG readiness |
| Orchestrator recall alignment | [ORCHESTRATOR_MEMORY_ALIGNMENT](./docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md) | aligns router, review, and bounded-execution quest families to memo recall posture |
| MCP organ access | `parts/mcp-organ-access/` | publishes exact durable-read and candidate-preparation capability ceilings for stack runtime binding |
| MCP owner evidence review | `parts/mcp-owner-evidence-review/` | authenticates one stack capture and binds its memo brief to the exact current reviewed-corpus read model without asserting proof, acceptance, or admission |
| Downstream feed regression | `mechanics/consumer-handoff/parts/downstream-feed-regression/tests/` | keeps consumer-facing recall, KAG export, checkpoint, and writeback read surfaces aligned without becoming runtime authority |

## Part-Local Artifacts

| Part | Artifact Homes |
|---|---|
| Playbook scope handoff | `parts/playbook-scope-handoff/tests/` |
| Eval guardrail handoff | `parts/eval-guardrail-handoff/schemas/`, `parts/eval-guardrail-handoff/examples/` |
| KAG/ToS bridge handoff | `parts/kag-tos-bridge-handoff/schemas/`, `parts/kag-tos-bridge-handoff/examples/` |
| KAG source export | `parts/kag-source-export/schemas/`, `parts/kag-source-export/examples/`, `parts/kag-source-export/generated/`, `parts/kag-source-export/scripts/` |
| MCP organ access | `parts/mcp-organ-access/config/`, `parts/mcp-organ-access/schemas/`, `parts/mcp-organ-access/tests/` |
| MCP owner evidence review | `parts/mcp-owner-evidence-review/config/`, `parts/mcp-owner-evidence-review/scripts/`, `parts/mcp-owner-evidence-review/tests/` |
| Downstream feed regression | `parts/downstream-feed-regression/tests/` |

## Interface

Inputs are consumer needs, source refs, scope and recall requirements, bridge
objects, guardrail cases, and quest alignment notes.

Outputs are bounded memo handoff surfaces and routeable refs. Stronger
consumer layers decide rights, scenarios, proof, graph activation, routing, and
runtime execution.
