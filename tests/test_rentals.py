import pytest

from car_rental.services.auth_service import register_user
from car_rental.services.car_service import add_car
from car_rental.services.rental_service import (
    create_rental,
    get_rentals,
    get_rental_by_id,
    get_user_rentals,
    get_active_rentals,
    return_car,
    cancel_rental
)


@pytest.fixture(autouse=True)
def clear_data():
    with open(
        "car_rental/data/users.json",
        "w",
        encoding="utf-8"
    ) as file:
        file.write("[]")

    with open(
        "car_rental/data/cars.json",
        "w",
        encoding="utf-8"
    ) as file:
        file.write("[]")

    with open(
        "car_rental/data/rentals.json",
        "w",
        encoding="utf-8"
    ) as file:
        file.write("[]")


def create_test_user_and_car():
    user = register_user(
        "brian",
        "password123"
    )

    car = add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    return user, car


def test_create_rental():
    user, car = create_test_user_and_car()

    rental = create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    assert rental.id == 1
    assert rental.user_id == user.id
    assert rental.car_id == car.id
    assert rental.status == "Active"


def test_rental_cost():
    user, car = create_test_user_and_car()

    rental = create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    assert rental.total_cost == 15000


def test_rental_is_saved():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    rentals = get_rentals()

    assert len(rentals) == 1
    assert rentals[0].id == 1


def test_get_rental_by_id():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    rental = get_rental_by_id(1)

    assert rental is not None
    assert rental.id == 1


def test_get_nonexistent_rental():
    rental = get_rental_by_id(999)

    assert rental is None
    
def test_get_user_rentals():
    user = register_user(
        "brian",
        "password123"
    )

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

    rental1 = create_rental(
        user.id,
        car1.id,
        "2026-09-10",
        "2026-09-13"
    )

    return_car(rental1.id)

    rental2 = create_rental(
        user.id,
        car2.id,
        "2026-09-15",
        "2026-09-18"
    )

    rentals = get_user_rentals(user.id)

    assert len(rentals) == 2
    assert rentals[0].id == rental1.id
    assert rentals[1].id == rental2.id


def test_active_rentals():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    active_rentals = get_active_rentals()

    assert len(active_rentals) == 1
    assert active_rentals[0].status == "Active"


def test_car_becomes_rented():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    from car_rental.services.car_service import get_car_by_id

    updated_car = get_car_by_id(car.id)

    assert updated_car.status == "Rented"


def test_cannot_rent_unavailable_car():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    with pytest.raises(
        ValueError,
        match="Car is not available for rental"
    ):
        create_rental(
            user.id,
            car.id,
            "2026-09-15",
            "2026-09-18"
        )


def test_user_must_exist():
    add_car(
        "Toyota",
        "Harrier",
        2022,
        "KDA 123A",
        5000
    )

    with pytest.raises(
        ValueError,
        match="User not found"
    ):
        create_rental(
            999,
            1,
            "2026-09-10",
            "2026-09-13"
        )


def test_car_must_exist():
    user = register_user(
        "brian",
        "password123"
    )

    with pytest.raises(
        ValueError,
        match="Car not found"
    ):
        create_rental(
            user.id,
            999,
            "2026-09-10",
            "2026-09-13"
        )


def test_invalid_dates():
    user, car = create_test_user_and_car()

    with pytest.raises(ValueError):
        create_rental(
            user.id,
            car.id,
            "2026-09-20",
            "2026-09-10"
        )


def test_same_start_and_end_date():
    user, car = create_test_user_and_car()

    with pytest.raises(
        ValueError,
        match="Rental must be at least one day"
    ):
        create_rental(
            user.id,
            car.id,
            "2026-09-10",
            "2026-09-10"
        )


def test_return_car():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    rental = return_car(1)

    assert rental.status == "Completed"


def test_car_becomes_available_after_return():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    return_car(1)

    from car_rental.services.car_service import get_car_by_id

    updated_car = get_car_by_id(car.id)

    assert updated_car.status == "Available"


def test_cannot_return_completed_rental():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    return_car(1)

    with pytest.raises(
        ValueError,
        match="Rental is not active"
    ):
        return_car(1)


def test_cancel_rental():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    rental = cancel_rental(1)

    assert rental.status == "Cancelled"


def test_car_becomes_available_after_cancellation():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    cancel_rental(1)

    from car_rental.services.car_service import get_car_by_id

    updated_car = get_car_by_id(car.id)

    assert updated_car.status == "Available"


def test_cannot_cancel_completed_rental():
    user, car = create_test_user_and_car()

    create_rental(
        user.id,
        car.id,
        "2026-09-10",
        "2026-09-13"
    )

    return_car(1)

    with pytest.raises(
        ValueError,
        match="Rental is not active"
    ):
        cancel_rental(1)
        