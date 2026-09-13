from unittest.mock import Mock

from cli.auth_commands import (
    register_command,
    login_command,
    logout_command
)


def test_register_command():
    auth_service = Mock()

    fake_user = Mock()
    fake_user.username = "terence"

    auth_service.register_user.return_value = fake_user

    inputs = iter([
        "terence",
        "password123",
        "Customer"
    ])

    def fake_input(prompt):
        return next(inputs)

    result = register_command(
        auth_service,
        input_function=fake_input
    )

    auth_service.register_user.assert_called_once_with(
        username="terence",
        password="password123",
        role="Customer"
    )

    assert result == fake_user


def test_login_command():
    auth_service = Mock()

    fake_user = Mock()
    fake_user.username = "terence"

    auth_service.login.return_value = fake_user

    inputs = iter([
        "terence",
        "password123"
    ])

    def fake_input(prompt):
        return next(inputs)

    session = {}

    result = login_command(
        auth_service,
        session,
        input_function=fake_input
    )

    auth_service.login.assert_called_once_with(
        username="terence",
        password="password123"
    )

    assert result == fake_user
    assert session["user"] == fake_user


def test_logout_command():
    auth_service = Mock()

    fake_user = Mock()

    session = {
        "user": fake_user
    }

    logout_command(
        auth_service,
        session
    )

    auth_service.logout.assert_called_once_with(session)

    assert session == {}
