# Agon Landing Log

## 2026-05-19

- Moved Agon config, examples, generated registries, schemas, scripts, tests,
  recurrence manifests, and hook bindings from package-level technical homes
  into their nearest functioning parts.
- Kept prebinding and retention-rank candidate intake under
  `parts/prebinding-and-candidate-intake/`.
- Kept bridge, KAG, SLC, Sophian, VDS, and mechanical-trial memo companions
  under `parts/bridge-and-evidence-seams/`.
- Kept wave recurrence manifests under `parts/wave-landing-and-stop-lines/`
  with a manifest reference regression test.

Validation route:

```bash
python scripts/validate_mechanic_artifact_inventory.py
python -m pytest -q mechanics/agon/parts/prebinding-and-candidate-intake/tests mechanics/agon/parts/bridge-and-evidence-seams/tests mechanics/agon/parts/wave-landing-and-stop-lines/tests
python scripts/release_check.py
```

## 2026-05-18

- Landed Agon as a memo mechanic package.
- Moved active Agon source docs from the transitional `mechanics/agon/docs/` district
  into `mechanics/agon/docs/`.
- Preserved former flat docs-root and docs-district lineage through the legacy
  index.
- Added owner map, provenance bridge, package card, and mechanics validation.
- Moved Agon-specific quest follow-through notes from flat root `quests/` into
  the public `quests/agon/ready/` lane and gave them the memo Markdown quest
  source contract.

Validation route:

```bash
python mechanics/questbook/scripts/validate_quest_store.py
python scripts/validate_memo_mechanics.py
python -m pytest -q mechanics/agon/parts/prebinding-and-candidate-intake/tests mechanics/agon/parts/bridge-and-evidence-seams/tests mechanics/agon/parts/wave-landing-and-stop-lines/tests
python scripts/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.
