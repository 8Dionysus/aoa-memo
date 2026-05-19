# AGENTS.md

## Guidance for `quests/`

`quests/` holds the public item store for memory-layer obligations that are
summarized from `QUESTBOOK.md` and validated as public repo state.

Quest files may track memo-facing recall, writeback, recurrence, and adoption
obligations. They do not own playbook scenario composition, proof outcomes,
runtime retention, or agent role rights.

## Current Shape

Quest sources use lane-first lifecycle placement:

- `quests/memo/<state>/AOA-MEM-Q-*.yaml`
- `quests/agon/<state>/AOM-Q-AGON-*.md`
- `quests/agon/<state>/AOMEMO-Q-AGON-*.md`

Questbook law lives in `mechanics/questbook/`. The root `quests/` district is
the source item store, not a private scratchpad and not a package-local docs
directory.

Keep `QUESTBOOK.md`, `quests/`, owning mechanic docs, and generated quest
companions aligned. Root generated quest companions are projections from these
source files, not a second quest ledger.

## Route Stack

- Above: root `AGENTS.md`, `QUESTBOOK.md`, and the Questbook mechanic set the
  public obligation route.
- Here: `quests/` owns lane-first source files for memo-facing obligations.
- Below: `quests/<lane>/<state>/` holds source objects. Generated quest
  catalogs and dispatch files are read models only.

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
python scripts/memory/validate_memo.py
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/release/release_check.py
```

## Closeout

Report which quest lane and lifecycle state changed, whether `QUESTBOOK.md`
changed, whether generated quest projections were rebuilt, and which
validation ran.
