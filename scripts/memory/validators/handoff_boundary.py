"""Inter-agent handoff and export-boundary validation profile."""

from __future__ import annotations

from .handoff_boundary_bridge import *  # noqa: F401,F403
from .handoff_boundary_kag import *  # noqa: F401,F403
from .handoff_boundary_playbook import *  # noqa: F401,F403
from .handoff_boundary_routing import *  # noqa: F401,F403

def run() -> None:
    validate_routing_memory_adoption_surface()
    validate_playbook_memory_scope_surface()
    validate_bridge_export_contracts()
    validate_kag_source_export()
