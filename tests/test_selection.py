"""Tests for :func:`csvstat.selection.select_columns`."""

import pytest

from csvstat.models import CsvStatError, UnknownColumnError
from csvstat.selection import select_columns

HEADER = ["alpha", "beta", "gamma", "delta"]


def test_none_selects_whole_header() -> None:
    assert select_columns(HEADER, None) == HEADER


def test_empty_string_selects_whole_header() -> None:
    assert select_columns(HEADER, "") == HEADER


def test_whole_header_is_a_copy() -> None:
    result = select_columns(HEADER, None)
    result.append("extra")
    assert HEADER == ["alpha", "beta", "gamma", "delta"]


def test_subset_in_header_order() -> None:
    assert select_columns(HEADER, "delta,beta") == ["beta", "delta"]


def test_single_column() -> None:
    assert select_columns(HEADER, "gamma") == ["gamma"]


def test_whitespace_around_names_is_ignored() -> None:
    assert select_columns(HEADER, "  beta ,  delta ") == ["beta", "delta"]


def test_duplicate_names_are_reported_once() -> None:
    assert select_columns(HEADER, "beta,beta") == ["beta"]


def test_unknown_name_raises_and_names_only_that_column() -> None:
    with pytest.raises(UnknownColumnError) as excinfo:
        select_columns(HEADER, "beta,missing")

    error = excinfo.value
    assert error.column == "missing"
    assert "missing" in error.message
    for other in ("alpha", "beta", "gamma", "delta"):
        assert other not in error.message


def test_spec_without_any_name_raises() -> None:
    with pytest.raises(CsvStatError):
        select_columns(HEADER, ",")


def test_spec_with_only_whitespace_raises() -> None:
    with pytest.raises(CsvStatError):
        select_columns(HEADER, "  ,  ")
