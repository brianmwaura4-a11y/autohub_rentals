import pytest

from car_rental.services.car_service import (
    get_all_cars,
    get_car_by_id,
    add_car,
    update_car,
    delete_car,
    check_availability,
)


def sample_cars():
    return [
        {
            "id": 1,
            "make": "Toyota",
            "model": "Corolla",
            "year": 2022,
            "registration": "KDA123A",
            "category": "Sedan",
            "price_per_day": 4000,
            "available": True,
        },
        {
            "id": 2,
            "make": "Nissan",
            "model": "X-Trail",
            "year": 2021,
            "registration": "KDB456B",
            "category": "SUV",
            "price_per_day": 5000,
            "available": False,
        },
    ]


def test_get_all_cars():
    cars = sample_cars()

    result = get_all_cars(cars)

    assert len(result) == 2


def test_get_car_by_id():
    cars = sample_cars()

    car = get_car_by_id(cars, 1)

    assert car is not None
    assert car["make"] == "Toyota"
    assert car["model"] == "Corolla"


def test_get_nonexistent_car():
    cars = sample_cars()

    car = get_car_by_id(cars, 99)

    assert car is None


def test_add_car():
    cars = []

    car = add_car(
        cars,
        "Toyota",
        "Corolla",
        2022,
        "KDA123A",
        "Sedan",
        4000,
    )

    assert len(cars) == 1
    assert car["make"] == "Toyota"
    assert car["model"] == "Corolla"
    assert car["available"] is True


def test_add_duplicate_registration():
    cars = sample_cars()

    with pytest.raises(ValueError):
        add_car(
            cars,
            "Honda",
            "Civic",
            2023,
            "KDA123A",
            "Sedan",
            4500,
        )


def test_update_car():
    cars = sample_cars()

    updated_car = update_car(
        cars,
        1,
        price_per_day=4500,
    )

    assert updated_car["price_per_day"] == 4500


def test_update_car_availability():
    cars = sample_cars()

    updated_car = update_car(
        cars,
        1,
        available=False,
    )

    assert updated_car["available"] is False


def test_update_nonexistent_car():
    cars = sample_cars()

    with pytest.raises(ValueError):
        update_car(
            cars,
            99,
            price_per_day=5000,
        )


def test_delete_car():
    cars = sample_cars()

    result = delete_car(cars, 1)

    assert result is True
    assert len(cars) == 1
    assert cars[0]["id"] == 2


def test_delete_nonexistent_car():
    cars = sample_cars()

    with pytest.raises(ValueError):
        delete_car(cars, 99)


def test_check_available_car():
    cars = sample_cars()

    result = check_availability(cars, 1)

    assert result is True


def test_check_unavailable_car():
    cars = sample_cars()

    result = check_availability(cars, 2)

    assert result is False
    