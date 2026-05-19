# Questbook Generated Views Contract

## Contract

Questbook generated views are root-published read models over the public
lane-first quest store.

They live in root `generated/` because they are consumed outside one mechanic
package. The Questbook mechanic owns their source contract, builder, validation,
and stop-lines. The generated files do not author quest meaning.

In `../../PARTS.md` terms, they are root-published read models that never author quest meaning.

## Required Outputs

- `generated/quest_catalog.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_dispatch.min.example.json`

## Required Builder

- `mechanics/questbook/parts/generated-views/scripts/build_quest_surfaces.py`

## Part-Local Artifacts

- `mechanics/questbook/parts/generated-views/scripts/build_quest_surfaces.py`

## Required Family

`config/root_technical_districts.json` must keep a `questbook_projections`
generated family with:

- `source_kind`: `projection`
- `owner_surface`: `mechanics/questbook/README.md`
- outputs matching the required output list
- builder matching the required builder

## Stop-lines

Generated Questbook views must not become:

- source quest state
- proof or closure verdict
- route dispatch authority
- playbook choreography
- runtime scheduling or live state
- role authority
- owner acceptance
- private memory
