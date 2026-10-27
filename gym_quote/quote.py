"""Quote result shared by the calculation and the command line."""


class QuoteResult:
    """Monthly total of a quote, or -1 when the selection is invalid or cancelled."""

    INVALID = -1

    def __init__(self, total=INVALID):
        self.total = total

    def is_valid(self):
        """Return True when the quote produced a real total."""
        return self.total != self.INVALID

    def __repr__(self):
        return f"QuoteResult(total={self.total})"
