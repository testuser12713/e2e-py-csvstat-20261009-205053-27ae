"""JSON report rendering.

Filled in by the "Add the JSON output" ticket. The signature is fixed by the
shared interface.
"""

from csvstat.models import ColumnStats


def render(results: list[ColumnStats]) -> str:
    """Render ``results`` as a JSON list of column-statistic objects."""
    return "[]"
