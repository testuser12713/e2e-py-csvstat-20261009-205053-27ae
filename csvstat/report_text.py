"""Plain-text report rendering.

Filled in by the "Implement per-column statistics and the plain-text report"
ticket. The signature is fixed by the shared interface.
"""

from csvstat.models import ColumnStats


def _format_minmax(value: float) -> str:
    """Format a minimum/maximum value without unnecessary decimals."""
    if value == int(value):
        return str(int(value))
    return str(value)


def _format_block(result: ColumnStats) -> str:
    """Render a single column's statistics as its own block."""
    lines = [f"Spalte: {result.name}", f"Anzahl: {result.count}"]

    if result.kind == "numeric":
        if result.minimum is not None and result.maximum is not None:
            lines.append(f"Minimum: {_format_minmax(result.minimum)}")
            lines.append(f"Maximum: {_format_minmax(result.maximum)}")
        if result.mean is not None:
            lines.append(f"Mittelwert: {result.mean:.4f}")
        lines.append(f"Fehlende Werte: {result.missing}")
    else:
        lines.append(f"Fehlende Werte: {result.missing}")
        lines.append(f"Eindeutige Werte: {result.unique}")

    return "\n".join(lines)


def render(results: list[ColumnStats]) -> str:
    """Render ``results`` as a human-readable text report."""
    return "\n\n".join(_format_block(result) for result in results)
