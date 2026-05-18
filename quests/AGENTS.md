# AGENTS.md

## Guidance for `quests/`

`quests/` holds memory-layer obligations that are summarized from
`QUESTBOOK.md` and validated as public repo state.

Quest files may track memo-facing recall, writeback, recurrence, and adoption
obligations. They do not own playbook scenario composition, proof outcomes,
runtime retention, or agent role rights.

## Current Shape

The foundation quest family uses `AOA-MEM-Q-*.yaml`.

Agon-specific follow-through currently uses `AOM-Q-AGON-*.md` and
`AOMEMO-Q-AGON-*.md` files that route back to the `docs/agon/` district.

Keep `QUESTBOOK.md`, `quests/`, and any generated quest companions aligned.

## Boundaries

- Keep quest payloads public-safe.
- Do not store private traces, secrets, raw transcripts, or local-only runtime
  evidence here.
- Do not promote one repeated observation into a stronger owner surface without
  reviewed evidence and a clear owner route.
- Route scenario composition to `aoa-playbooks` and proof to `aoa-evals`.

## Validation

When quests change, run:

```bash
python scripts/validate_memo.py
python scripts/release_check.py
```

## Closeout

Report which `AOA-MEM-Q-` or Agon quest surface changed, whether `QUESTBOOK.md`
changed, and which validation ran.
