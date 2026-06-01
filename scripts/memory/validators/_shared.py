"""Compatibility re-export for memo validator shared support."""

from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timedelta
from functools import lru_cache
import os
from pathlib import Path
import re
import sys

try:
    from jsonschema import Draft202012Validator, FormatChecker
    from referencing import Registry, Resource
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: jsonschema. Install it with: pip install jsonschema")
    raise SystemExit(2) from exc

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("Missing dependency: PyYAML. Install it with: pip install PyYAML")
    raise SystemExit(2) from exc

from ._shared_datetime import *  # noqa: F401,F403
from ._shared_io import *  # noqa: F401,F403
from ._shared_paths import *  # noqa: F401,F403
from ._shared_quest_constants import *  # noqa: F401,F403
from ._shared_refs import *  # noqa: F401,F403
from ._shared_schema import *  # noqa: F401,F403
from ._shared_schema_constants import *  # noqa: F401,F403
