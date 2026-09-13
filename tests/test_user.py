import pytest

from models.user import User


def test_user_stores_user_information():
    user = User(
        user_id="USR001",
        username="terence",
        password_hash="hashed_password",
        role="Customer"
    )

    assert user.id == "USR001"
    assert user.username == "terence"
    assert user.password_hash == "hashed_password"
    assert user.role == "Customer"


def test_user_to_dict():
    user = User(
        user_id="USR001",
        username="terence",
        password_hash="hashed_password",
        role="Customer"
    )

    data = user.to_dict()

    assert data == {
        "id": "USR001",
        "username": "terence",
        "password_hash": "hashed_password",
        "role": "Customer"
    }


def test_user_from_dict():
    data = {
        "id": "USR001",
        "username": "terence",
        "password_hash": "hashed_password",
        "role": "Customer"
    }

    user = User.from_dict(data)

    assert user.id == "USR001"
    assert user.username == "terence"
    assert user.password_hash == "hashed_password"
    assert user.role == "Customer"


def test_user_rejects_invalid_role():
    with pytest.raises(ValueError):
        User(
            user_id="USR001",
            username="terence",
            password_hash="hashed_password",
            role="Manager"
        )


def test_user_accepts_valid_roles():
    valid_roles = [
        "Customer",
        "Rental Staff",
        "Administrator",
        "Maintenance"
    ]

    for role in valid_roles:
        user = User(
            user_id="USR001",
            username="terence",
            password_hash="hashed_password",
            role=role
        )

        assert user.role == role
