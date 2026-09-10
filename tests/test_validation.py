import pytest

from car_rental.utils.validation import (
    validate_email,
    validate_password,
    validate_date,
    validate_price,
)


def test_valid_email():
    assert validate_email("brian@example.com") is True


def test_invalid_email():
    assert validate_email("brian@example") is False


def test_email_without_at_symbol():
    assert validate_email("brianexample.com") is False


def test_valid_password():
    assert validate_password("password123") is True


def test_short_password():
    assert validate_password("123") is False


def test_valid_date():
    assert validate_date("2026-09-10") is True


def test_invalid_date():
    assert validate_date("10/09/2026") is False


def test_invalid_date_value():
    assert validate_date("2026-99-99") is False


def test_valid_price():
    assert validate_price(4000) is True


def test_zero_price():
    assert validate_price(0) is False


def test_negative_price():
    assert validate_price(-1000) is False


def test_non_numeric_price():
    with pytest.raises((TypeError, ValueError)):
        validate_price("four thousand")
        