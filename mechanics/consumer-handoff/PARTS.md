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

## Interface

Inputs are consumer needs, source refs, scope and recall requirements, bridge
objects, guardrail cases, and quest alignment notes.

Outputs are bounded memo handoff surfaces and routeable refs. Stronger
consumer layers decide rights, scenarios, proof, graph activation, routing, and
runtime execution.
