"""Memory/RAG/context validation profile for memo contracts."""

from __future__ import annotations

from .memory_context_contracts import *  # noqa: F401,F403
from .memory_context_profiles import *  # noqa: F401,F403
from .memory_context_readiness import *  # noqa: F401,F403
from .memory_context_registry import *  # noqa: F401,F403
from .questbook import validate_questbook_surface


def run() -> None:
    validate_memory_object_profiles()
    validate_trust_lifecycle_contracts()
    validate_memory_readiness_boundary_materialization()
    validate_memory_readiness_boundary_contract()
    validate_registry()
    validate_core_memory_contract()
    validate_checkpoint_to_memory_contract()
    validate_witness_trace_contract()
    validate_quest_chronicle_surface()
    validate_questbook_surface()
