"""
Car CLI commands.

This file handles the command-line interface for cars.

It receives commands from the user and sends them
to car_service.py.

The CLI should not directly edit cars.json.
"""


from car_rental.services.car_service import (
    get_all_cars,
    get_car_details,
    add_car,
    update_car,
    delete_car,
    update_car_rating,
)


def show_cars():
    """
    Display all cars.

    This is the command that allows a customer/admin
    to see the list of cars.
    """

    # Ask the service for all cars.
    cars = get_all_cars()

    # If there are no cars, tell the user.
    if not cars:
        print("No cars available.")
        return

    print("\nAvailable Cars")
    print("=" * 60)

    # Display each car.
    for car in cars:

        # Convert True/False into readable text.
        availability = (
            "Available"
            if car.available
            else "Not Available"
        )

        print(f"ID: {car.car_id}")
        print(f"Car: {car.make} {car.model}")
        print(f"Year: {car.year}")
        print(f"Category: {car.category}")
        print(
            f"Price: KSh "
            f"{car.price_per_day:,.2f}/day"
        )
        print(f"Rating: {car.rating}/5")
        print(f"Status: {availability}")

        # Only show validity date when it exists.
        if car.valid_until:
            print(
                f"Valid Until: "
                f"{car.valid_until}"
            )

        print("-" * 60)


def show_car(car_id):
    """
    Display detailed information about one car.

    The customer can see:

        - Basic car information
        - Price
        - Rating
        - Inspection document
        - Inspection date
        - Validity
        - Whether the car can be rented
    """

    # Get detailed information from the service.
    details = get_car_details(car_id)

    # Car does not exist.
    if details is None:
        print("Car not found.")
        return

    print("\nCar Details")
    print("=" * 60)

    print(f"ID: {details['id']}")
    print(f"Make: {details['make']}")
    print(f"Model: {details['model']}")
    print(f"Year: {details['year']}")
    print(
        f"Registration: "
        f"{details['registration']}"
    )
    print(
        f"Category: "
        f"{details['category']}"
    )
    print(
        f"Price: KSh "
        f"{details['price_per_day']:,.2f}/day"
    )

    # Display the car rating.
    print(
        f"Rating: "
        f"{details['rating']}/5"
    )

    # Display availability.
    print(
        "Availability: "
        + (
            "Available"
            if details["available"]
            else "Not Available"
        )
    )

    # Display inspection document.
    print(
        "Inspection Document: "
        + (
            details["inspection_document"]
            or "Not provided"
        )
    )

    # Display inspection date.
    print(
        "Inspection Date: "
        + (
            details["inspection_date"]
            or "Not provided"
        )
    )

    # Display expiry/validity date.
    print(
        "Valid Until: "
        + (
            details["valid_until"]
            or "Not provided"
        )
    )

    # Show whether the document is valid.
    print(
        "Inspection Status: "
        + (
            "VALID"
            if details["valid"]
            else "INVALID/EXPIRED"
        )
    )

    # Show whether the customer can rent it.
    print(
        "Rental Status: "
        + (
            "RENTABLE"
            if details["rentable"]
            else "NOT RENTABLE"
        )
    )


def add_car_command(args):
    """
    CLI command for adding a new car.

    The values come from argparse and are sent
    to car_service.add_car().
    """

    try:

        # Send the user's information to the service.
        car = add_car(
            make=args.make,
            model=args.model,
            year=args.year,
            registration=args.registration,
            category=args.category,
            price_per_day=args.price,
            inspection_document=args.document,
            inspection_date=args.inspection_date,
            valid_until=args.valid_until,
            rating=args.rating
        )

        print(
            "Car added successfully. "
            f"Car ID: {car.car_id}"
        )

    except ValueError as error:

        # Display validation/business errors.
        print(f"Error: {error}")


def update_car_command(args):
    """
    CLI command for updating an existing car.

    Only values supplied by the user are updated.
    """

    # Start with an empty dictionary.
    updates = {}

    # Add only the fields that the user supplied.

    if args.make:
        updates["make"] = args.make

    if args.model:
        updates["model"] = args.model

    if args.year:
        updates["year"] = args.year

    if args.category:
        updates["category"] = args.category

    if args.price is not None:
        updates["price_per_day"] = args.price

    if args.document:
        updates["inspection_document"] = args.document

    if args.inspection_date:
        updates["inspection_date"] = args.inspection_date

    if args.valid_until:
        updates["valid_until"] = args.valid_until

    try:

        # Send the updates to the service.
        update_car(
            args.car_id,
            **updates
        )

        print("Car updated successfully.")

    except ValueError as error:
        print(f"Error: {error}")


def delete_car_command(args):
    """
    CLI command for deleting a car.
    """

    try:

        # Tell the service to delete the car.
        delete_car(args.car_id)

        print("Car deleted successfully.")

    except ValueError as error:
        print(f"Error: {error}")


def rate_car_command(args):
    """
    CLI command for rating a car.

    The rating is based on five areas:

        Engine
        Brakes
        Tyres
        Body
        Service
    """

    try:

        # Put all five scores into a list.
        scores = [
            args.engine,
            args.brakes,
            args.tyres,
            args.body,
            args.service
        ]

        # Send the scores to the service.
        car = update_car_rating(
            args.car_id,
            scores
        )

        print(
            f"{car.make} {car.model} "
            f"has been rated "
            f"{car.rating}/5."
        )

    except ValueError as error:
        print(f"Error: {error}")


def register_car_commands(subparsers):
    """
    Register all car-related commands with argparse.

    Brian's main.py will call this function.

    Commands created here include:

        cars
        car
        add-car
        update-car
        delete-car
        rate-car
    """

    # --------------------------------------------------
    # COMMAND 1: cars
    # --------------------------------------------------
    #
    # Displays all cars.
    #
    # Example:
    #
    # python -m car_rental cars
    #

    cars_parser = subparsers.add_parser(
        "cars",
        help="Display all cars"
    )

    cars_parser.set_defaults(
        func=lambda args: show_cars()
    )


    # --------------------------------------------------
    # COMMAND 2: car
    # --------------------------------------------------
    #
    # Displays details of one car.
    #
    # Example:
    #
    # python -m car_rental car 1
    #

    car_parser = subparsers.add_parser(
        "car",
        help="Display details of a car"
    )

    car_parser.add_argument(
        "car_id",
        type=int
    )

    car_parser.set_defaults(
        func=lambda args: show_car(args.car_id)
    )


    # --------------------------------------------------
    # COMMAND 3: add-car
    # --------------------------------------------------
    #
    # Adds a new car.
    #
    # Example:
    #
    # python -m car_rental add-car \
    # --make Toyota \
    # --model Corolla \
    # --year 2022 \
    # --registration KDA123A \
    # --category Sedan \
    # --price 3500
    #

    add_parser = subparsers.add_parser(
        "add-car",
        help="Add a new car"
    )

    add_parser.add_argument(
        "--make",
        required=True
    )

    add_parser.add_argument(
        "--model",
        required=True
    )

    add_parser.add_argument(
        "--year",
        required=True,
        type=int
    )

    add_parser.add_argument(
        "--registration",
        required=True
    )

    add_parser.add_argument(
        "--category",
        required=True
    )

    add_parser.add_argument(
        "--price",
        required=True,
        type=float
    )

    # Inspection/service document.
    add_parser.add_argument(
        "--document",
        default=""
    )

    # Date of inspection.
    add_parser.add_argument(
        "--inspection-date",
        default=""
    )

    # Date when the document expires.
    add_parser.add_argument(
        "--valid-until",
        default=""
    )

    # Initial rating.
    add_parser.add_argument(
        "--rating",
        default=0.0,
        type=float
    )

    add_parser.set_defaults(
        func=add_car_command
    )


    # --------------------------------------------------
    # COMMAND 4: update-car
    # --------------------------------------------------
    #
    # Updates an existing car.
    #
    # Example:
    #
    # python -m car_rental update-car 1 --price 4000
    #

    update_parser = subparsers.add_parser(
        "update-car",
        help="Update a car"
    )

    update_parser.add_argument(
        "car_id",
        type=int
    )

    update_parser.add_argument("--make")
    update_parser.add_argument("--model")
    update_parser.add_argument(
        "--year",
        type=int
    )
    update_parser.add_argument("--category")
    update_parser.add_argument(
        "--price",
        type=float
    )
    update_parser.add_argument("--document")
    update_parser.add_argument(
        "--inspection-date"
    )
    update_parser.add_argument(
        "--valid-until"
    )

    update_parser.set_defaults(
        func=update_car_command
    )


    # --------------------------------------------------
    # COMMAND 5: delete-car
    # --------------------------------------------------
    #
    # Deletes a car.
    #
    # Example:
    #
    # python -m car_rental delete-car 1
    #

    delete_parser = subparsers.add_parser(
        "delete-car",
        help="Delete a car"
    )

    delete_parser.add_argument(
        "car_id",
        type=int
    )

    delete_parser.set_defaults(
        func=delete_car_command
    )


    # --------------------------------------------------
    # COMMAND 6: rate-car
    # --------------------------------------------------
    #
    # Rates a car based on inspection/service scores.
    #
    # Example:
    #
    # python -m car_rental rate-car 1 \
    # --engine 5 \
    # --brakes 4 \
    # --tyres 5 \
    # --body 4 \
    # --service 5
    #

    rate_parser = subparsers.add_parser(
        "rate-car",
        help="Rate a car from inspection/service scores"
    )

    rate_parser.add_argument(
        "car_id",
        type=int
    )

    rate_parser.add_argument(
        "--engine",
        required=True,
        type=float
    )

    rate_parser.add_argument(
        "--brakes",
        required=True,
        type=float
    )

    rate_parser.add_argument(
        "--tyres",
        required=True,
        type=float
    )

    rate_parser.add_argument(
        "--body",
        required=True,
        type=float
    )

    rate_parser.add_argument(
        "--service",
        required=True,
        type=float
    )

    rate_parser.set_defaults(
        func=rate_car_command
    )

    