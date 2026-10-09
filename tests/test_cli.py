"""CLI-level tests for the csvstat skeleton.

These tests only assert the wiring the skeleton itself promises: the option
surface of ``--help`` and the error handling for bad input. They deliberately
say nothing about the stub return values of ``stats``/``report_*``, which later
tickets fill in.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Run ``python -m csvstat`` with ``args`` and capture its output."""
    return subprocess.run(
        [sys.executable, "-m", "csvstat", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_help_exits_zero_and_lists_options() -> None:
    result = run_cli("--help")

    assert result.returncode == 0
    assert "--delimiter" in result.stdout
    assert "--columns" in result.stdout
    assert "--json" in result.stdout


def test_missing_file_reports_error_on_stderr(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.csv"

    result = run_cli(str(missing))

    assert result.returncode != 0
    assert result.stderr.strip() != ""


def test_empty_file_reports_error_on_stderr(tmp_path: Path) -> None:
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")

    result = run_cli(str(empty))

    assert result.returncode != 0
    assert result.stderr.strip() != ""


def test_header_only_file_reports_error_on_stderr(tmp_path: Path) -> None:
    header_only = tmp_path / "header_only.csv"
    header_only.write_text("name,age\n", encoding="utf-8")

    result = run_cli(str(header_only))

    assert result.returncode != 0
    assert result.stderr.strip() != ""


@pytest.mark.parametrize("delimiter", ["", ";;"])
def test_delimiter_must_be_single_character(tmp_path: Path, delimiter: str) -> None:
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("a,b\n1,2\n", encoding="utf-8")

    result = run_cli("--delimiter", delimiter, str(csv_file))

    assert result.returncode != 0
