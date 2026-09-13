import pytest

from car_rental.utils.validation import (
    validate_username,
    validate_password,
    validate_role,
    validate_car_data,
    validate_dates,
    validate_positive_number
)


def test_valid_username():
    assert validate_username("brian") is True


def test_empty_username():
    with pytest.raises(ValueError):
        validate_username("")


def test_short_username():
    with pytest.raises(ValueError):
        validate_username("ab")


def test_valid_password():
    assert validate_password("password123") is True


def test_short_password():
    with pytest.raises(ValueError):
        validate_password("123")


def test_valid_role():
    assert validate_role("Customer") is True


def test_invalid_role():
    with pytest.raises(ValueError):
        validate_role("Manager")


def test_valid_car_data():
    assert validate_car_data(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    ) is True


def test_empty_car_make():
    with pytest.raises(ValueError):
        validate_car_data(
            "",
            "Harrier",
            2022,
            "KDA 123A",
            5000
        )


def test_invalid_car_year():
    with pytest.raises(ValueError):
        validate_car_data(
            "Toyota",
            "Harrier",
            1800,
            "KDA 123A",
            5000
        )


def test_invalid_daily_rate():
    with pytest.raises(ValueError):
        validate_car_data(
            "Toyota",
            "Harrier",
            2022,
            "KDA 123A",
            0
        )


def test_valid_dates():
    assert validate_dates(
        "2026-09-10",
        "2026-09-13"
    ) is True


def test_invalid_date_order():
    with pytest.raises(ValueError):
        validate_dates(
            "2026-09-13",
            "2026-09-10"
        )


def test_invalid_date_format():
    with pytest.raises(ValueError):
        validate_dates(
            "10-09-2026",
            "13-09-2026"
        )


def test_valid_positive_number():
    assert validate_positive_number(5000, "Daily rate") is True


def test_invalid_positive_number():
    with pytest.raises(ValueError):
        validate_positive_number(0, "Daily rate")
