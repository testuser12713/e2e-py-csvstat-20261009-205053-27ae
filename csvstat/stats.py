"""Per-column statistics computation.

Filled in by the "Implement per-column statistics" ticket. The signature is
fixed by the shared interface.
"""

from csvstat.models import ColumnStats, Table


def compute_stats(table: Table, columns: list[str]) -> list[ColumnStats]:
    """Compute statistics for ``columns``, one entry per column in that order."""
    return []
