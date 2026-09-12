"""
Car service.

This file contains the business logic for cars.

The CLI should NOT directly modify cars.json.

Instead:

CLI
 ↓
car_service.py
 ↓
json_handler.py
 ↓
cars.json
"""


from datetime import date, datetime

from car_rental.models.car import Car
from car_rental.utils.json_handler import load_data, save_data


# Location of the cars JSON file.
#
# Your team's json_handler.py will use this file
# to load and save car information.
CARS_FILE = "car_rental/data/cars.json"


def get_all_cars():
    """
    Get all cars from cars.json.

    Returns:
        A list of Car objects.
    """

    # Load the raw data from cars.json.
    data = load_data(CARS_FILE)

    # Convert every dictionary into a Car object.
    cars = [Car.from_dict(car) for car in data]

    return cars


def get_car_by_id(car_id):
    """
    Find one car using its ID.

    Parameters:
        car_id:
            ID of the car we want to find.

    Returns:
        Car object if found.
        None if the car does not exist.
    """

    # Get all cars first.
    cars = get_all_cars()

    # Search through every car.
    for car in cars:

        # Check whether this is the requested car.
        if car.car_id == car_id:
            return car

    # Nothing was found.
    return None


def generate_car_id():
    """
    Generate a new unique car ID.

    Example:

        Existing IDs:
        1
        2
        3

        New ID:
        4

    Returns:
        New car ID.
    """

    cars = get_all_cars()

    # If there are no cars yet,
    # start the IDs from 1.
    if not cars:
        return 1

    # Find the largest existing ID
    # and add 1.
    return max(car.car_id for car in cars) + 1


def add_car(
    make,
    model,
    year,
    registration,
    category,
    price_per_day,
    inspection_document="",
    inspection_date="",
    valid_until="",
    rating=0.0
):
    """
    Add a new car to the system.

    Returns:
        The newly created Car object.

    Raises:
        ValueError if the registration already exists.
    """

    # Get existing cars.
    cars = get_all_cars()

    # Check whether another car already has
    # the same registration number.
    for car in cars:

        if car.registration.lower() == registration.lower():
            raise ValueError(
                "A car with this registration already exists."
            )

    # Create the new Car object.
    car = Car(
        car_id=generate_car_id(),
        make=make,
        model=model,
        year=year,
        registration=registration,
        category=category,
        price_per_day=price_per_day,

        # New cars are available by default.
        available=True,

        rating=rating,

        inspection_document=inspection_document,
        inspection_date=inspection_date,
        valid_until=valid_until
    )

    # Add the new car to the list.
    cars.append(car)

    # Convert every Car object to a dictionary
    # before saving it as JSON.
    save_data(
        CARS_FILE,
        [item.to_dict() for item in cars]
    )

    # Return the new car to the CLI.
    return car


def update_car(car_id, **updates):
    """
    Update information about an existing car.

    Example:

        update_car(
            1,
            price_per_day=4000
        )

    This changes the price of car ID 1.

    Parameters:
        car_id:
            ID of the car to update.

        updates:
            Fields that need to be changed.

    Returns:
        Updated Car object.
    """

    # Load all cars.
    cars = get_all_cars()

    # Start with no car selected.
    car = None

    # Search for the requested car.
    for item in cars:

        if item.car_id == car_id:
            car = item
            break

    # If no car was found, stop the operation.
    if car is None:
        raise ValueError("Car not found.")

    # These are the fields that this service allows us
    # to update.
    allowed_fields = {
        "make",
        "model",
        "year",
        "registration",
        "category",
        "price_per_day",
        "available",
        "rating",
        "inspection_document",
        "inspection_date",
        "valid_until"
    }

    # Apply each requested update.
    for field, value in updates.items():

        # Only allow fields defined above.
        if field in allowed_fields:
            setattr(car, field, value)

    # Save the updated cars back to JSON.
    save_data(
        CARS_FILE,
        [item.to_dict() for item in cars]
    )

    return car


def delete_car(car_id):
    """
    Delete a car from the system.

    Parameters:
        car_id:
            ID of the car to delete.

    Returns:
        True when deletion succeeds.

    Raises:
        ValueError if the car does not exist.
    """

    # Load all cars.
    cars = get_all_cars()

    # Check whether the car exists.
    car = get_car_by_id(car_id)

    if car is None:
        raise ValueError("Car not found.")

    # Keep every car except the one being deleted.
    cars = [
        item
        for item in cars
        if item.car_id != car_id
    ]

    # Save the remaining cars.
    save_data(
        CARS_FILE,
        [item.to_dict() for item in cars]
    )

    return True


def check_availability(car_id):
    """
    Check whether a car is available.

    Returns:
        True if available.
        False if unavailable or not found.
    """

    car = get_car_by_id(car_id)

    # Car does not exist.
    if car is None:
        return False

    return car.available


def set_car_availability(car_id, available):
    """
    Change the availability of a car.

    Example:

        set_car_availability(1, False)

    This can be used when a car is rented.

        set_car_availability(1, True)

    This can be used when a car is returned.
    """

    return update_car(
        car_id,
        available=available
    )


def calculate_rating(scores):
    """
    Calculate the overall rating of a car.

    The rating is based on five areas:

        1. Engine
        2. Brakes
        3. Tyres
        4. Body
        5. Service

    Each score must be between 0 and 5.

    Example:

        [5, 4, 5, 4, 5]

    Average:

        4.6

    Returns:
        Rating rounded to one decimal place.
    """

    # Cannot calculate an average with no scores.
    if not scores:
        return 0.0

    # Make sure every score is between 0 and 5.
    if any(score < 0 or score > 5 for score in scores):
        raise ValueError(
            "Each score must be between 0 and 5."
        )

    # Calculate the average.
    rating = sum(scores) / len(scores)

    # Round to one decimal place.
    return round(rating, 1)


def update_car_rating(car_id, scores):
    """
    Calculate and save a new rating for a car.

    Parameters:
        car_id:
            ID of the car.

        scores:
            List of inspection/service scores.

    Example:

        update_car_rating(
            1,
            [5, 4, 5, 4, 5]
        )

    Returns:
        Updated Car object.
    """

    # Calculate the rating.
    rating = calculate_rating(scores)

    # Save the rating to the car.
    return update_car(
        car_id,
        rating=rating
    )


def check_validity(car_id):
    """
    Check whether a car's inspection document is still valid.

    The valid_until date must use:

        YYYY-MM-DD

    Example:

        2026-12-31

    Returns:
        True if the document is valid.
        False if expired, missing, invalid, or car not found.
    """

    # Find the car.
    car = get_car_by_id(car_id)

    if car is None:
        return False

    # If there is no expiry date,
    # we cannot confirm validity.
    if not car.valid_until:
        return False

    try:

        # Convert the text date into a Python date.
        expiry_date = datetime.strptime(
            car.valid_until,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        # The date was not in the correct format.
        return False

    # Compare expiry date with today's date.
    return expiry_date >= date.today()


def is_rentable(car_id):
    """
    Determine whether a car can actually be rented.

    A car is rentable only when:

        1. The car exists.
        2. The car is available.
        3. Its inspection/document is valid.

    Returns:
        True if the car can be rented.
        False otherwise.
    """

    car = get_car_by_id(car_id)

    if car is None:
        return False

    # Both conditions must be true.
    return (
        car.available
        and check_validity(car_id)
    )


def get_car_details(car_id):
    """
    Get complete information about one car.

    This is useful for the CLI because the customer
    can see:

        - Car information
        - Price
        - Rating
        - Inspection document
        - Inspection date
        - Validity
        - Rental status

    Returns:
        Dictionary containing complete car information.
        None if the car does not exist.
    """

    car = get_car_by_id(car_id)

    if car is None:
        return None

    return {
        "id": car.car_id,
        "make": car.make,
        "model": car.model,
        "year": car.year,
        "registration": car.registration,
        "category": car.category,
        "price_per_day": car.price_per_day,
        "available": car.available,
        "rating": car.rating,

        # Inspection/service document.
        "inspection_document": car.inspection_document,

        # Date inspection happened.
        "inspection_date": car.inspection_date,

        # Date inspection expires.
        "valid_until": car.valid_until,

        # Automatically check whether the document
        # is still valid.
        "valid": check_validity(car_id),

        # Automatically determine whether the car
        # is available AND has a valid document.
        "rentable": is_rentable(car_id)
    }