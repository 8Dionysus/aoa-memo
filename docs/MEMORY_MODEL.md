# Memory Model

This document defines the conceptual model of the AoA memory layer.

## Why a memory layer exists

AoA needs more than reusable practice, bounded execution, and bounded proof.
It also needs memory that can accumulate without collapsing the distinction between:
- what happened
- what is reusable
- what should be done next
- what can be honestly defended as proof

The memory layer exists to make recall explicit and structured rather than invisible and accidental.

## What counts as memory here

Within `aoa-memo`, memory should mean reviewable surfaces such as:
- memory objects
- provenance threads
- temporal recall handles
- salience-oriented recall surfaces
- episodic and semantic memory distinctions when useful

## Memory classes

The first useful distinction is between:

### Episodic memory

Memory about a concrete event, interaction, run, change, or episode.

Typical examples:
- a change sequence that happened in a repository
- a prior agent run and its result
- a conversation-derived memory object
- a notable decision with temporal context

### Semantic memory

Memory about stable meaning abstracted across episodes.

Typical examples:
- a durable system fact
- a stable repository role
- a named ownership boundary
- a persistent conceptual distinction

### Provenance thread

A memory surface that helps answer:
- where did this come from?
- what shaped it?
- what earlier object or event should it be traced back to?

## What memory must not do

Memory should not silently become:
- proof
- workflow execution
- reusable practice canon
- routing dispatch

Memory may support all of those layers, but it should not replace them.

## Memory temperature and salience

As AoA matures, memory will likely need bounded ways to express:
- freshness
- relevance
- recurrence
- salience
- decayed importance

These should be treated as explicit reviewable surfaces, not invisible heuristics.

## Recall discipline

A good memory surface should make it easier to answer:
- what should be recalled right now?
- why this memory rather than another?
- how recent or durable is it?
- what object or episode gave rise to it?

## Relationship to neighboring layers

- `aoa-techniques` stores reusable practice
- `aoa-skills` stores bounded execution
- `aoa-evals` stores bounded proof
- `aoa-routing` stores navigation and dispatch
- `aoa-memo` stores memory and recall surfaces

## Compact principle

Memory should make the past more usable without making truth more vague.
