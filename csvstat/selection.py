"""Column selection for the ``--columns`` option.

Filled in by the "Add --columns selection with validation" ticket. The
signature is fixed by the shared interface.
"""


def select_columns(header: list[str], spec: str | None) -> list[str]:
    """Return the columns to analyse, in header order.

    ``None`` selects the whole header. A comma-separated ``spec`` selects
    exactly the named columns. An unknown name raises ``UnknownColumnError``.
    """
    return list(header)
