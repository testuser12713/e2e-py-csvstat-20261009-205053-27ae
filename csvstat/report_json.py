"""JSON report rendering.

Filled in by the "Add the JSON output" ticket. The signature is fixed by the
shared interface.
"""

import json
import math
from typing import Any

from csvstat.models import ColumnStats


def _finite(value: float | None) -> float | None:
    """Return ``value`` if it is a finite number, otherwise ``None``.

    JSON has no representation for NaN or Infinity; emitting them would make
    the document invalid, so such values degrade to ``null``.
    """
    if value is None:
        return None
    if math.isfinite(value):
        return value
    return None


def _column_object(result: ColumnStats) -> dict[str, Any]:
    """Build the JSON object for a single column."""
    return {
        "column": result.name,
        "type": result.kind,
        "count": result.count,
        "min": _finite(result.minimum),
        "max": _finite(result.maximum),
        "mean": _finite(result.mean),
        "missing": result.missing,
        "unique": result.unique,
    }


def render(results: list[ColumnStats]) -> str:
    """Render ``results`` as a JSON list of column-statistic objects."""
    payload = [_column_object(result) for result in results]
    return json.dumps(payload, ensure_ascii=False, allow_nan=False)
