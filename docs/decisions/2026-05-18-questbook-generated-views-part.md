# Questbook Generated Views Part

## Context

Questbook projections are built by the Questbook mechanic but published under
root `generated/`. This can look like placement debt if the only rule is that
mechanic-owned generated artifacts belong under `mechanics/<slug>/generated/`.

The stronger pattern from Agents-of-Abyss keeps Questbook generated views as
root-published read models over the public `quests/` store, while the Questbook
mechanic owns the contracts, builders, validators, and stop-lines. `aoa-memo`
already followed that placement in `generated/AGENTS.md` and
`mechanics/ARTIFACT_TOPOLOGY.md`, but the Questbook package did not have a
part-level contract that future agents could inspect.

## Decision

Add `mechanics/questbook/parts/generated-views/` as the functioning-part
contract for root-published Questbook generated read models.

Keep these outputs in root `generated/`:

- `generated/quest_catalog.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_dispatch.min.example.json`

Strengthen `mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py` so it checks
the generated-view part files, the required output list, the required builder,
and the `questbook_projections` family in
`config/root_technical_districts.json`.

## Consequences

- Questbook generated views are no longer an implicit root exception.
- The root generated placement is machine-checked from the owning mechanic's
  validator.
- Future package-local generated artifacts may still move under a mechanic
  when they serve only one mechanic boundary.
- This does not make generated quest views source quest state, proof, route
  dispatch, playbook choreography, runtime state, role authority, owner
  acceptance, or private memory.

## Verification

Use:

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/generated-views/scripts/build_quest_surfaces.py --check
python scripts/validate_memo_mechanic_parts.py
python -m pytest -q mechanics/questbook/parts/source-contract/tests/test_questbook_store.py tests/test_memo_mechanic_parts.py
python scripts/release_check.py
```
