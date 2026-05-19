# Spark Scenario: generated-parity-check

Use `generated-parity-check` to compare an authored source, builder, generated
companion, and validator.

## Scope

Inspect one generated family or one generated file and its source-backed
builder route. Rebuild generated output only when the user asks for repair and
the builder route is clear.

## Done Signal

Source, builder, generated output, and validation route agree, or the mismatch
is evidenced and routed.

## Stop-line

Do not hand-edit generated companions as source truth.

## Handoff Route

Write a handoff when the source is unclear, the generator is missing, generated
output carries new meaning, or the owner route crosses repositories.

## Validation

Run the `--check` builder command and validator named by the generated surface.
