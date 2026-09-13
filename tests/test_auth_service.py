import json
import pytest

from services.auth_service import AuthService


@pytest.fixture
def auth_service(tmp_path):
    users_file = tmp_path / "users.json"
    return AuthService(users_file)


def test_register_user(auth_service):
    user = auth_service.register_user(
        username="terence",
        password="password123",
        role="Customer"
    )

    assert user.username == "terence"
    assert user.role == "Customer"


def test_password_is_not_stored_as_plain_text(auth_service):
    user = auth_service.register_user(
        username="terence",
        password="password123",
        role="Customer"
    )

    assert user.password_hash != "password123"


def test_registered_user_is_saved_to_json(auth_service, tmp_path):
    auth_service.register_user(
        username="terence",
        password="password123",
        role="Customer"
    )

    users_file = tmp_path / "users.json"

    with open(users_file, "r") as file:
        users = json.load(file)

    assert len(users) == 1
    assert users[0]["username"] == "terence"


def test_duplicate_username_is_rejected(auth_service):
    auth_service.register_user(
        username="terence",
        password="password123",
        role="Customer"
    )

    with pytest.raises(ValueError):
        auth_service.register_user(
            username="terence",
            password="another123",
            role="Customer"
        )


def test_empty_username_is_rejected(auth_service):
    with pytest.raises(ValueError):
        auth_service.register_user(
            username="",
            password="password123",
            role="Customer"
        )


def test_short_password_is_rejected(auth_service):
    with pytest.raises(ValueError):
        auth_service.register_user(
            username="terence",
            password="123",
            role="Customer"
        )


def test_invalid_role_is_rejected(auth_service):
    with pytest.raises(ValueError):
        auth_service.register_user(
            username="terence",
            password="password123",
            role="Manager"
        )


def test_get_user_by_username(auth_service):
    auth_service.register_user(
        username="terence",
        password="password123",
        role="Customer"
    )

    user = auth_service.get_user_by_username("terence")

    assert user is not None
    assert user.username == "terence"


def test_successful_login(auth_service):
    auth_service.register_user(
        username="terence",
        password="password123",
        role="Customer"
    )

    user = auth_service.login(
        username="terence",
        password="password123"
    )

    assert user.username == "terence"
    assert user.role == "Customer"


def test_login_rejects_wrong_password(auth_service):
    auth_service.register_user(
        username="terence",
        password="password123",
        role="Customer"
    )

    with pytest.raises(ValueError):
        auth_service.login(
            username="terence",
            password="wrongpassword"
        )


def test_login_rejects_unknown_username(auth_service):
    with pytest.raises(ValueError):
        auth_service.login(
            username="unknown",
            password="password123"
        )


def test_has_role_returns_true_for_correct_role(auth_service):
    user = auth_service.register_user(
        username="terence",
        password="password123",
        role="Administrator"
    )

    assert auth_service.has_role(user, "Administrator") is True


def test_has_role_returns_false_for_wrong_role(auth_service):
    user = auth_service.register_user(
        username="terence",
        password="password123",
        role="Customer"
    )

    assert auth_service.has_role(user, "Administrator") is False


def test_logout_clears_session(auth_service):
    user = auth_service.register_user(
        username="terence",
        password="password123",
        role="Customer"
    )

    session = {"user": user}

    auth_service.logout(session)

    assert session == {}
