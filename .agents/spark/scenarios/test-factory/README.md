# Spark Scenario: test-factory

Use `test-factory` to add bounded tests for an already clear memory contract.

## Scope

Add or adjust a small test around an existing source-backed contract,
validator, schema, generated-parity rule, or route-card invariant.

## Done Signal

Tests prove a named existing memory contract and pass locally.

## Stop-line

Do not invent new memory semantics to make tests interesting.

## Handoff Route

Write a handoff when the contract itself is unclear, belongs to a sibling
owner, or requires broad invariant design before testing.

## Validation

Run the targeted test command and the owning source-surface validator when one
is named.
