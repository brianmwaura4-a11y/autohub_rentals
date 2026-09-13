from car_rental.cli.admin_commands import (
    list_users_command,
    view_user_command,
    change_user_role_command,
    delete_user_command,
    list_all_cars_command,
    delete_car_command,
    list_rentals_command
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

from car_rental.cli.auth_commands import (
    logout_command
)


def admin_menu(session):

    current_user = session.get("user")

    while "user" in session:

        print("\n")
        print("=" * 50)
        print("ADMINISTRATOR MENU")
        print("=" * 50)
        print(f"Welcome, {current_user.username}")
        print()
        print("1. View Users")
        print("2. View User")
        print("3. Change User Role")
        print("4. Delete User")
        print("5. View All Cars")
        print("6. Add Car")
        print("7. Delete Car")
        print("8. View All Rentals")
        print("9. Logout")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            list_users_command()

        elif choice == "2":
            try:
                user_id = int(
                    input("Enter user ID: ")
                )

                view_user_command(user_id)

            except ValueError:
                print("Error: User ID must be a number.")

        elif choice == "3":
            try:
                user_id = int(
                    input("Enter user ID: ")
                )

                print("\nAvailable roles:")
                print("1. Customer")
                print("2. Rental Staff")
                print("3. Administrator")
                print("4. Maintenance")

                role_choice = input(
                    "Select role: "
                ).strip()

                roles = {
                    "1": "Customer",
                    "2": "Rental Staff",
                    "3": "Administrator",
                    "4": "Maintenance"
                }

                if role_choice not in roles:
                    print("Invalid role.")
                    continue

                change_user_role_command(
                    user_id,
                    roles[role_choice]
                )

            except ValueError:
                print("Error: User ID must be a number.")

        elif choice == "4":
            try:
                user_id = int(
                    input("Enter user ID: ")
                )

                if user_id == current_user.id:
                    print(
                        "Error: You cannot delete "
                        "your own account."
                    )
                    continue

                confirmation = input(
                    "Are you sure you want to delete "
                    "this user? (y/n): "
                ).strip().lower()

                if confirmation in {"y", "yes"}:
                    delete_user_command(user_id)
                else:
                    print("User deletion cancelled.")

            except ValueError:
                print("Error: User ID must be a number.")

        elif choice == "5":
            list_all_cars_command()

        elif choice == "6":
            try:
                make = input("Enter car make: ")
                model = input("Enter car model: ")
                year = int(
                    input("Enter manufacturing year: ")
                )
                registration = input(
                    "Enter registration number: "
                )
                daily_rate = float(
                    input("Enter daily rental rate: ")
                )

                add_car_command(
                    make,
                    model,
                    year,
                    registration,
                    daily_rate
                )

            except ValueError:
                print(
                    "Error: Please enter valid car information."
                )

        elif choice == "7":
            try:
                car_id = int(
                    input("Enter car ID: ")
                )

                confirmation = input(
                    "Are you sure you want to delete "
                    "this car? (y/n): "
                ).strip().lower()

                if confirmation in {"y", "yes"}:
                    delete_car_command(car_id)
                else:
                    print("Car deletion cancelled.")

            except ValueError:
                print("Error: Car ID must be a number.")

        elif choice == "8":
            list_rentals_command()

        elif choice == "9":
            logout_command(session)

        else:
            print("Invalid choice. Please try again.")


def customer_menu(session):

    current_user = session.get("user")

    while "user" in session:

        print("\n")
        print("=" * 50)
        print("CUSTOMER MENU")
        print("=" * 50)
        print(f"Welcome, {current_user.username}")
        print()
        print("1. View Available Cars")
        print("2. Rent a Car")
        print("3. View My Rentals")
        print("4. View Rental")
        print("5. Cancel Rental")
        print("6. Return Car")
        print("7. Logout")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            list_cars_command()

        elif choice == "2":
            try:
                car_id = int(
                    input("Enter car ID: ")
                )

                start_date = input(
                    "Enter start date (YYYY-MM-DD): "
                )

                end_date = input(
                    "Enter end date (YYYY-MM-DD): "
                )

                rent_car_command(
                    current_user.id,
                    car_id,
                    start_date,
                    end_date
                )

            except ValueError:
                print("Error: Car ID must be a number.")

        elif choice == "3":
            view_user_rentals_command(
                current_user.id
            )

        elif choice == "4":
            try:
                rental_id = int(
                    input("Enter rental ID: ")
                )

                view_rental_command(
                    rental_id
                )

            except ValueError:
                print(
                    "Error: Rental ID must be a number."
                )

        elif choice == "5":
            try:
                rental_id = int(
                    input("Enter rental ID: ")
                )

                cancel_rental_command(
                    rental_id
                )

            except ValueError:
                print(
                    "Error: Rental ID must be a number."
                )

        elif choice == "6":
            try:
                rental_id = int(
                    input("Enter rental ID: ")
                )

                return_car_command(
                    rental_id
                )

            except ValueError:
                print(
                    "Error: Rental ID must be a number."
                )

        elif choice == "7":
            logout_command(session)

        else:
            print("Invalid choice. Please try again.")


def start_user_menu(session):

    current_user = session.get("user")

    if current_user is None:
        print("No user is logged in.")
        return

    if current_user.role == "Administrator":
        admin_menu(session)
    else:
        customer_menu(session)
