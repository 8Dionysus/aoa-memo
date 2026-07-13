# aoa-memo local stats port

This directory exposes statistical questions whose domain meaning belongs to
`aoa-memo`. It uses the shared `aoa-stats` measurement grammar without moving
memory-object meaning or reviewed-corpus authority into the central organ.

## Current reference measurement

| Measurement | Question | Reference value |
| --- | --- | --- |
| `aoa-memo/reviewed-memory-object-count` | How many reviewed durable memory object bundles are present in the authored corpus? | `12` at source revision `166c8a7b732bc05838430d258167569cba07a4bf` |

The reference packet is a census of `memo/objects/**/object.json`. Reviewed
bundles and the corpus contract remain stronger than this packet.

## Authority

The count does not measure recall quality, truth, proof strength, freshness, or
live availability. `aoa-stats` may validate and compose the packet without
redefining memory meaning.

## Surfaces

- `port.manifest.json` declares the local question, measurement contract, and
  export.
- `packets/reviewed-memory-object-count.reference.json` records the
  evidence-linked reference observation.
- `memo/README.md`, `memo/OBJECT_SHAPE.md`, and
  `memo/objects/**/object.json` remain the owner evidence route.
