from datetime import datetime

from car_rental.models import Rental
from car_rental.services.auth_service import get_users
from car_rental.services.car_service import (
    get_car_by_id,
    set_car_status
)
from car_rental.utils.json_handler import (
    read_json,
    append_json,
    update_json
)
from car_rental.utils.validation import validate_dates


RENTALS_FILE = "rentals.json"


def get_rentals():
    """Return all rentals as Rental objects."""
    rental_data = read_json(RENTALS_FILE)

    return [
        Rental.from_dict(data)
        for data in rental_data
    ]


def get_rental_by_id(rental_id):
    """Find a rental by its ID."""
    rentals = get_rentals()

    for rental in rentals:
        if rental.id == rental_id:
            return rental

    return None


def get_active_rentals():
    """Return all active rentals."""
    rentals = get_rentals()

    return [
        rental for rental in rentals
        if rental.status == "Active"
    ]


def create_rental(
    user_id,
    car_id,
    start_date,
    end_date
):
    """Create a new car rental."""

    validate_dates(start_date, end_date)

    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )

    days = (end - start).days

    if days <= 0:
        raise ValueError(
            "Rental must be at least one day."
        )

    users = get_users()

    user = None

    for existing_user in users:
        if existing_user.id == user_id:
            user = existing_user
            break

    if user is None:
        raise ValueError("User not found.")

    car = get_car_by_id(car_id)

    if car is None:
        raise ValueError("Car not found.")

    if car.status != "Available":
        raise ValueError(
            "Car is not available for rental."
        )

    rentals = get_rentals()

    if rentals:
        new_id = max(rental.id for rental in rentals) + 1
    else:
        new_id = 1

    total_cost = car.daily_rate * days

    rental = Rental(
        rental_id=new_id,
        user_id=user_id,
        car_id=car_id,
        start_date=start_date,
        end_date=end_date,
        total_cost=total_cost,
        status="Active"
    )

    append_json(
        RENTALS_FILE,
        rental.to_dict()
    )

    set_car_status(
        car_id,
        "Rented"
    )

    return rental


def return_car(rental_id):
    """Return a rented car and complete the rental."""

    rental = get_rental_by_id(rental_id)

    if rental is None:
        raise ValueError("Rental not found.")

    if rental.status != "Active":
        raise ValueError(
            "Rental is not active."
        )

    updated_rental = Rental(
        rental_id=rental.id,
        user_id=rental.user_id,
        car_id=rental.car_id,
        start_date=rental.start_date,
        end_date=rental.end_date,
        total_cost=rental.total_cost,
        status="Completed"
    )

    success = update_json(
        RENTALS_FILE,
        rental_id,
        updated_rental.to_dict()
    )

    if not success:
        raise ValueError(
            "Rental could not be updated."
        )

    set_car_status(
        rental.car_id,
        "Available"
    )

    return updated_rental


def cancel_rental(rental_id):
    """Cancel an active rental."""

    rental = get_rental_by_id(rental_id)

    if rental is None:
        raise ValueError("Rental not found.")

    if rental.status != "Active":
        raise ValueError(
            "Rental is not active."
        )

    updated_rental = Rental(
        rental_id=rental.id,
        user_id=rental.user_id,
        car_id=rental.car_id,
        start_date=rental.start_date,
        end_date=rental.end_date,
        total_cost=rental.total_cost,
        status="Cancelled"
    )

    success = update_json(
        RENTALS_FILE,
        rental_id,
        updated_rental.to_dict()
    )

    if not success:
        raise ValueError(
            "Rental could not be cancelled."
        )

    set_car_status(
        rental.car_id,
        "Available"
    )

    return updated_rental
