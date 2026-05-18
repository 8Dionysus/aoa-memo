# AGENTS.md

## Guidance for `docs/agon/`

`docs/agon/` owns memo-side Agon memory seams that were formerly flat
Agon docs-root surfaces.

This district keeps Agon candidate memory, bridge, retention, evidence, and
wave landing notes together while preserving the same boundary: `aoa-memo`
remembers candidate context and source refs; it does not run trials, write
durable scars, mutate rank, decide verdicts, or promote Tree-of-Sophia canon.

## Read Before Editing

Start with:

1. root `AGENTS.md`
2. `docs/AGENTS.md`
3. `docs/README.md`
4. `docs/ROOT_SURFACE_LAW.md`
5. this file
6. `docs/agon/README.md`
7. the target Agon doc plus matching config, schema, generated registry,
   manifest, quest, and test surfaces when they exist

## Boundaries

- Keep Agon memory surfaces candidate-only unless a stronger owner has already
  provided reviewed source evidence.
- Do not move verdict law, arena execution, rank mutation, durable scar writes,
  stats authority, KAG promotion, or authored canon here.
- Route proof to `aoa-evals`, role or rights policy to `aoa-agents`, graph lift
  to `aoa-kag`, source doctrine to `Agents-of-Abyss` or `Tree-of-Sophia`, and
  runtime storage to `abyss-stack`.
- Keep links and manifests pointed at `docs/agon/`, not the old flat docs-root
  paths.

## Validation

For Agon district edits, run the narrow docs-district gate and the affected
Agon validators:

```bash
python scripts/validate_docs_districts.py
python scripts/validate_agon_memo_prebindings.py
python scripts/validate_agon_epistemic_memo_bridge.py
python scripts/validate_agon_kag_memo_evidence_package_registry.py
python scripts/validate_agon_mechanical_trial_memo_intakes.py
python scripts/validate_agon_retention_rank_memo_bridge.py
python scripts/validate_agon_slc_memo_bridge_registry.py
python scripts/validate_agon_sophian_memo_evidence_registry.py
python scripts/validate_agon_vds_memo_bridge.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report which Agon source family changed, whether any config, generated,
manifest, quest, schema, example, or test surfaces changed, and whether any
old flat Agon docs-root reference remains.
