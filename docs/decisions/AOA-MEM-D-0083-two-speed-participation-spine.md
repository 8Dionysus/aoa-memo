# Decision: Keep memory participation inside one two-speed owner family

- Decision ID: AOA-MEM-D-0083

## Status

Accepted on 2026-07-30 for source-local implementation, shadow observation,
and a reversible skill canary. Visible hook cues, semantic auto-write,
production activation, and landing remain deferred.

## Index Metadata

- Original date: 2026-07-30
- Surface classes: skills/home, consumer handoff, boundary/runtime/sibling
- Mechanic parents: consumer-handoff
- Guard families: skill admission, memory surface, sibling and boundary
- Memory object classes: decision
- Posture: active two-speed participation rationale

## Context

The admitted `aoa-memo` skill accurately handled an already material memory
artifact, but its prompt-visible trigger began with “Existing memo artifact”.
Natural session evidence showed reads and mentions of the bundle without a
structured invocation or outcome claim, while direct `aoa_memo_brief` use was
rare and concentrated in explicit memory or MCP research. A correct access
plane therefore existed without evidence that ordinary persistent Codex
sessions noticed when reviewed memory could help.

Making every prompt run the full recall package would add latency, context,
and distraction. A separate orientation skill would split one semantic family,
compete with `aoa-memo`, and duplicate its authority ceiling. Automatic packet
injection would reopen the proactive C contour before natural benefit is
established.

`aoa-session-memory` is a separate, self-sufficient session-evidence owner.
Its hooks and archive may supply refs, but `aoa-memo` participation cannot
depend on that repository or reuse its hook authority.

## Decision

Keep one advertised `aoa-memo` bundle and add an internal two-speed route:

- `orient` is the cheap normal entry for ongoing AoA/Abyss work where a
  reviewed prior decision, durable lesson, provenance constraint, or lifecycle
  fact could materially change the owner route or method;
- `recall`, `review`, and `evolve` remain the strict deep owner routes for an
  exact memory question or effect.

Fast orientation calls the existing read-only `aoa_memo_brief` once. It may
perform one bounded reviewed lexical search only when one specific prior
decision or lesson could change the route. MCP output remains a locator.
Current owner source must be verified before memory changes an answer or
action. No material hit, sufficient current source, stale or ambiguous memory,
and sibling-owner questions resolve to silence or handoff.

Add an `aoa-memo`-owned shadow hook fragment beside the consumer-handoff
contract. The hook observes only content-minimized lifecycle, opportunity, and
`aoa_memo` tool-result stages. It stores no prompt, tool input, tool response,
memory payload, model output, secret, semantic candidate, or source claim. It
returns no model-visible context, never blocks, never continues a turn, and
performs no model call.

The first evidence ladder is:

```text
eligible opportunity
  -> noticed (initially unknown)
  -> aoa_memo invoked
  -> result returned
  -> used or rejected (review required)
  -> task outcome (eval or owner evidence required)
```

An invocation or returned result cannot be reported as noticed use, action
change, or benefit. Shadow observation precedes the reversible skill canary.
A later selective route-only `UserPromptSubmit` cue requires a separate
operator-versioned policy and evidence gate; direct memory-packet injection
remains outside this decision.

## Alternatives

- Add a separate prompt-visible orientation skill. Rejected because the
  existing family already owns the trigger, source ceiling, silence posture,
  and deep escalation route.
- Run deep recall for every AoA/Abyss prompt. Rejected because most tasks
  should remain current-source-first and many correct outcomes require silence.
- Inject a memory packet from `UserPromptSubmit`. Rejected because it would
  turn an observability repair into proactive delivery before natural benefit.
- Reuse or modify `aoa-session-memory` hooks as the memo hook. Rejected because
  the repositories have independent owners, lifecycles, and standalone value.
- Count skill-file reads or MCP calls as use. Rejected because neither proves
  selection, material influence, action change, or outcome.

## Consequences

- Ordinary persistent sessions gain one discoverable memory-orientation entry
  without a new skill name.
- Exact memory work retains the strict source-return and mode package gates.
- Correct silence remains first-class and does not require a visible memory
  message.
- Shadow receipts can measure missed and excess invocation without retaining
  prompt or memory content.
- Outcome review remains necessary; hook health cannot become benefit proof.
- `aoa-session-memory` can cooperate through stable refs while remaining
  independently installable and operable.
- The hook definition needs exact Codex trust before live execution and must
  remain independently removable.

## Affected Surfaces

- `skills/aoa-memo/`
- `skills/port.manifest.json`
- `mechanics/consumer-handoff/parts/orchestrator-recall-alignment/`
- `aoa-evals:evals/comparison/fixed-baseline/aoa-memo-active-organ-offline-replay/`
- `abyss-stack` Codex hook composition and runtime receipt route

## Verification

Require:

- direct, indirect, incomplete, negative, and edge trigger cases;
- exact fast-lane silence and one-brief budget;
- deep-route package-gate preservation;
- raw-session and first-writeback handoffs;
- no dependency on `aoa-session-memory`;
- prompt-visible fresh-session inspection;
- hook schema, minimization, hash-chain, fail-open, concurrency, and no-output
  tests;
- held-out Codex sessions comparing current skill, two-speed skill, and later
  selective cue separately;
- natural review that distinguishes opportunity, invocation, delivery, use,
  action change, terminal outcome, cost, and operator burden.

Source checks, hook receipts, and fresh-session selection are mechanism
evidence only. Natural benefit, deployment, policy promotion, and landing
remain separate decisions.
