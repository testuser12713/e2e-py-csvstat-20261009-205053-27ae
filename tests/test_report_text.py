"""Tests for :func:`csvstat.report_text.render`."""

from csvstat.models import ColumnStats
from csvstat.report_text import render


def _numeric(name: str, mean: float) -> ColumnStats:
    return ColumnStats(
        name=name,
        kind="numeric",
        count=3,
        minimum=1,
        maximum=9,
        mean=mean,
        missing=0,
        unique=None,
    )


def test_column_order_is_preserved() -> None:
    text = render([_numeric("first", 2.0), _numeric("second", 3.0)])

    assert text.index("Spalte: first") < text.index("Spalte: second")


def test_numeric_block_contains_all_labels() -> None:
    text = render([_numeric("age", 2.0)])

    assert "Spalte: age" in text
    assert "Anzahl: 3" in text
    assert "Minimum: 1" in text
    assert "Maximum: 9" in text
    assert "Mittelwert: 2.0000" in text
    assert "Fehlende Werte: 0" in text


def test_text_block_shows_unique_values_and_no_numeric_stats() -> None:
    result = ColumnStats(
        name="name",
        kind="text",
        count=3,
        minimum=None,
        maximum=None,
        mean=None,
        missing=1,
        unique=2,
    )

    text = render([result])

    assert "Spalte: name" in text
    assert "Anzahl: 3" in text
    assert "Fehlende Werte: 1" in text
    assert "Eindeutige Werte: 2" in text
    assert "Minimum" not in text
    assert "Mittelwert" not in text


def test_all_missing_numeric_column() -> None:
    result = ColumnStats(
        name="v",
        kind="numeric",
        count=0,
        minimum=None,
        maximum=None,
        mean=None,
        missing=2,
        unique=None,
    )

    text = render([result])

    assert "Anzahl: 0" in text
    assert "Fehlende Werte: 2" in text
    assert "Minimum" not in text
    assert "Maximum" not in text
    assert "Mittelwert" not in text


def test_mean_is_rounded_to_four_decimals() -> None:
    text = render([_numeric("v", 1.6667)])

    assert "Mittelwert: 1.6667" in text
