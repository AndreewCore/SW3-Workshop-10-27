"""Tests for the quote result."""

from gym_quote.quote import QuoteResult


def test_default_result_is_invalid():
    """A quote without a total is invalid and reports -1."""
    result = QuoteResult()
    assert result.total == -1
    assert not result.is_valid()


def test_result_with_total_is_valid():
    """A quote with a positive total is valid."""
    assert QuoteResult(30).is_valid()
