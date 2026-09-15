import argparse

from car_rental.cli.auth_commands import (
    register_command,
    login_command
)

from car_rental.cli.menu import start_user_menu


def main():
    parser = argparse.ArgumentParser(
        description="AutoHub Car Rental Management System"
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

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

    admin_register_parser = subparsers.add_parser(
        "register-admin",
        help="Register a new administrator"
    )

    admin_register_parser.add_argument(
        "username",
        help="Administrator username"
    )

    admin_register_parser.add_argument(
        "password",
        help="Administrator password"
    )

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

    args = parser.parse_args()

    session = {}

    if args.command == "register":
        register_command(
            username=args.username,
            password=args.password
        )

    elif args.command == "register-admin":
        register_command(
            username=args.username,
            password=args.password,
            role="Administrator"
        )

    elif args.command == "login":
        user = login_command(
            username=args.username,
            password=args.password,
            session=session
        )

        if user is not None:
            start_user_menu(session)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
