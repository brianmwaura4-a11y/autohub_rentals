from app.cars import add_car, get_car, get_available_cars


def test_add_car():
    car = add_car(
        "Toyota",
        "Corolla",
        2022,
        3500
    )

    assert car["make"] == "Toyota"
    assert car["model"] == "Corolla"
    assert car["year"] == 2022
    assert car["price_per_day"] == 3500


def test_get_car():
    add_car("Toyota", "Corolla", 2022, 3500)

    car = get_car(1)

    assert car is not None
    assert car["model"] == "Corolla"


def test_get_nonexistent_car():
    car = get_car(999)

    assert car is None


def test_get_available_cars():
    add_car("Toyota", "Corolla", 2022, 3500)
    add_car("Honda", "Civic", 2023, 4000)

    cars = get_available_cars()

    assert len(cars) == 2
