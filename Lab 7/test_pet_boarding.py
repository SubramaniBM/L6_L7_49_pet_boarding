import math

from hypothesis import given, settings, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee

# Contract for the hardened module: each function returns None for invalid
# input and never raises. A valid result must satisfy the invariants below.

FUZZ = settings(max_examples=300, deadline=None)

# Numbers as text, including the awkward ones: nan, inf, negatives, huge values.
number_text = st.floats(allow_nan=True, allow_infinity=True).map(str)
noisy_text = st.text(max_size=20)


# ---------------------------------------------------------------- parse_booking

def _check_booking(result):
    if result is None:
        return
    pet, days = result
    assert isinstance(pet, str) and pet.strip() != ""
    assert isinstance(days, float)
    assert math.isfinite(days) and days > 0


@FUZZ
@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        result = parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"
    _check_booking(result)


@FUZZ
@given(st.text(max_size=15), number_text | noisy_text)
def test_parse_booking_structured(pet, days):
    try:
        result = parse_booking(f"{pet}:{days}")
    except Exception as e:
        assert False, f"parse_booking crashed with: {e!r}"
    _check_booking(result)


@FUZZ
@given(st.sampled_from(["dog", "cat", "golden retriever"]),
       st.floats(min_value=0.5, max_value=365))
def test_parse_booking_accepts_valid_input(pet, days):
    assert parse_booking(f" {pet} : {days} ") == (pet.title(), days)


# ----------------------------------------------------------------- stay_average

@FUZZ
@given(st.text() | st.none())
def test_stay_average_no_crash(s):
    try:
        result = stay_average(s)
    except Exception as e:
        assert False, f"stay_average crashed with: {e!r}"
    if result is not None:
        assert isinstance(result, int) and result > 0


@FUZZ
@given(st.lists(st.integers() | noisy_text, max_size=8))
def test_stay_average_structured(items):
    csv = ",".join(str(x) for x in items)
    try:
        result = stay_average(csv)
    except Exception as e:
        assert False, f"stay_average crashed with: {e!r}"
    if result is not None:
        assert isinstance(result, int) and result > 0


@FUZZ
@given(st.lists(st.integers(min_value=1, max_value=10_000), min_size=1, max_size=20))
def test_stay_average_within_bounds(days):
    result = stay_average(",".join(map(str, days)))
    assert result == sum(days) // len(days)
    assert min(days) <= result <= max(days)


# ------------------------------------------------------------------ payable_fee

def _check_fee(result):
    if result is None:
        return
    assert isinstance(result, float)
    assert math.isfinite(result) and result >= 0


@FUZZ
@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        result = payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e!r}"
    _check_fee(result)


@FUZZ
@given(number_text | noisy_text, number_text | noisy_text)
def test_payable_fee_structured(fee, discount):
    try:
        result = payable_fee(f"{fee}|{discount}")
    except Exception as e:
        assert False, f"payable_fee crashed with: {e!r}"
    _check_fee(result)


@FUZZ
@given(st.floats(min_value=0, max_value=1e6), st.floats(min_value=0, max_value=1e6))
def test_payable_fee_matches_formula(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result == round(max(fee * 1.18 - discount, 0.0), 2)
    assert result <= round(fee * 1.18, 2)
