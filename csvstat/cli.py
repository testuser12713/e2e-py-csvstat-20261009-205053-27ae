"""Command-line interface of the csvstat tool.

Wiring: parse arguments, load the table, select columns, compute statistics and
print a text or JSON report to stdout. A :class:`CsvStatError` is reported as
``csvstat: <message>`` on stderr with exit code 2.
"""

import argparse
import sys
from collections.abc import Sequence

from csvstat import reader, report_json, report_text, selection, stats
from csvstat.models import CsvStatError


def _single_character(value: str) -> str:
    """Argparse type: accept exactly one character as the delimiter."""
    if len(value) != 1:
        raise argparse.ArgumentTypeError("must be a single character")
    return value


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the ``csvstat`` command."""
    parser = argparse.ArgumentParser(
        prog="csvstat",
        description="Print per-column statistics for a CSV file.",
    )
    parser.add_argument(
        "datei",
        metavar="DATEI",
        help="the CSV file to analyse",
    )
    parser.add_argument(
        "--delimiter",
        default=",",
        type=_single_character,
        metavar="Z",
        help="field delimiter, a single character (default: ',')",
    )
    parser.add_argument(
        "--columns",
        default=None,
        metavar="a,b",
        help="comma-separated list of columns to analyse (default: all)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json",
        help="print the report as JSON instead of plain text",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI. Returns the process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        table = reader.load_table(args.datei, args.delimiter)
        columns = selection.select_columns(table.header, args.columns)
        results = stats.compute_stats(table, columns)
        output = report_json.render(results) if args.json else report_text.render(results)
    except CsvStatError as exc:
        print(f"csvstat: {exc.message}", file=sys.stderr)
        return 2

    print(output)
    return 0
