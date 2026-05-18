# AGENTS.md

## Applies To

This card applies to `mechanics/lineage-harvest/docs/`.

## Role

This directory holds active mechanic-owned doctrine for the lineage-harvest
mechanic.

It is not a schema home, generated-output home, runtime ledger, proof record,
KAG promotion dossier, ToS canon route, stats report, or source-owner adoption
record.

## Read Before Editing

Read:

1. `mechanics/lineage-harvest/AGENTS.md`
2. `mechanics/lineage-harvest/README.md`
3. `mechanics/lineage-harvest/OWNER_MAP.md`
4. `mechanics/lineage-harvest/PARTS.md`
5. `mechanics/ARTIFACT_TOPOLOGY.md` if non-doc artifacts may move

## Boundaries

- Keep active lineage-harvest docs under this directory.
- Keep root technical artifacts in root districts while
  `mechanics/ARTIFACT_TOPOLOGY.md` says they are public support contracts.
- Do not reintroduce an active flat docs-root copy.
- Do not grant proof, KAG promotion, ToS canon, stats certification, runtime
  execution, source-owner consent, or adoption authority.

## Validation

After editing active docs, run:

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_memo.py
```

For release-bound work, also run:

```bash
python scripts/release_check.py
```
