# Reviewed Memory Corpus

`memo/` is the reviewed memory corpus for `aoa-memo`.

Other repositories use `repo/memo/` as a local memory port for candidates,
receipts, exports, and local notes. This directory is different: it is the
source-owned home for reviewed memory objects after they land in `aoa-memo`.

## Why This Exists

`aoa-memo` already owns memory doctrine, schemas, examples, generated read
models, local memo port standards, and memo mechanics. The missing surface was
the corpus itself: a place where reviewed memory objects can live as durable
repo-owned objects instead of remaining only examples, generated projections, or
external local-port packets.

## Layout

```text
memo/
  AGENTS.md
  README.md
  OBJECT_SHAPE.md

  objects/
    anchors/
    state-capsules/
    episodes/
    claims/
    decisions/
    patterns/
    bridges/
    audit-events/

  support/
    provenance-threads/
    recall-contracts/

  intake/
    reviewed/
    quarantine/
    receipts/
```

## Object Bundle

Each reviewed object uses a bundle:

```text
memo/objects/<kind-dir>/<year>/<slug>/
  object.json
  MEMO.md
```

- `object.json` is machine truth: schema-backed, provenance-linked, lifecycle
  aware, and stable enough for generated read models.
- `MEMO.md` is the human companion: compact orientation, rationale, source
  route, and review posture.

The bundle keeps the object inspectable without forcing every long-form note
into JSON and without making Markdown the only durable record.

## Read Path

Start with `AGENTS.md`, then use `OBJECT_SHAPE.md` for the storage contract.
For object meaning, route to the bundle's `object.json`, its `MEMO.md`, and the
source refs named in `provenance.source_refs`.

Generated consumers should treat `memo/objects/**/object.json` as the future
corpus source and keep `generated/` as read-model output.

## Write Path

Reviewed memory lands here by a bounded source change in `aoa-memo`:

1. receive or prepare reviewed intake;
2. require the origin export packet to allow `reviewed_write`;
3. check evidence, owner route, poisoning risk, lifecycle, provenance, and
   local validation receipts;
4. run `scripts/memory/land_reviewed_memo_intake.py` first as a dry-run plan,
   then with `--write` after review accepts the target object bundle;
5. run corpus validation and generated read-model checks;
6. publish generated/read-model updates after the object lands.

## First Bundle

The first object records this placement decision:

`memo/objects/decisions/2026/reviewed-corpus-district/`

Its decision rationale also lives in
`docs/decisions/AOA-MEM-D-0063-reviewed-memory-corpus-district.md`.
