import pytest
from pathlib import Path

from car_rental.services.auth_service import (
    register_user,
    login_user,
    find_user_by_username,
    has_role,
    get_users
)


USERS_FILE = (
    Path(__file__).resolve().parent.parent
    / "car_rental"
    / "data"
    / "users.json"
)


@pytest.fixture(autouse=True)
def clear_users_file():
    """Start each test with an empty users file."""
    USERS_FILE.write_text("[]", encoding="utf-8")


def test_register_user():
    user = register_user(
        "brian",
        "password123"
    )

    assert user.username == "brian"
    assert user.role == "Customer"
    assert user.id == 1


def test_password_is_hashed():
    user = register_user(
        "brian",
        "password123"
    )

    assert user.password_hash != "password123"


def test_register_user_with_role():
    user = register_user(
        "staff",
        "password123",
        "Rental Staff"
    )

    assert user.role == "Rental Staff"


def test_duplicate_username():
    register_user(
        "brian",
        "password123"
    )

    with pytest.raises(ValueError, match="Username already exists."):
        register_user(
            "brian",
            "different123"
        )


def test_duplicate_username_is_case_insensitive():
    register_user(
        "brian",
        "password123"
    )

    with pytest.raises(ValueError, match="Username already exists."):
        register_user(
            "BRIAN",
            "different123"
        )


def test_login_successful():
    register_user(
        "brian",
        "password123"
    )

    user = login_user(
        "brian",
        "password123"
    )

    assert user.username == "brian"
    assert user.role == "Customer"


def test_login_is_case_insensitive():
    register_user(
        "brian",
        "password123"
    )

    user = login_user(
        "BRIAN",
        "password123"
    )

    assert user.username == "brian"


def test_login_wrong_password():
    register_user(
        "brian",
        "password123"
    )

    with pytest.raises(
        ValueError,
        match="Invalid username or password."
    ):
        login_user(
            "brian",
            "wrongpassword"
        )


def test_login_nonexistent_user():
    with pytest.raises(
        ValueError,
        match="Invalid username or password."
    ):
        login_user(
            "unknown",
            "password123"
        )


def test_find_user_by_username():
    register_user(
        "brian",
        "password123"
    )

    user = find_user_by_username("brian")

    assert user is not None
    assert user.username == "brian"


def test_find_nonexistent_user():
    user = find_user_by_username("unknown")

    assert user is None


def test_get_users():
    register_user(
        "brian",
        "password123"
    )

    register_user(
        "john",
        "password456"
    )

    users = get_users()

    assert len(users) == 2
    assert users[0].username == "brian"
    assert users[1].username == "john"


def test_has_role():
    user = register_user(
        "brian",
        "password123"
    )

    assert has_role(user, "Customer") is True
    assert has_role(user, "Administrator") is False


def test_invalid_username():
    with pytest.raises(
        ValueError,
        match="Username must be at least 3 characters long."
    ):
        register_user(
            "ab",
            "password123"
        )


def test_invalid_password():
    with pytest.raises(
        ValueError,
        match="Password must be at least 6 characters long."
    ):
        register_user(
            "brian",
            "123"
        )
