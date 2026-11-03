import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# ---------- boarding_fee ----------

def test_unknown_pet_type_raises():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("hamster", 3, False)


def test_negative_days_raises():
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("cat", -1, False)


def test_zero_days_is_valid():
    # days < 0 False at the boundary
    assert boarding_fee("cat", 0, False) == 0


@pytest.mark.parametrize("pet_type, days, is_premium, expected", [
    ("dog", 2, False, 0),      # extra == 0 (boundary)
    ("dog", 3, True, 0),       # premium adds a day, extra == 0
    ("rabbit", 4, True, 0),    # rabbit gets no premium bonus
])
def test_within_included_days(pet_type, days, is_premium, expected):
    assert boarding_fee(pet_type, days, is_premium) == expected


def test_premium_dog_gets_extra_included_day():
    # is_premium True and not rabbit: included 2 + 1 = 3, extra 2 at 30
    assert boarding_fee("dog", 5, True) == 60


def test_premium_cat_gets_extra_included_day():
    # included 3 + 1 = 4, extra 1 at 20
    assert boarding_fee("cat", 5, True) == 20


def test_premium_rabbit_no_bonus():
    # is_premium True but rabbit: included stays 4, extra 1 at 20
    assert boarding_fee("rabbit", 5, True) == 20


def test_non_premium_dog_short_stay():
    # is_premium False, dog rate, extra <= 10
    assert boarding_fee("dog", 4, False) == 60


def test_non_premium_cat_short_stay():
    # non-dog rate, extra <= 10
    assert boarding_fee("cat", 6, False) == 60


def test_extra_exactly_ten_no_surcharge():
    # extra == 10 (boundary): extra > 10 False
    assert boarding_fee("cat", 13, False) == 200


def test_cat_long_stay_surcharge():
    # extra > 10, not dog: rate 20 + 10
    assert boarding_fee("cat", 14, False) == 11 * 30


def test_rabbit_long_stay_surcharge():
    assert boarding_fee("rabbit", 20, False) == 16 * 30


def test_dog_long_stay_surcharge():
    # extra > 10, dog: rate 30 + 10 + 5
    assert boarding_fee("dog", 13, False) == 11 * 45


# ---------- admission_ok ----------

@pytest.mark.parametrize("age, vaccinations, is_senior, expected", [
    (10, 3, True, True),     # senior, enough vaccinations
    (10, 2, True, False),    # senior, not enough vaccinations
    (0.5, 5, False, False),  # too young
    (1, 2, False, True),     # age == 1 (boundary), enough vaccinations
    (4, 1, False, False),    # adult, not enough vaccinations
])
def test_admission_ok(age, vaccinations, is_senior, expected):
    assert admission_ok(age, vaccinations, is_senior) is expected


# ---------- checkout_status ----------

@pytest.mark.parametrize("minutes_left, is_long_stay, is_weekend, expected", [
    # short stay, weekday: cutoff 15
    (15, False, False, "open"),
    (14, False, False, "late"),
    (0, False, False, "late"),
    (-1, False, False, "closed"),
    # long stay, weekday: cutoff 30
    (30, True, False, "open"),
    (15, True, False, "late"),
    (14, True, False, "closed"),
    # short stay, weekend: cutoff 35
    (35, False, True, "open"),
    (20, False, True, "late"),
    (19, False, True, "closed"),
    # long stay, weekend: cutoff 50
    (50, True, True, "open"),
    (35, True, True, "late"),
    (34, True, True, "closed"),
])
def test_checkout_status(minutes_left, is_long_stay, is_weekend, expected):
    assert checkout_status(minutes_left, is_long_stay, is_weekend) == expected
