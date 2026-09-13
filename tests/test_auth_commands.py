import pytest

from car_rental.cli.auth_commands import (
    register_command,
    login_command
)


@pytest.fixture(autouse=True)
def clean_users_file(monkeypatch):
    """Keep authentication command tests isolated from users.json."""

    from car_rental.services import auth_service
    from car_rental.models import User

    test_users = []

    def fake_read_json(filename):
        return [
            user.to_dict()
            for user in test_users
        ]

    def fake_append_json(filename, item):
        test_users.append(
            User.from_dict(item)
        )

    def fake_update_json(filename, item_id, updated_item):
        for index, user in enumerate(test_users):
            if user.id == item_id:
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


def test_register_command_success(capsys):
    user = register_command(
        "command_test_user",
        "password123",
        "Customer"
    )

    captured = capsys.readouterr()

    assert user is not None
    assert user.username == "command_test_user"
    assert user.role == "Customer"

    assert "Registration successful!" in captured.out
    assert "Username: command_test_user" in captured.out
    assert "Role: Customer" in captured.out


def test_register_command_failure(capsys):
    register_command(
        "ab",
        "password123",
        "Customer"
    )

    captured = capsys.readouterr()

    assert "Error:" in captured.out
    assert (
        "Username must be at least 3 characters long."
        in captured.out
    )


def test_login_command_success(capsys):
    register_command(
        "login_command_user",
        "password123",
        "Customer"
    )

    user = login_command(
        "login_command_user",
        "password123"
    )

    captured = capsys.readouterr()

    assert user is not None
    assert user.username == "login_command_user"
    assert user.role == "Customer"

    assert "Login successful!" in captured.out
    assert "Welcome, login_command_user!" in captured.out
    assert "Role: Customer" in captured.out


def test_login_command_wrong_password(capsys):
    register_command(
        "wrong_password_user",
        "password123",
        "Customer"
    )

    user = login_command(
        "wrong_password_user",
        "wrongpassword"
    )

    captured = capsys.readouterr()

    assert user is None
    assert "Error:" in captured.out
    assert "Invalid username or password." in captured.out


def test_login_command_unknown_user(capsys):
    user = login_command(
        "unknown_command_user",
        "password123"
    )

    captured = capsys.readouterr()

    assert user is None
    assert "Error:" in captured.out
    assert "Invalid username or password." in captured.out
