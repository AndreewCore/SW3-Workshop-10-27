
"""Tests for the command-line interface."""

from gym_quote.cli import run_cli


def test_cli_displays_quote_and_accepts_confirmation(monkeypatch, capsys):
    """A valid quote is displayed and can be confirmed."""
    answers = iter([
        "PREMIUM",
        "GROUP_CLASSES, SPA",
        "2",
        "y",
    ])
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt="": next(answers),
    )

    result = run_cli()
    output = capsys.readouterr().out

    assert result.is_valid()
    assert result.total == 215
    assert "Subtotal: $230.00" in output
    assert "Final total: $215.00" in output
    assert "Quote confirmed" in output


def test_cli_cancellation_returns_minus_one(monkeypatch, capsys):
    """Rejecting the quote cancels the transaction."""
    answers = iter(["BASIC", "", "1", "n"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt="": next(answers),
    )

    result = run_cli()
    output = capsys.readouterr().out

    assert result.total == -1
    assert not result.is_valid()
    assert "Quote cancelled." in output


def test_cli_rejects_invalid_member_count(monkeypatch, capsys):
    """A non-integer member count is rejected."""
    answers = iter(["BASIC", "", "abc"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _prompt="": next(answers),
    )

    result = run_cli()
    output = capsys.readouterr().out

    assert result.total == -1
    assert "valid integer" in output
