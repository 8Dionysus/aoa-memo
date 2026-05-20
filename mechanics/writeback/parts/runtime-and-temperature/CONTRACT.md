# Runtime and temperature Contract

## Owner Boundary

`aoa-memo` owns this part only as a bounded memory-layer operation inside `mechanics/writeback/`.

Stronger claims route through `../../OWNER_MAP.md`. Source placement and legacy context route through `../../PROVENANCE.md` and `../../legacy/`.

## Source Surfaces

- [RUNTIME_WRITEBACK_SEAM](../../docs/RUNTIME_WRITEBACK_SEAM.md)
- [WRITEBACK_TEMPERATURE_POLICY](../../docs/WRITEBACK_TEMPERATURE_POLICY.md)
- `schemas/reviewed_memory_intake_packet_v1.json`
- `examples/reviewed_memory_intake_packet.abyss-stack.example.json`
- `examples/reviewed_memory_intake_packet.abyss-machine.example.json`

## Contract

keeps runtime writeback mapped without runtime ownership

The runtime target schema, generated runtime target/intake/governance surfaces,
reviewed intake packet schema, packet examples, and their builders are
part-local here. They may describe memo-side runtime writeback posture, but
they must not become live runtime storage or worker scheduling.

## Stop-lines

This part inherits the package stop-lines from `../../README.md#must-not-claim` and `../../OWNER_MAP.md`.

It must not become proof, runtime execution, route dispatch, role authority,
KAG substrate truth, playbook choreography, stats truth, ToS canon, source-owner
acceptance, or private memory unless a stronger owner accepts that work in its
own repository.
