import argparse

from car_rental.cli.auth_commands import (
    register_command,
    login_command
)

from car_rental.cli.car_commands import (
    list_cars_command,
    add_car_command
)

from car_rental.cli.rental_commands import (
    rent_car_command,
    view_rental_command,
    view_user_rentals_command,
    cancel_rental_command,
    return_car_command
)

from car_rental.cli.admin_commands import (
    list_users_command,
    list_all_cars_command,
    list_rentals_command,
    delete_car_command
)


def main():
    parser = argparse.ArgumentParser(
        description="AutoHub Car Rental Management System"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    # Register
    register_parser = subparsers.add_parser(
        "register",
        help="Register a new customer"
    )

    register_parser.add_argument(
        "username",
        help="Username"
    )

    register_parser.add_argument(
        "password",
        help="Password"
    )

    register_parser.set_defaults(
        role="Customer"
    )

    # Login
    login_parser = subparsers.add_parser(
        "login",
        help="Login to the system"
    )

    login_parser.add_argument(
        "username",
        help="Username"
    )

    login_parser.add_argument(
        "password",
        help="Password"
    )

    # List available cars
    subparsers.add_parser(
        "cars",
        help="List available cars"
    )

    # Add car
    add_car_parser = subparsers.add_parser(
        "add-car",
        help="Add a new car"
    )

    add_car_parser.add_argument(
        "make",
        help="Car make"
    )

    add_car_parser.add_argument(
        "model",
        help="Car model"
    )

    add_car_parser.add_argument(
        "year",
        type=int,
        help="Car manufacturing year"
    )

    add_car_parser.add_argument(
        "registration_number",
        help="Car registration number"
    )

    add_car_parser.add_argument(
        "daily_rate",
        type=float,
        help="Daily rental rate"
    )

    # Rent car
    rent_parser = subparsers.add_parser(
        "rent",
        help="Rent a car"
    )

    rent_parser.add_argument(
        "user_id",
        type=int,
        help="User ID"
    )

    rent_parser.add_argument(
        "car_id",
        type=int,
        help="Car ID"
    )

    rent_parser.add_argument(
        "start_date",
        help="Rental start date (YYYY-MM-DD)"
    )

    rent_parser.add_argument(
        "end_date",
        help="Rental end date (YYYY-MM-DD)"
    )

    # View rental
    view_rental_parser = subparsers.add_parser(
        "view-rental",
        help="View a rental"
    )

    view_rental_parser.add_argument(
        "rental_id",
        type=int,
        help="Rental ID"
    )

    # View user's rentals
    my_rentals_parser = subparsers.add_parser(
        "my-rentals",
        help="View rentals for a user"
    )

    my_rentals_parser.add_argument(
        "user_id",
        type=int,
        help="User ID"
    )

    # Cancel rental
    cancel_rental_parser = subparsers.add_parser(
        "cancel-rental",
        help="Cancel a rental"
    )

    cancel_rental_parser.add_argument(
        "rental_id",
        type=int,
        help="Rental ID"
    )

    # Return car
    return_parser = subparsers.add_parser(
        "return",
        help="Return a rented car"
    )

    return_parser.add_argument(
        "rental_id",
        type=int,
        help="Rental ID"
    )

    # List users
    subparsers.add_parser(
        "users",
        help="List all users"
    )

    # List all cars
    subparsers.add_parser(
        "all-cars",
        help="List all cars"
    )

    # List rentals
    subparsers.add_parser(
        "rentals",
        help="List all rentals"
    )

    # Delete car
    delete_car_parser = subparsers.add_parser(
        "delete-car",
        help="Delete a car"
    )

    delete_car_parser.add_argument(
        "car_id",
        type=int,
        help="Car ID"
    )

    args = parser.parse_args()

    if args.command == "register":
        register_command(
            args.username,
            args.password,
            args.role
        )

    elif args.command == "login":
        login_command(
            args.username,
            args.password
        )

    elif args.command == "cars":
        list_cars_command()

    elif args.command == "add-car":
        add_car_command(
            args.make,
            args.model,
            args.year,
            args.registration_number,
            args.daily_rate
        )

    elif args.command == "rent":
        rent_car_command(
            args.user_id,
            args.car_id,
            args.start_date,
            args.end_date
        )

    elif args.command == "view-rental":
        view_rental_command(
            args.rental_id
        )

    elif args.command == "my-rentals":
        view_user_rentals_command(
            args.user_id
        )

    elif args.command == "cancel-rental":
        cancel_rental_command(
            args.rental_id
        )

    elif args.command == "return":
        return_car_command(
            args.rental_id
        )

    elif args.command == "users":
        list_users_command()

    elif args.command == "all-cars":
        list_all_cars_command()

    elif args.command == "rentals":
        list_rentals_command()

    elif args.command == "delete-car":
        delete_car_command(
            args.car_id
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
