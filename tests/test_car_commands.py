from pathlib import Path

import pytest

from car_rental.cli.car_commands import (
    list_cars_command,
    list_all_cars_command,
    add_car_command,
    update_car_command,
    delete_car_command
)

from car_rental.services.car_service import (
    get_car_by_id
)


CARS_FILE = (
    Path(__file__).resolve().parent.parent
    / "car_rental"
    / "data"
    / "cars.json"
)


@pytest.fixture(autouse=True)
def clear_cars_file():
    CARS_FILE.write_text("[]", encoding="utf-8")


def test_list_cars_when_empty(capsys):
    result = list_cars_command()

    captured = capsys.readouterr()

    assert result == []
    assert "No cars are currently available." in captured.out


def test_add_car_command(capsys):
    car = add_car_command(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    captured = capsys.readouterr()

    assert car is not None
    assert car.make == "Toyota"
    assert car.model == "Harrier"
    assert "Car added successfully!" in captured.out


def test_list_cars_command(capsys):
    add_car_command(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    capsys.readouterr()

    result = list_cars_command()

    captured = capsys.readouterr()

    assert len(result) == 1
    assert "Toyota Harrier" in captured.out
    assert "KDA 123A" in captured.out
    assert "KSh 5000" in captured.out


def test_list_all_cars_command(capsys):
    add_car_command(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    capsys.readouterr()

    result = list_all_cars_command()

    captured = capsys.readouterr()

    assert len(result) == 1
    assert "All Cars" in captured.out
    assert "Toyota Harrier" in captured.out
    assert "Available" in captured.out


def test_update_car_command(capsys):
    car = add_car_command(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    capsys.readouterr()

    updated_car = update_car_command(
        car.id,
        "Toyota",
        "RAV4",
        2023,
        "KDA 123A",
        6000,
        "Available"
    )

    captured = capsys.readouterr()

    assert updated_car is not None
    assert updated_car.model == "RAV4"
    assert updated_car.year == 2023
    assert updated_car.daily_rate == 6000
    assert "Car updated successfully!" in captured.out


def test_update_car_command_not_found(capsys):
    result = update_car_command(
        999,
        "Toyota",
        "RAV4",
        2023,
        "KDA 123A",
        6000,
        "Available"
    )

    captured = capsys.readouterr()

    assert result is None
    assert "Car not found." in captured.out


def test_add_car_command_invalid_data(capsys):
    result = add_car_command(
        "",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    captured = capsys.readouterr()

    assert result is None
    assert "Error:" in captured.out


def test_add_car_command_duplicate_registration(capsys):
    add_car_command(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    capsys.readouterr()

    result = add_car_command(
        "Mazda",
        "CX-5",
        2021,
        "KDA 123A",
        4500
    )

    captured = capsys.readouterr()

    assert result is None
    assert "Registration number already exists." in captured.out


def test_delete_car_command(capsys):
    car = add_car_command(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    capsys.readouterr()

    result = delete_car_command(car.id)

    captured = capsys.readouterr()

    assert result is True
    assert "Car deleted successfully." in captured.out
    assert get_car_by_id(car.id) is None


def test_delete_car_command_not_found(capsys):
    result = delete_car_command(999)

    captured = capsys.readouterr()

    assert result is False
    assert "Car not found." in captured.out
