# Questbook Landing Log

## 2026-05-19

- Renamed `parts/public-index/` to `parts/obligation-index/` and
  `parts/generated-views/` to `parts/quest-read-model-projections/` so both
  public Questbook parts name their owned memo operation.
- Moved the Questbook source validator into
  `mechanics/questbook/parts/source-contract/scripts/`.
- Moved the generated quest projection builder into
  `mechanics/questbook/parts/quest-read-model-projections/scripts/`.
- Moved the Questbook regression into
  `mechanics/questbook/parts/source-contract/tests/`.
- Preserved the root `QUESTBOOK.md`, root `quests/`, and root generated
  projection outputs as intentional public surfaces.

Validation route:

Current executable routes live in the nearest `AGENTS.md` or `VALIDATION.md`
and in `config/validation_lanes.json`; historical run evidence remains in
Git and CI history.

## 2026-05-18

- Added `parts/quest-read-model-projections/` as the functioning-part contract for
  root-published Questbook generated read models.
- Kept `generated/quests/quest_catalog.min*.json` and
  `generated/quests/quest_dispatch.min*.json` in root `generated/` because they are
  public read models over root `quests/`, not package-local generated
  artifacts.
- Strengthened the Questbook validator so the part contract, root technical
  district family, required outputs, and builder agree.
- Preserved stop-lines: no source quest state, proof, route dispatch, playbook
  choreography, runtime state, role authority, owner acceptance, or private
  memory.

Validation route:

Current executable routes live in the nearest `AGENTS.md` or `VALIDATION.md`
and in `config/validation_lanes.json`; historical run evidence remains in
Git and CI history.

## 2026-05-18

- Added Questbook as the memo mechanic for public memory-layer obligations.
- Moved flat root quest sources into lane-first lifecycle directories under
  `quests/`.
- Added the generated quest projection builder to the Questbook mechanic.
- Added source-contract and quest-store validation for YAML and Markdown quest
  sources.

Validation route:

Current executable routes live in the nearest `AGENTS.md` or `VALIDATION.md`
and in `config/validation_lanes.json`; historical run evidence remains in
Git and CI history.

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.
