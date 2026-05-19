# Spark Prompt: memory-audit

```text
You are running a standalone Spark memory-audit session.

Read:
- root AGENTS.md
- .agents/AGENTS.md
- .agents/spark/AGENTS.md
- .agents/spark/registry.json
- .agents/spark/scenarios/memory-audit/README.md
- the source surface named by the user

Task:
Audit the named scope for boundedness drift, duplicate meaning, stale paths,
weak provenance, temporal ambiguity, public-safety problems, weak owner routing,
and missing validation.

Rules:
- audit first
- do not edit unless the user explicitly requested fixes
- keep one scope
- finish as done-or-handoff

Return:
- scope read
- findings with file paths
- likely owner route
- validation implication
- done result or handoff packet
```
