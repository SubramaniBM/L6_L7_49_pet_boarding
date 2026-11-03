import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# ---------- boarding_fee ----------

def test_unknown_pet_type_raises():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("hamster", 3, False)


def test_negative_days_raises():
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("cat", -1, False)


def test_within_included_days():
    assert boarding_fee("dog", 1, False) == 0


def test_premium_dog_gets_extra_included_day():
    # included 2 + 1 premium = 3, extra 2 at dog rate 30
    assert boarding_fee("dog", 5, True) == 60


def test_cat_long_stay_surcharge():
    # included 3, extra 17 at (20 + 10)
    assert boarding_fee("cat", 20, False) == 510


def test_dog_long_stay_surcharge():
    # included 2, extra 13 at (30 + 10 + 5)
    assert boarding_fee("dog", 15, False) == 585


# ---------- admission_ok ----------

def test_admission_senior():
    assert admission_ok(10, 3, True) is True


def test_admission_too_young():
    assert admission_ok(0.5, 2, False) is False


def test_admission_ok():
    assert admission_ok(4, 2, False) is True


# ---------- checkout_status ----------

def test_checkout_open_long_stay_weekend():
    # cutoff 30 + 20 = 50
    assert checkout_status(60, True, True) == "open"


def test_checkout_late():
    # cutoff 15, late window starts at 0
    assert checkout_status(10, False, False) == "late"


def test_checkout_closed():
    assert checkout_status(-1, False, False) == "closed"
