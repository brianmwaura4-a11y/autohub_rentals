import pytest

from car_rental.cli.auth_commands import (
    register_command,
    login_command
)
from car_rental.models import User


def test_register_command_success(capsys):
    user = register_command(
        "brian",
        "password123",
        "Customer"
    )

    captured = capsys.readouterr()

    assert user is not None
    assert user.username == "brian"
    assert user.role == "Customer"
    assert "Registration successful!" in captured.out
    assert "Username: brian" in captured.out
    assert "Role: Customer" in captured.out


def test_register_command_failure(capsys):
    register_command(
        "ab",
        "password123",
        "Customer"
    )

    captured = capsys.readouterr()

    assert "Error:" in captured.out
    assert "Username must be at least 3 characters long." in captured.out


def test_login_command_success(capsys):
    register_command(
        "brian",
        "password123",
        "Customer"
    )

    user = login_command(
        "brian",
        "password123"
    )

    captured = capsys.readouterr()

    assert user is not None
    assert user.username == "brian"
    assert user.role == "Customer"
    assert "Login successful!" in captured.out
    assert "Welcome, brian!" in captured.out
    assert "Role: Customer" in captured.out


def test_login_command_wrong_password(capsys):
    register_command(
        "brian",
        "password123",
        "Customer"
    )

    user = login_command(
        "brian",
        "wrongpassword"
    )

    captured = capsys.readouterr()

    assert user is None
    assert "Error:" in captured.out
    assert "Invalid username or password." in captured.out


def test_login_command_unknown_user(capsys):
    user = login_command(
        "unknown",
        "password123"
    )

    captured = capsys.readouterr()

    assert user is None
    assert "Error:" in captured.out
    assert "Invalid username or password." in captured.out
