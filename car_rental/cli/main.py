import argparse

from car_rental.cli.admin_commands import (
    list_users_command,
    list_all_cars_command,
    list_rentals_command,
    delete_car_command
)

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
    return_car_command
)


def create_parser():

    parser = argparse.ArgumentParser(
        prog="car-rental",
        description="Car Rental Management System"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    # Register
    register_parser = subparsers.add_parser(
        "register",
        help="Register a new user"
    )

    register_parser.add_argument(
        "username",
        help="Username"
    )

    register_parser.add_argument(
        "password",
        help="Password"
    )

    register_parser.add_argument(
        "--role",
        default="Customer",
        choices=[
            "Customer",
            "Rental Staff",
            "Administrator",
            "Maintenance"
        ],
        help="User role"
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

    # Cars
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
        "make"
    )

    add_car_parser.add_argument(
        "model"
    )

    add_car_parser.add_argument(
        "year",
        type=int
    )

    add_car_parser.add_argument(
        "registration_number"
    )

    add_car_parser.add_argument(
        "daily_rate",
        type=float
    )

    # Rent
    rent_parser = subparsers.add_parser(
        "rent",
        help="Rent a car"
    )

    rent_parser.add_argument(
        "user_id",
        type=int
    )

    rent_parser.add_argument(
        "car_id",
        type=int
    )

    rent_parser.add_argument(
        "start_date"
    )

    rent_parser.add_argument(
        "end_date"
    )

    # Return
    return_parser = subparsers.add_parser(
        "return",
        help="Return a rented car"
    )

    return_parser.add_argument(
        "rental_id",
        type=int
    )
    
        # Users
    subparsers.add_parser(
        "users",
        help="List all users"
    )

    # All cars
    subparsers.add_parser(
        "all-cars",
        help="List all cars"
    )

    # Rentals
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
        type=int
    )

    return parser


def main():

    parser = create_parser()

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
