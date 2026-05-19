# Checkpoint Parts Index

Functioning Checkpoint memo parts live here. Each part mirrors one active row in `../PARTS.md` and keeps its own contract and validation route.

## Parts

- [Checkpoint memory boundary](checkpoint-memory-boundary/README.md) - names what memo may preserve and what routes away
- [Checkpoint carry contract](checkpoint-carry-contract/README.md) - keeps pause, return, and carry refs bounded and reviewable
- [Approval and health records](approval-and-health-records/README.md) - maps approval and health examples into existing memory objects
- [Checkpoint-to-memory mapping](checkpoint-to-memory-mapping/README.md) - maps checkpoint artifacts into existing object kinds without creating checkpoint-only memory

## Validation

Executable part validation lives in [parts/AGENTS](AGENTS.md#validation) and the package [AGENTS](../AGENTS.md#validation).
