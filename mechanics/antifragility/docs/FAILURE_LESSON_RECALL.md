# FAILURE LESSON RECALL

## Goal

Recall prior failure lessons when they can improve posture, not when they merely add noise.

## Preferred query shapes

Useful queries are usually narrow:

- repo + surface + stressor family
- repo + degraded mode
- service + incident class
- owner repo + adaptation family

Examples:

- `ATM10-Agent + hybrid-query + retrieval_only_fallback`
- `abyss-stack + langchain-api + upstream_model_path_unhealthy`

## What a recall result should answer

A bounded recall result should help answer:

- have we seen something close to this before
- what posture previously helped
- what should be inspected first
- what action should remain blocked until review

## Precedence reminder

For current truth, prefer:

1. source-owned receipts
2. owner-local current artifacts
3. bounded eval outputs
4. memo recall as contextual support

Memo may shape attention.
It does not overrule source-owned evidence.

## Freshness and suppression

Suppress or cool recall when:

- the lesson is stale
- the lesson is still a draft
- the current evidence window is too weak
- a newer lesson supersedes it

Temperature and salience should help, but not replace, explicit trust signals.

## Suggested recall surface behavior

A healthy failure-lesson recall surface should expose:

- the lesson summary
- source receipt refs
- optional adaptation refs
- trust posture
- one recommended posture sentence
- one note about what remains uncertain
