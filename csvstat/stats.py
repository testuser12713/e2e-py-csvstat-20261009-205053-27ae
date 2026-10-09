"""Per-column statistics computation.

Filled in by the "Implement per-column statistics" ticket. The signature is
fixed by the shared interface.
"""

import statistics

from csvstat.models import ColumnStats, Table


def _cell(row: list[str], index: int) -> str:
    """Return the cell at ``index``, treating a short row as an empty cell."""
    return row[index] if index < len(row) else ""


def _is_float(value: str) -> bool:
    """Return whether ``value`` parses as a float."""
    try:
        float(value)
    except ValueError:
        return False
    return True


def compute_stats(table: Table, columns: list[str]) -> list[ColumnStats]:
    """Compute statistics for ``columns``, one entry per column in that order."""
    results: list[ColumnStats] = []

    for name in columns:
        index = table.header.index(name)
        cells = [_cell(row, index) for row in table.rows]
        non_empty = [cell for cell in cells if cell != ""]

        if all(_is_float(cell) for cell in non_empty):
            numbers = [float(cell) for cell in non_empty]
            if numbers:
                minimum = min(numbers)
                maximum = max(numbers)
                mean: float | None = round(statistics.fmean(numbers), 4)
            else:
                minimum = maximum = mean = None
            results.append(
                ColumnStats(
                    name=name,
                    kind="numeric",
                    count=len(non_empty),
                    minimum=minimum,
                    maximum=maximum,
                    mean=mean,
                    missing=len(cells) - len(non_empty),
                    unique=None,
                )
            )
        else:
            results.append(
                ColumnStats(
                    name=name,
                    kind="text",
                    count=len(non_empty),
                    minimum=None,
                    maximum=None,
                    mean=None,
                    missing=len(cells) - len(non_empty),
                    unique=len(set(non_empty)),
                )
            )

    return results
