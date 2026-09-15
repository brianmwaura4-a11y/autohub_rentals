
from pathlib import Path

import pytest

from car_rental.services.car_service import (
    get_cars,
    get_car_by_id,
    get_available_cars,
    add_car,
    update_car,
    delete_car,
    set_car_status
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


def test_get_cars_empty():
    cars = get_cars()

    assert cars == []


def test_add_car():
    car = add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    assert car.id == 1
    assert car.make == "Toyota"
    assert car.model == "Harrier"
    assert car.year == 2022
    assert car.registration_number == "KDA 123A"
    assert car.daily_rate == 5000
    assert car.status == "Available"


def test_get_cars():
    add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    add_car(
        "Mazda",
        "CX-5",
        2021,
        "KDB 456B",
        4500
    )

    cars = get_cars()

    assert len(cars) == 2
    assert cars[0].make == "Toyota"
    assert cars[1].make == "Mazda"


def test_get_car_by_id():
    car = add_car(
        "Toyota",
        "Corolla",
        2023,
        "KDC 789C",
        4000
    )

    found_car = get_car_by_id(car.id)

    assert found_car is not None
    assert found_car.id == car.id
    assert found_car.model == "Corolla"


def test_get_car_by_id_not_found():
    car = get_car_by_id(999)

    assert car is None


def test_get_available_cars():
    car1 = add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    car2 = add_car(
        "Mazda",
        "CX-5",
        2021,
        "KDB 456B",
        4500
    )

    set_car_status(
        car2.id,
        "Rented"
    )

    available_cars = get_available_cars()

    assert len(available_cars) == 1
    assert available_cars[0].id == car1.id


def test_add_car_duplicate_registration():
    add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    with pytest.raises(
        ValueError,
        match="Registration number already exists"
    ):
        add_car(
            "Mazda",
            "CX-5",
            2021,
            "KDA 123A",
            4500
        )


def test_add_car_duplicate_registration_case_insensitive():
    add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    with pytest.raises(
        ValueError,
        match="Registration number already exists"
    ):
        add_car(
            "Mazda",
            "CX-5",
            2021,
            "kda 123a",
            4500
        )


def test_add_car_invalid_data():
    with pytest.raises(ValueError):
        add_car(
            "",
            "Harrier",
            2022,
            "KDA 123A",
            5000
        )


def test_update_car():
    car = add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    updated_car = update_car(
        car.id,
        "Toyota",
        "RAV4",
        2023,
        "KDA 123A",
        6000,
        "Available"
    )

    assert updated_car.id == car.id
    assert updated_car.model == "RAV4"
    assert updated_car.year == 2023
    assert updated_car.daily_rate == 6000


def test_update_car_not_found():
    with pytest.raises(
        ValueError,
        match="Car not found"
    ):
        update_car(
            999,
            "Toyota",
            "Harrier",
            2022,
            "KDA 123A",
            5000,
            "Available"
        )


def test_set_car_status():
    car = add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    updated_car = set_car_status(
        car.id,
        "Rented"
    )

    assert updated_car.status == "Rented"

    found_car = get_car_by_id(car.id)

    assert found_car.status == "Rented"


def test_set_car_status_invalid():
    car = add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    with pytest.raises(
        ValueError,
        match="Invalid car status"
    ):
        set_car_status(
            car.id,
            "Broken"
        )


def test_delete_car():
    car = add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    result = delete_car(car.id)

    assert result is True
    assert get_car_by_id(car.id) is None
    assert get_cars() == []


def test_delete_car_not_found():
    with pytest.raises(
        ValueError,
        match="Car not found"
    ):
        delete_car(999)


def test_delete_rented_car():
    car = add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    set_car_status(
        car.id,
        "Rented"
    )

    with pytest.raises(
        ValueError,
        match="A rented car cannot be deleted"
    ):
        delete_car(car.id)
