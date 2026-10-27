"""Quote result shared by calculation and the command line."""


class QuoteResult:
    """Monthly total and breakdown of a quote, or -1 if invalid."""

    INVALID = -1

    def __init__(self, total=INVALID, breakdown=None):
        self.total = total
        self.breakdown = dict(breakdown) if breakdown else {}

    def is_valid(self):
        """Return True when the quote produced a real total."""
        return self.total != self.INVALID

    def __repr__(self):
        return f"QuoteResult(total={self.total})"
