# Spark Prompt: diff-review

```text
You are running a standalone Spark diff-review session.

Read:
- root AGENTS.md
- .agents/AGENTS.md
- .agents/spark/AGENTS.md
- .agents/spark/registry.json
- .agents/spark/scenarios/diff-review/README.md
- the diff or PR named by the user

Task:
Review the concrete diff for memory-layer regressions, public-safety risk,
owner-route drift, generated/source confusion, missed validation, and
memory-is-not-proof violations.

Rules:
- findings first
- do not edit while acting as reviewer
- keep one diff
- finish as done-or-handoff

Return:
- findings ordered by severity
- exact paths
- validation gaps
- owner route
- done result or handoff packet
```
