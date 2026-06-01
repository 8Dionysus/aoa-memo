from __future__ import annotations

from memory_object_surface_common import (
    JsonDict,
    SECTION_SPECS,
    clean_sentence_fragment,
    related_object_ids,
    scope_classes_for,
    short_list,
    strongest_next_source,
    strongest_next_sources,
)


def catalog_item(
    memory_object: JsonDict,
    source_path: str,
    recall_modes: list[str],
    curated_ids: set[str],
    *,
    source_kind: str,
    include_full: bool,
) -> JsonDict:
    trust = memory_object["trust"]
    lifecycle = memory_object["lifecycle"]
    item: JsonDict = {
        "id": memory_object["id"],
        "kind": memory_object["kind"],
        "title": memory_object["title"],
        "summary": memory_object["summary"],
        "scope_classes": scope_classes_for(memory_object),
        "temperature": trust["temperature"],
        "review_state": lifecycle["review_state"],
        "current_recall_status": lifecycle["current_recall"]["status"],
        "authority_kind": trust["authority_kind"],
        "source_kind": source_kind,
        "primary_recall_modes": recall_modes,
        "source_path": source_path,
        "inspect_key": memory_object["id"],
        "expand_key": memory_object["id"],
    }
    if include_full:
        item.update(
            {
                "scope": memory_object["scope"],
                "provenance_thread_id": memory_object.get("provenance", {}).get("provenance_thread_id"),
                "related_object_ids": related_object_ids(memory_object, curated_ids),
                "strongest_next_sources": strongest_next_sources(memory_object),
            }
        )
    return item


def recall_posture_short(memory_object: JsonDict) -> str:
    lifecycle = memory_object["lifecycle"]
    current_recall = lifecycle["current_recall"]
    return (
        f"{current_recall['status']} current recall; "
        f"{lifecycle['review_state']} review state; "
        f"{clean_sentence_fragment(current_recall['status_reason'])}"
    )


def trust_posture_short(memory_object: JsonDict) -> str:
    trust = memory_object["trust"]
    return (
        f"{trust['temperature']} temperature; "
        f"{trust['authority_kind']} authority; "
        f"confidence {trust['confidence']:.2f}; "
        f"freshness {trust['freshness']:.2f}"
    )


def use_when_short(memory_object: JsonDict, recall_modes: list[str]) -> str:
    lifecycle = memory_object["lifecycle"]
    status = lifecycle["current_recall"]["status"]
    kind = memory_object["kind"]
    if status == "preferred":
        return f"Use as the current {kind} surface for {short_list(recall_modes)} recall."
    if status == "allowed":
        return f"Use when {kind}-level recall is needed and this object remains allowed for {short_list(recall_modes)}."
    if status == "historical":
        return f"Use only for trace-back or replacement history around this {kind}."
    return f"Inspect only when auditing why this {kind} was withdrawn."


def do_not_use_short(memory_object: JsonDict) -> str:
    lifecycle = memory_object["lifecycle"]
    current_recall = lifecycle["current_recall"]
    kind = memory_object["kind"]
    if current_recall["status"] == "withdrawn":
        return f"Do not treat this {kind} as current memo meaning."
    if current_recall["status"] == "historical":
        return f"Do not use this {kind} as the default current entrypoint."
    return f"Do not treat this {kind} as proof or stronger than its cited sources."


def capsules_item(memory_object: JsonDict, source_path: str, recall_modes: list[str], source_kind: str) -> JsonDict:
    return {
        "id": memory_object["id"],
        "kind": memory_object["kind"],
        "title": memory_object["title"],
        "summary": memory_object["summary"],
        "source_kind": source_kind,
        "recall_posture_short": recall_posture_short(memory_object),
        "trust_posture_short": trust_posture_short(memory_object),
        "use_when_short": use_when_short(memory_object, recall_modes),
        "do_not_use_short": do_not_use_short(memory_object),
        "strongest_next_source": strongest_next_source(memory_object, source_path),
        "source_path": source_path,
    }


def identity_summary(memory_object: JsonDict, recall_modes: list[str]) -> tuple[str, str]:
    lifecycle = memory_object["lifecycle"]
    current_recall = lifecycle["current_recall"]
    summary = (
        f"Names the {memory_object['kind']} surface, its active recall modes, "
        f"and its {current_recall['status']} current-recall posture."
    )
    payload_ref = memory_object.get("payload_ref")
    payload_text = f" Payload ref: {payload_ref}." if isinstance(payload_ref, str) and payload_ref else ""
    body = (
        f"{memory_object['title']}. {memory_object['summary']} "
        f"Scope: {short_list(memory_object['scope'])}. "
        f"Scope classes: {short_list(scope_classes_for(memory_object))}. "
        f"Primary recall modes: {short_list(recall_modes)}. "
        f"Current recall status: {current_recall['status']} because "
        f"{clean_sentence_fragment(current_recall['status_reason'])}.{payload_text}"
    )
    return summary, body


def provenance_summary(memory_object: JsonDict, curated_ids: set[str]) -> tuple[str, str]:
    provenance = memory_object["provenance"]
    sources = strongest_next_sources(memory_object)
    related_ids = related_object_ids(memory_object, curated_ids)
    summary = "Preserves source refs, provenance thread linkage, and related curated object ids for backward walk."
    body = (
        f"Provenance thread: {provenance.get('provenance_thread_id') or 'none'}. "
        f"Source refs: {short_list(list(provenance.get('source_refs', [])))}. "
        f"Episode refs: {short_list(list(provenance.get('episode_refs', [])))}. "
        f"Related curated object ids: {short_list(related_ids)}. "
        f"Strongest next sources: {short_list(sources)}."
    )
    return summary, body


def trust_summary(memory_object: JsonDict) -> tuple[str, str]:
    trust = memory_object["trust"]
    lifecycle = memory_object["lifecycle"]
    current_recall = lifecycle["current_recall"]
    freeze_basis = lifecycle.get("freeze_basis", {})
    freeze_text = ""
    if freeze_basis:
        freeze_text = (
            f" Freeze basis: {short_list(list(freeze_basis.get('qualifies_by', [])))}"
            f"{'; ' + clean_sentence_fragment(freeze_basis['note']) if freeze_basis.get('note') else ''}."
        )
    body = (
        f"Authority kind: {trust['authority_kind']} ({trust['authority']}). "
        f"Temperature: {trust['temperature']}; confidence {trust['confidence']:.2f}; "
        f"freshness {trust['freshness']:.2f}; salience {trust['salience']:.2f}. "
        f"Review state: {lifecycle['review_state']}. "
        f"Retention class: {lifecycle['retention_class']}. "
        f"Promotion state: {lifecycle.get('promotion_state', 'none')}. "
        f"Supersedes: {short_list(list(lifecycle.get('supersedes', [])))}. "
        f"Superseded by: {lifecycle.get('superseded_by') or 'none'}. "
        f"Replacement ref: {current_recall.get('replacement_ref') or 'none'}. "
        f"Contradiction refs: {short_list(list(current_recall.get('contradiction_refs', [])))}.{freeze_text}"
    )
    summary = "Summarizes trust posture, lifecycle posture, and contradiction or replacement visibility."
    return summary, body


def bridges_summary(memory_object: JsonDict, source_path: str) -> tuple[str, str]:
    bridges = memory_object.get("bridges", {})
    access = memory_object.get("access", {})
    summary = "Collects access posture, route capsule, and outward bridge refs without turning memory into routing policy."
    body = (
        f"Access class: {access.get('access_class', 'none')}. "
        f"Scope classes: {short_list(scope_classes_for(memory_object))}. "
        f"Read scopes: {short_list(list(access.get('read_scopes', [])))}. "
        f"Write scopes: {short_list(list(access.get('write_scopes', [])))}. "
        f"Promotion scopes: {short_list(list(access.get('promotion_scopes', [])))}. "
        f"Route capsule ref: {bridges.get('route_capsule_ref') or source_path}. "
        f"ToS refs: {short_list(list(bridges.get('tos_refs', [])))}. "
        f"Skill refs: {short_list(list(bridges.get('skill_refs', [])))}. "
        f"Eval refs: {short_list(list(bridges.get('eval_refs', [])))}. "
        f"KAG lift status: {bridges.get('kag_lift_status', 'none')}."
    )
    return summary, body


def sections_item(
    memory_object: JsonDict,
    source_path: str,
    recall_modes: list[str],
    curated_ids: set[str],
    source_kind: str,
) -> JsonDict:
    builders = [
        identity_summary(memory_object, recall_modes),
        provenance_summary(memory_object, curated_ids),
        trust_summary(memory_object),
        bridges_summary(memory_object, source_path),
    ]
    sections = []
    for index, ((section_key, heading), (summary, body)) in enumerate(zip(SECTION_SPECS, builders), start=1):
        sections.append(
            {
                "section_id": f"{memory_object['id']}#{section_key}",
                "heading": heading,
                "ordinal": index,
                "summary": summary,
                "body": body,
            }
        )
    return {
        "id": memory_object["id"],
        "kind": memory_object["kind"],
        "title": memory_object["title"],
        "source_kind": source_kind,
        "source_path": source_path,
        "sections": sections,
    }
