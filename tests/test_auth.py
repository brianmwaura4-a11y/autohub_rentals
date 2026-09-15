import pytest

from car_rental.services.auth_service import (
    register_user,
    login_user,
    logout_user,
    find_user,
)


@pytest.fixture(autouse=True)
def clean_users_file(monkeypatch):
    """Keep authentication tests isolated from users.json."""

    from car_rental.services import auth_service

    test_users = []

    def fake_read_json(filename):
        return [
            user.to_dict()
            for user in test_users
        ]

    def fake_append_json(filename, item):
        from car_rental.models import User

        test_users.append(
            User.from_dict(item)
        )

    def fake_update_json(filename, item_id, updated_item):
        for index, user in enumerate(test_users):
            if user.id == item_id:
                from car_rental.models import User

                test_users[index] = User.from_dict(
                    updated_item
                )
                return True

        return False

    def fake_delete_json(filename, item_id):
        original_length = len(test_users)

        test_users[:] = [
            user
            for user in test_users
            if user.id != item_id
        ]

        return len(test_users) < original_length

    monkeypatch.setattr(
        auth_service,
        "read_json",
        fake_read_json
    )

    monkeypatch.setattr(
        auth_service,
        "append_json",
        fake_append_json
    )

    monkeypatch.setattr(
        auth_service,
        "update_json",
        fake_update_json
    )

    monkeypatch.setattr(
        auth_service,
        "delete_json",
        fake_delete_json
    )


def test_register_user():
    user = register_user(
        "brian_test_auth",
        "password123",
        "Customer",
    )

    assert user.username == "brian_test_auth"
    assert user.role == "Customer"


def test_register_duplicate_username():
    register_user(
        "duplicate_user",
        "password123",
        "Customer",
    )

    with pytest.raises(ValueError):
        register_user(
            "duplicate_user",
            "password456",
            "Customer",
        )


def test_register_duplicate_username_case_insensitive():
    register_user(
        "CaseUser",
        "password123",
        "Customer",
    )

    with pytest.raises(ValueError):
        register_user(
            "caseuser",
            "password456",
            "Customer",
        )


def test_find_user():
    register_user(
        "find_user_test",
        "password123",
        "Customer",
    )

    user = find_user("find_user_test")

    assert user is not None
    assert user.username == "find_user_test"


def test_find_nonexistent_user():
    user = find_user("unknown_user")

    assert user is None


def test_login_success():
    register_user(
        "login_test",
        "password123",
        "Customer",
    )

    user = login_user(
        "login_test",
        "password123",
    )

    assert user is not None
    assert user.username == "login_test"


def test_login_wrong_password():
    register_user(
        "wrong_password_test",
        "password123",
        "Customer",
    )

    with pytest.raises(ValueError):
        login_user(
            "wrong_password_test",
            "wrongpassword",
        )


def test_login_nonexistent_user():
    with pytest.raises(ValueError):
        login_user(
            "unknown_login_user",
            "password123",
        )


def test_logout():
    session = {
        "user": "test_user"
    }

    result = logout_user(session)

    assert result is True
    assert "user" not in session


def test_logout_when_not_logged_in():
    session = {}

    result = logout_user(session)

    assert result is False
    assert "user" not in session
