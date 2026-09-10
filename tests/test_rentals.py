import pytest

from car_rental.services.rental_service import (
    calculate_rental_cost,
    create_rental,
    get_rental_by_id,
    get_user_rentals,
    cancel_rental,
    complete_rental,
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


def sample_rentals():
    return []


def test_calculate_rental_cost():
    result = calculate_rental_cost(4000, 3)

    assert result == 12000


def test_calculate_rental_cost_one_day():
    result = calculate_rental_cost(4000, 1)

    assert result == 4000


def test_calculate_rental_cost_invalid_days():
    with pytest.raises(ValueError):
        calculate_rental_cost(4000, 0)


def test_create_rental():
    cars = sample_cars()
    rentals = []

    rental = create_rental(
        rentals,
        cars,
        user_id=1,
        car_id=1,
        pickup_date="2026-09-10",
        return_date="2026-09-13",
    )

    assert rental["user_id"] == 1
    assert rental["car_id"] == 1
    assert rental["total_cost"] == 12000
    assert rental["status"] == "active"


def test_create_rental_makes_car_unavailable():
    cars = sample_cars()
    rentals = []

    create_rental(
        rentals,
        cars,
        user_id=1,
        car_id=1,
        pickup_date="2026-09-10",
        return_date="2026-09-13",
    )

    assert cars[0]["available"] is False


def test_cannot_rent_unavailable_car():
    cars = sample_cars()
    rentals = []

    with pytest.raises(ValueError):
        create_rental(
            rentals,
            cars,
            user_id=1,
            car_id=2,
            pickup_date="2026-09-10",
            return_date="2026-09-13",
        )


def test_get_rental_by_id():
    rentals = [
        {
            "id": 1,
            "user_id": 1,
            "car_id": 1,
            "pickup_date": "2026-09-10",
            "return_date": "2026-09-13",
            "total_cost": 12000,
            "status": "active",
        }
    ]

    rental = get_rental_by_id(rentals, 1)

    assert rental is not None
    assert rental["total_cost"] == 12000


def test_get_nonexistent_rental():
    rentals = []

    rental = get_rental_by_id(rentals, 99)

    assert rental is None


def test_get_user_rentals():
    rentals = [
        {
            "id": 1,
            "user_id": 1,
            "car_id": 1,
            "total_cost": 12000,
            "status": "active",
        },
        {
            "id": 2,
            "user_id": 2,
            "car_id": 2,
            "total_cost": 15000,
            "status": "active",
        },
    ]

    result = get_user_rentals(rentals, 1)

    assert len(result) == 1
    assert result[0]["user_id"] == 1


def test_cancel_rental():
    cars = sample_cars()

    rentals = [
        {
            "id": 1,
            "user_id": 1,
            "car_id": 1,
            "pickup_date": "2026-09-20",
            "return_date": "2026-09-23",
            "total_cost": 12000,
            "status": "active",
        }
    ]

    cars[0]["available"] = False

    result = cancel_rental(
        rentals,
        cars,
        rental_id=1,
        user_id=1,
    )

    assert result["status"] == "cancelled"
    assert cars[0]["available"] is True


def test_cannot_cancel_another_users_rental():
    cars = sample_cars()

    rentals = [
        {
            "id": 1,
            "user_id": 1,
            "car_id": 1,
            "pickup_date": "2026-09-20",
            "return_date": "2026-09-23",
            "total_cost": 12000,
            "status": "active",
        }
    ]

    with pytest.raises(PermissionError):
        cancel_rental(
            rentals,
            cars,
            rental_id=1,
            user_id=2,
        )


def test_complete_rental():
    cars = sample_cars()

    rentals = [
        {
            "id": 1,
            "user_id": 1,
            "car_id": 1,
            "pickup_date": "2026-09-10",
            "return_date": "2026-09-13",
            "total_cost": 12000,
            "status": "active",
        }
    ]

    cars[0]["available"] = False

    result = complete_rental(
        rentals,
        cars,
        rental_id=1,
    )

    assert result["status"] == "completed"
    assert cars[0]["available"] is True


def test_cannot_complete_nonexistent_rental():
    cars = sample_cars()
    rentals = []

    with pytest.raises(ValueError):
        complete_rental(
            rentals,
            cars,
            rental_id=99,
        )
        