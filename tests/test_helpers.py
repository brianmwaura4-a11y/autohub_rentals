from car_rental.utils.helpers import (
    print_header,
    print_success,
    print_error,
    print_message,
    confirm_action
)


def test_print_header(capsys):
    print_header("AutoHub")

    captured = capsys.readouterr()

    assert "AutoHub" in captured.out
    assert "=" * 50 in captured.out


def test_print_success(capsys):
    print_success("Car added successfully.")

    captured = capsys.readouterr()

    assert "Success: Car added successfully." in captured.out


def test_print_error(capsys):
    print_error("Something went wrong.")

    captured = capsys.readouterr()

    assert "Error: Something went wrong." in captured.out


def test_print_message(capsys):
    print_message("Welcome to AutoHub.")

    captured = capsys.readouterr()

    assert "Welcome to AutoHub." in captured.out


def test_confirm_action_yes(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda message: "y"
    )

    result = confirm_action("Continue?")

    assert result is True


def test_confirm_action_yes_full_word(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda message: "yes"
    )

    result = confirm_action("Continue?")

    assert result is True


def test_confirm_action_no(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda message: "n"
    )

    result = confirm_action("Continue?")

    assert result is False


def test_confirm_action_invalid_answer(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda message: "maybe"
    )

    result = confirm_action("Continue?")

    assert result is False
