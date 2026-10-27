
"""Command-line interface for gym membership quotes."""

from gym_quote.calculator import calculate_quote
from gym_quote.quote import QuoteResult


def run_cli():
    """Request input, display the quote, and ask for confirmation."""
    print("=== GYM MEMBERSHIP QUOTE ===")
    print("Available plans: BASIC, STANDARD, PREMIUM")
    print("Available extras: GROUP_CLASSES, PERSONAL_TRAINING,")
    print("                  SPA, SPECIALIZED_PROGRAM")

    plan = input("Select a plan: ").strip().upper()

    extras_text = input(
        "Select extras separated by commas (or press Enter): "
    ).strip()

    extras = [
        item.strip().upper()
        for item in extras_text.split(",")
        if item.strip()
    ]

    try:
        members = int(input("Number of members: ").strip())
    except ValueError:
        print("Error: enter a valid integer for members.")
        return QuoteResult()

    result = calculate_quote(plan, extras, members)

    if not result.is_valid():
        print("Error: invalid plan, extras, or member count.")
        return result

    breakdown = result.breakdown

    print("\n=== QUOTE BREAKDOWN ===")
    print(f"Plan for all members: ${breakdown['plan']:.2f}")
    print(f"Extras for all members: ${breakdown['extras']:.2f}")
    print(f"Subtotal: ${breakdown['subtotal']:.2f}")
    print(f"Group discount: -${breakdown['group_discount']:.2f}")
    print(
        "After group discount: "
        f"${breakdown['after_group_discount']:.2f}"
    )
    print(
        "Special offer discount: "
        f"-${breakdown['special_offer_discount']:.2f}"
    )
    print(
        "After special offer: "
        f"${breakdown['after_special_offer']:.2f}"
    )
    print(
        "Premium surcharge: "
        f"+${breakdown['premium_surcharge']:.2f}"
    )
    print(
        "Before rounding: "
        f"${breakdown['before_rounding']:.2f}"
    )
    print(f"Final total: ${result.total:.2f}")

    confirmation = input(
        "\nDo you confirm this quote? (y/n): "
    ).strip().lower()

    if confirmation not in {"y", "yes", "s", "si", "sí"}:
        print("Quote cancelled.")
        return QuoteResult()

    print(f"Quote confirmed. Total: ${result.total:.2f}")
    return result
