
from car_rental.models import Car
from car_rental.utils.json_handler import (
    read_json,
    append_json,
    update_json,
    delete_json
)
from car_rental.utils.validation import validate_car_data


CARS_FILE = "cars.json"


def get_cars():
    """Return all cars as Car objects."""
    car_data = read_json(CARS_FILE)

    return [
        Car.from_dict(data)
        for data in car_data
    ]


def get_car_by_id(car_id):
    """Find a car by its ID."""
    cars = get_cars()

    for car in cars:
        if car.id == car_id:
            return car

    return None


def get_available_cars():
    """Return all cars that are currently available."""
    cars = get_cars()

    return [
        car for car in cars
        if car.status == "Available"
    ]


def add_car(
    make,
    model,
    year,
    registration_number,
    daily_rate
):
    """Add a new car to the system."""

    validate_car_data(
        make,
        model,
        year,
        registration_number,
        daily_rate
    )

    existing_cars = get_cars()

    for car in existing_cars:
        if car.registration_number.lower() == registration_number.lower():
            raise ValueError(
                "Registration number already exists."
            )

    if existing_cars:
        new_id = max(car.id for car in existing_cars) + 1
    else:
        new_id = 1

    car = Car(
        car_id=new_id,
        make=make,
        model=model,
        year=year,
        registration_number=registration_number,
        daily_rate=daily_rate,
        status="Available"
    )

    append_json(CARS_FILE, car.to_dict())

    return car


def update_car(
    car_id,
    make,
    model,
    year,
    registration_number,
    daily_rate,
    status
):
    """Update an existing car."""

    validate_car_data(
        make,
        model,
        year,
        registration_number,
        daily_rate
    )

    car = get_car_by_id(car_id)

    if car is None:
        raise ValueError("Car not found.")

    existing_cars = get_cars()

    for existing_car in existing_cars:
        if (
            existing_car.id != car_id
            and existing_car.registration_number.lower()
            == registration_number.lower()
        ):
            raise ValueError(
                "Registration number already exists."
            )

    if status not in Car.VALID_STATUSES:
        raise ValueError("Invalid car status.")

    updated_car = Car(
        car_id=car_id,
        make=make,
        model=model,
        year=year,
        registration_number=registration_number,
        daily_rate=daily_rate,
        status=status
    )

    success = update_json(
        CARS_FILE,
        car_id,
        updated_car.to_dict()
    )

    if not success:
        raise ValueError("Car could not be updated.")

    return updated_car


def delete_car(car_id):
    """Delete a car from the system."""

    car = get_car_by_id(car_id)

    if car is None:
        raise ValueError("Car not found.")

    if car.status == "Rented":
        raise ValueError(
            "A rented car cannot be deleted."
        )

    success = delete_json(
        CARS_FILE,
        car_id
    )

    if not success:
        raise ValueError("Car could not be deleted.")

    return True


def set_car_status(car_id, status):
    """Change the status of a car."""

    if status not in Car.VALID_STATUSES:
        raise ValueError("Invalid car status.")

    car = get_car_by_id(car_id)

    if car is None:
        raise ValueError("Car not found.")

    updated_car = Car(
        car_id=car.id,
        make=car.make,
        model=car.model,
        year=car.year,
        registration_number=car.registration_number,
        daily_rate=car.daily_rate,
        status=status
    )

    success = update_json(
        CARS_FILE,
        car_id,
        updated_car.to_dict()
    )

    if not success:
        raise ValueError(
            "Car status could not be updated."
        )

    return updated_car
