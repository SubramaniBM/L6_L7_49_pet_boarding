import math

# Hardened version (Lab 7): every function validates its input and returns
# None instead of raising when the input is malformed.

GST_RATE = 1.18


def _to_number(text):
    """Convert text to a finite float, or return None."""
    try:
        value = float(text.strip())
    except (ValueError, OverflowError):
        return None
    return value if math.isfinite(value) else None


def parse_booking(text):
    """'pet:days' -> (Pet, days). Days must be a finite number above zero."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    pet = parts[0].strip()
    if not pet:
        return None
    days = _to_number(parts[1])
    if days is None or days <= 0:
        return None
    return pet.title(), days


def stay_average(days_csv):
    """'2,5,7' -> floor of the mean. Every entry must be a positive integer."""
    if not isinstance(days_csv, str):
        return None
    values = []
    for raw in days_csv.split(','):
        raw = raw.strip()
        if not raw:
            return None
        try:
            value = int(raw)
        except ValueError:          # non-numeric, or too many digits
            return None
        if value <= 0:
            return None
        values.append(value)
    return sum(values) // len(values)


def payable_fee(text):
    """'fee|discount' -> fee incl. 18% GST minus discount, never below 0."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    fee = _to_number(parts[0])
    discount = _to_number(parts[1])
    if fee is None or discount is None or fee < 0 or discount < 0:
        return None
    total = fee * GST_RATE - discount
    if not math.isfinite(total):    # e.g. fee near float max overflows
        return None
    return round(max(total, 0.0), 2)


def _show(label, result):
    if result is None:
        print(label, "Invalid input")
    else:
        print(label, result)


def main():
    try:
        print("==== Running parse_booking ====")
        user_input = input("Enter pet:days (e.g. dog:5): ")
        _show("Pet and Days:", parse_booking(user_input))

        print("\n==== Running stay_average ====")
        user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
        _show("Average Stay:", stay_average(user_input))

        print("\n==== Running payable_fee ====")
        user_input = input("Enter fee|discount (e.g. 1500|100): ")
        _show("Payable Fee:", payable_fee(user_input))
    except (EOFError, KeyboardInterrupt):
        print("\nInput closed. Exiting.")


if __name__ == "__main__":
    main()
