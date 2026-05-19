# Spark Prompt: release-prep

```text
You are running a standalone Spark release-prep session.

Read:
- root AGENTS.md
- .github/AGENTS.md when GitHub landing is in scope
- .agents/AGENTS.md
- .agents/spark/AGENTS.md
- .agents/spark/registry.json
- .agents/spark/scenarios/release-prep/README.md
- the diff or release slice named by the user

Task:
Run a fast release-readiness pass for the named slice.

Rules:
- inspect changed surfaces
- name public-claim and generated-parity risk
- do not publish, tag, push, or merge without explicit user command
- finish as done-or-handoff

Return:
- changed surfaces
- checks run
- skipped checks
- remaining release risk
- owner route or handoff
```
