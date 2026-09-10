import pytest

from car_rental.services.auth_service import (
    register_user,
    login_user,
    logout_user,
    find_user,
)


def test_register_user():
    users = []

    user = register_user(
        users,
        "brian",
        "brian@example.com",
        "password123",
        "customer",
    )

    assert user["username"] == "brian"
    assert user["email"] == "brian@example.com"
    assert user["role"] == "customer"
    assert len(users) == 1


def test_register_duplicate_username():
    users = []

    register_user(
        users,
        "brian",
        "brian@example.com",
        "password123",
        "customer",
    )

    with pytest.raises(ValueError):
        register_user(
            users,
            "brian",
            "another@example.com",
            "password456",
            "customer",
        )


def test_register_duplicate_email():
    users = []

    register_user(
        users,
        "brian",
        "brian@example.com",
        "password123",
        "customer",
    )

    with pytest.raises(ValueError):
        register_user(
            users,
            "john",
            "brian@example.com",
            "password456",
            "customer",
        )


def test_find_user():
    users = [
        {
            "id": 1,
            "username": "brian",
            "email": "brian@example.com",
            "password": "password123",
            "role": "customer",
        }
    ]

    user = find_user(users, "brian")

    assert user is not None
    assert user["username"] == "brian"


def test_find_nonexistent_user():
    users = []

    user = find_user(users, "unknown")

    assert user is None


def test_login_success():
    users = [
        {
            "id": 1,
            "username": "brian",
            "email": "brian@example.com",
            "password": "password123",
            "role": "customer",
        }
    ]

    user = login_user(users, "brian", "password123")

    assert user is not None
    assert user["username"] == "brian"


def test_login_wrong_password():
    users = [
        {
            "id": 1,
            "username": "brian",
            "email": "brian@example.com",
            "password": "password123",
            "role": "customer",
        }
    ]

    with pytest.raises(ValueError):
        login_user(users, "brian", "wrongpassword")


def test_login_nonexistent_user():
    users = []

    with pytest.raises(ValueError):
        login_user(users, "unknown", "password123")


def test_logout():
    user = {
        "id": 1,
        "username": "brian",
        "email": "brian@example.com",
        "role": "customer",
    }

    result = logout_user(user)

    assert result is None
    