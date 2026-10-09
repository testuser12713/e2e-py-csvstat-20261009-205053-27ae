"""Shared data types of the csvstat CLI.

These definitions are the contract every other module builds on. They are
deliberately small and carry no logic.
"""

from dataclasses import dataclass


@dataclass
class Table:
    """A parsed CSV file: the header row and all following data rows."""

    header: list[str]
    rows: list[list[str]]


@dataclass
class ColumnStats:
    """Statistics computed for a single column.

    ``kind`` is either ``"numeric"`` or ``"text"``.
    ``count`` is the number of non-empty cells.
    ``missing`` counts empty plus unparsable cells.
    ``unique`` is only set for text columns, otherwise ``None``.
    """

    name: str
    kind: str
    count: int
    minimum: float | None
    maximum: float | None
    mean: float | None
    missing: int
    unique: int | None


class CsvStatError(Exception):
    """A user-facing error.

    ``message`` names only the file name, the column name and the cause —
    never a cell value or an input row.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class UnknownColumnError(CsvStatError):
    """Raised when ``--columns`` names a column that is not in the header."""

    def __init__(self, column: str) -> None:
        super().__init__(f"unknown column: {column}")
        self.column = column
