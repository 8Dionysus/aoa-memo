# Spark Prompt: test-factory

```text
You are running a standalone Spark test-factory session.

Read:
- root AGENTS.md
- tests/AGENTS.md or the nearest package-local test route card
- .agents/AGENTS.md
- .agents/spark/AGENTS.md
- .agents/spark/registry.json
- .agents/spark/scenarios/test-factory/README.md
- the source contract named by the user

Task:
Add or adjust the smallest test that constrains the existing memory contract.

Rules:
- test an existing contract
- do not invent semantics
- keep one test surface
- run the targeted test
- finish as done-or-handoff

Return:
- contract tested
- files changed
- validation run
- skipped checks
- remaining risk
```
