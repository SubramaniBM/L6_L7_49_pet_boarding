from hypothesis import given, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee

@given(st.text() | st.none())
def test_parse_booking_no_crash(s):

@given(st.text() | st.none())
def test_stay_average_no_crash(s):

@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
