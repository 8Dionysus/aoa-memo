# Consumer Handoff Docs

Active consumer-handoff memo mechanic docs live here.

## Surfaces

| Surface | Owns |
|---|---|
| [AGENT_MEMORY_POSTURE_SEAM](AGENT_MEMORY_POSTURE_SEAM.md) | memo-side fields that `aoa-agents` may consume without inheriting role policy |
| [PLAYBOOK_MEMORY_SCOPES](PLAYBOOK_MEMORY_SCOPES.md) | bounded recall modes and scopes that `aoa-playbooks` may request |
| [MEMORY_EVAL_GUARDRAILS](MEMORY_EVAL_GUARDRAILS.md) | memory risk cases that `aoa-evals` may turn into proof surfaces |
| [KAG_TOS_BRIDGE_CONTRACT](KAG_TOS_BRIDGE_CONTRACT.md) | chunk-face, graph-face, and ToS bridge handoff posture |
| [KAG_SOURCE_EXPORT](KAG_SOURCE_EXPORT.md) | source-owned donor export posture for KAG readiness |
| [ORCHESTRATOR_MEMORY_ALIGNMENT](ORCHESTRATOR_MEMORY_ALIGNMENT.md) | orchestrator quest-family alignment to memo recall posture |

## Stop-Line

These surfaces publish bounded handoff posture only. Stronger authority stays
with the owners named in [OWNER_MAP](../OWNER_MAP.md).
