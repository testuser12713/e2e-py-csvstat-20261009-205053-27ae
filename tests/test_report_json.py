"""Tests for the JSON report rendering."""

import json

from csvstat.models import ColumnStats
from csvstat.report_json import render


def _numeric(name: str = "price") -> ColumnStats:
    return ColumnStats(
        name=name,
        kind="numeric",
        count=7,
        minimum=1.5,
        maximum=99.25,
        mean=12.3457,
        missing=2,
        unique=None,
    )


def _text(name: str = "city") -> ColumnStats:
    return ColumnStats(
        name=name,
        kind="text",
        count=5,
        minimum=None,
        maximum=None,
        mean=None,
        missing=1,
        unique=4,
    )


def test_render_is_valid_json() -> None:
    parsed = json.loads(render([_numeric()]))
    assert isinstance(parsed, list)
    assert len(parsed) == 1


def test_render_one_object_per_column_in_order() -> None:
    parsed = json.loads(render([_text("a"), _numeric("b"), _text("c")]))
    assert [item["column"] for item in parsed] == ["a", "b", "c"]


def test_render_has_expected_keys() -> None:
    item = json.loads(render([_numeric()]))[0]
    assert set(item) == {
        "column",
        "type",
        "count",
        "min",
        "max",
        "mean",
        "missing",
        "unique",
    }


def test_numeric_figures_match_input_stats() -> None:
    stats = _numeric()
    item = json.loads(render([stats]))[0]
    assert item["column"] == stats.name
    assert item["type"] == "numeric"
    assert item["count"] == stats.count
    assert item["min"] == stats.minimum
    assert item["max"] == stats.maximum
    assert item["mean"] == stats.mean
    assert item["missing"] == stats.missing
    assert item["unique"] is None


def test_text_figures_match_input_stats() -> None:
    stats = _text()
    item = json.loads(render([stats]))[0]
    assert item["type"] == "text"
    assert item["count"] == stats.count
    assert item["min"] is None
    assert item["max"] is None
    assert item["mean"] is None
    assert item["missing"] == stats.missing
    assert item["unique"] == stats.unique


def test_mean_keeps_four_decimal_rounding() -> None:
    stats = _numeric()
    stats.mean = round(12.34567, 4)
    item = json.loads(render([stats]))[0]
    assert item["mean"] == 12.3457


def test_non_applicable_values_are_null() -> None:
    item = json.loads(render([_text()]))[0]
    assert item["min"] is None
    assert item["max"] is None
    assert item["mean"] is None


def test_non_finite_values_become_null() -> None:
    stats = _numeric()
    stats.minimum = float("nan")
    stats.maximum = float("inf")
    stats.mean = float("-inf")
    text = render([stats])
    assert "NaN" not in text
    assert "Infinity" not in text
    item = json.loads(text)[0]
    assert item["min"] is None
    assert item["max"] is None
    assert item["mean"] is None


def test_empty_results_render_empty_list() -> None:
    assert json.loads(render([])) == []


def test_render_never_emits_non_finite_json() -> None:
    for value in (float("nan"), float("inf"), float("-inf")):
        stats = _numeric()
        stats.mean = value
        parsed = json.loads(render([stats]))
        assert parsed[0]["mean"] is None
