"""Reading a CSV file into a :class:`csvstat.models.Table`.

The reader is local-only: it opens the given path, parses it with
:func:`csv.reader` and returns the data. It never touches the network and never
writes anything. Error messages name only the file name and the cause — never
cell values or input rows (see AC-10).
"""

import csv
import os

from csvstat.models import CsvStatError, Table


def _file_name(path: str) -> str:
    """Return just the file name of ``path`` for use in user-facing messages."""
    return os.path.basename(path) or path


def load_table(path: str, delimiter: str) -> Table:
    """Read ``path`` and return its header and data rows.

    The first row is the header, every following row is a data row. Raises
    :class:`CsvStatError` when the file is missing or unreadable, when it is
    empty, or when it has no data rows.
    """
    if not isinstance(delimiter, str) or len(delimiter) != 1:
        raise CsvStatError("delimiter must be a single character")

    name = _file_name(path)

    try:
        with open(path, newline="", encoding="utf-8") as handle:
            rows = list(csv.reader(handle, delimiter=delimiter))
    except FileNotFoundError:
        raise CsvStatError(f"{name}: file not found") from None
    except IsADirectoryError:
        raise CsvStatError(f"{name}: is a directory, not a file") from None
    except PermissionError:
        raise CsvStatError(f"{name}: permission denied") from None
    except UnicodeDecodeError:
        raise CsvStatError(f"{name}: not valid UTF-8 text") from None
    except csv.Error as exc:
        raise CsvStatError(f"{name}: invalid CSV ({exc})") from None
    except OSError as exc:
        raise CsvStatError(f"{name}: cannot be read ({exc.strerror or exc})") from None

    if not rows:
        raise CsvStatError(f"{name}: file is empty")

    header, data_rows = rows[0], rows[1:]
    if not data_rows:
        raise CsvStatError(f"{name}: file contains no data rows")

    return Table(header=header, rows=data_rows)
