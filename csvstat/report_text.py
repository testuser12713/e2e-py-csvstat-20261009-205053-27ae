"""Plain-text report rendering.

Filled in by the "Implement per-column statistics and the plain-text report"
ticket. The signature is fixed by the shared interface.
"""

from csvstat.models import ColumnStats


def render(results: list[ColumnStats]) -> str:
    """Render ``results`` as a human-readable text report."""
    return ""
