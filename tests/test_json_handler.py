import json

from car_rental.utils.json_handler import (
    load_data,
    save_data,
)


def test_save_data(tmp_path):
    file_path = tmp_path / "cars.json"

    cars = [
        {
            "id": 1,
            "make": "Toyota",
            "model": "Corolla",
        }
    ]

    save_data(file_path, cars)

    assert file_path.exists()


def test_load_data(tmp_path):
    file_path = tmp_path / "cars.json"

    cars = [
        {
            "id": 1,
            "make": "Toyota",
            "model": "Corolla",
        }
    ]

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(cars, file)

    result = load_data(file_path)

    assert result == cars


def test_save_and_load_data(tmp_path):
    file_path = tmp_path / "cars.json"

    data = [
        {
            "id": 1,
            "make": "Toyota",
            "model": "Corolla",
            "price_per_day": 4000,
        }
    ]

    save_data(file_path, data)
    result = load_data(file_path)

    assert result == data


def test_load_missing_file(tmp_path):
    file_path = tmp_path / "missing.json"

    result = load_data(file_path)

    assert result == []
    