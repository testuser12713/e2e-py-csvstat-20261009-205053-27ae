"""Tests for :func:`csvstat.stats.compute_stats`."""

from pathlib import Path

from csvstat import reader
from csvstat.models import Table
from csvstat.stats import compute_stats


def test_numeric_column_statistics() -> None:
    table = Table(header=["age"], rows=[["1"], ["2"], ["3"]])

    (result,) = compute_stats(table, ["age"])

    assert result.name == "age"
    assert result.kind == "numeric"
    assert result.count == 3
    assert result.minimum == 1
    assert result.maximum == 3
    assert result.mean == 2.0
    assert result.missing == 0
    assert result.unique is None


def test_text_column_statistics() -> None:
    table = Table(header=["name"], rows=[["a"], ["b"], ["a"], ["c"]])

    (result,) = compute_stats(table, ["name"])

    assert result.kind == "text"
    assert result.count == 4
    assert result.minimum is None
    assert result.maximum is None
    assert result.mean is None
    assert result.missing == 0
    assert result.unique == 3


def test_empty_cells_are_excluded_from_numeric_stats() -> None:
    table = Table(header=["v"], rows=[["1"], [""], ["3"], ["5"]])

    (result,) = compute_stats(table, ["v"])

    assert result.kind == "numeric"
    assert result.count == 3
    assert result.minimum == 1
    assert result.maximum == 5
    assert result.mean == 3.0
    assert result.missing == 1


def test_non_numeric_cell_makes_column_text() -> None:
    table = Table(header=["v"], rows=[["1"], ["x"], ["3"]])

    (result,) = compute_stats(table, ["v"])

    assert result.kind == "text"
    assert result.count == 3
    assert result.missing == 0
    assert result.unique == 3
    assert result.minimum is None
    assert result.mean is None


def test_all_empty_column_has_no_numeric_values() -> None:
    table = Table(header=["v"], rows=[[""], [""]])

    (result,) = compute_stats(table, ["v"])

    assert result.kind == "numeric"
    assert result.count == 0
    assert result.minimum is None
    assert result.maximum is None
    assert result.mean is None
    assert result.missing == 2
    assert result.unique is None


def test_mean_is_rounded_to_four_decimals() -> None:
    table = Table(header=["v"], rows=[["1"], ["2"], ["2"]])

    (result,) = compute_stats(table, ["v"])

    assert result.mean == 1.6667


def test_columns_are_returned_in_requested_order() -> None:
    table = Table(header=["a", "b", "c"], rows=[["1", "2", "3"]])

    results = compute_stats(table, ["c", "a"])

    assert [result.name for result in results] == ["c", "a"]


def test_semicolon_delimited_file(tmp_path: Path) -> None:
    csv_file = tmp_path / "data.csv"
    csv_file.write_text("name;age\nalice;30\nbob;40\n", encoding="utf-8")

    table = reader.load_table(str(csv_file), ";")
    results = compute_stats(table, table.header)
    by_name = {result.name: result for result in results}

    assert by_name["name"].kind == "text"
    assert by_name["name"].unique == 2
    assert by_name["age"].kind == "numeric"
    assert by_name["age"].count == 2
    assert by_name["age"].minimum == 30
    assert by_name["age"].maximum == 40
    assert by_name["age"].mean == 35.0
