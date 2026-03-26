# Spark lane for aoa-memo

This file only governs work started from `Spark/`.

The root `AGENTS.md` remains authoritative for repository identity, ownership boundaries, reading order, and validation commands. This local file only narrows how GPT-5.3-Codex-Spark should behave when used as the fast-loop lane.

If `SWARM.md` exists in this directory, treat it as queue / swarm context. This `AGENTS.md` is the operating policy for Spark work.

## Default Spark posture

- Use Spark for short-loop work where a small diff is enough.
- Start with a map: task, files, risks, and validation path.
- Prefer one bounded patch per loop.
- Read the nearest source docs before editing.
- Use the narrowest relevant validation already documented by the repo.
- Report exactly what was and was not checked.
- Escalate instead of widening into a broad architectural rewrite.

## Spark is strongest here for

- recall-contract docs, examples, and schema cleanup
- provenance, salience, temperature, or lifecycle wording alignment
- generated memory-surface sync work
- tight audits of temporal posture and reviewability
- small object-profile clarity fixes

## Do not widen Spark here into

- treating memory as proof
- rewriting role policy, routing logic, or scenario logic here
- collapsing episodic, semantic, and provenance distinctions
- writing objects that pretend to be current truth without temporal framing

## Local done signal

A Spark task is done here when:

- memory remains explicit and bounded
- provenance is still visible
- temporal and salience posture are clearer
- generated outputs are aligned when touched
- the documented validation path ran when relevant

## Local note

Spark should behave like a curator of bounded traces here, not like a myth-maker of memory authority.

## Reporting contract

Always report:

- the restated task and touched scope
- which files or surfaces changed
- whether the change was semantic, structural, or clarity-only
- what validation actually ran
- what still needs a slower model or human review
