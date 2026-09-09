from app.cars import add_car
from app.customers import add_customer
from app.rentals import create_rental, calculate_rental_cost


def test_calculate_rental_cost():
    cost = calculate_rental_cost(3500, 3)

    assert cost == 10500


def test_create_rental():
    add_car("Toyota", "Corolla", 2022, 3500)

    add_customer(
        "Brian",
        "brian@example.com",
        "0712345678"
    )

    rental = create_rental(
        customer_id=1,
        car_id=1,
        days=3
    )

    assert rental["customer_id"] == 1
    assert rental["car_id"] == 1
    assert rental["days"] == 3
    assert rental["total_cost"] == 10500


def test_rental_makes_car_unavailable():
    add_car("Toyota", "Corolla", 2022, 3500)

    add_customer(
        "Brian",
        "brian@example.com",
        "0712345678"
    )

    create_rental(
        customer_id=1,
        car_id=1,
        days=3
    )

    from app.cars import get_available_cars

    cars = get_available_cars()

    assert len(cars) == 0
