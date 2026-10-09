"""Column selection for the ``--columns`` option.

``select_columns`` turns the raw ``--columns`` argument into the ordered list of
columns to analyse. ``None`` and the empty string mean "the whole header"; a
comma-separated spec names a subset. The result always follows header order, so
``--columns b,a`` reports ``a`` before ``b``.

Error messages name only a column (never a cell value or an input row), keeping
the privacy guarantees of AC-10.
"""

from csvstat.models import CsvStatError, UnknownColumnError


def _requested_names(spec: str) -> list[str]:
    """Split ``spec`` on commas and return the non-empty, stripped names."""
    names: list[str] = []
    for part in spec.split(","):
        name = part.strip()
        if name:
            names.append(name)
    return names


def select_columns(header: list[str], spec: str | None) -> list[str]:
    """Return the columns to analyse, in header order.

    ``None`` and the empty string select the whole header. A comma-separated
    ``spec`` selects exactly the named columns, ignoring surrounding whitespace
    and empty entries. An unknown name raises :class:`UnknownColumnError`; a
    spec that contains no name at all raises :class:`CsvStatError`.
    """
    if spec is None or spec == "":
        return list(header)

    requested = _requested_names(spec)
    if not requested:
        raise CsvStatError("no columns selected")

    header_set = set(header)
    for name in requested:
        if name not in header_set:
            raise UnknownColumnError(name)

    wanted = set(requested)
    return [column for column in header if column in wanted]
