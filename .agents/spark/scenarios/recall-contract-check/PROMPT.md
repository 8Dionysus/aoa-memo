# Spark Prompt: recall-contract-check

```text
You are running a standalone Spark recall-contract-check session.

Read:
- root AGENTS.md
- .agents/AGENTS.md
- .agents/spark/AGENTS.md
- .agents/spark/registry.json
- .agents/spark/scenarios/recall-contract-check/README.md
- the recall-facing source named by the user

Task:
Check whether the named recall contract keeps source, provenance, temporal
posture, salience, owner route, and validation explicit.

Rules:
- keep one contract
- memory must not become proof, identity, route policy, role right, KAG truth,
  or runtime state
- repair only if the user asked for repair and the patch is small
- finish as done-or-handoff

Return:
- contract checked
- source and stronger-owner route
- recall claim limits
- validation implication
- done result or handoff packet
```
