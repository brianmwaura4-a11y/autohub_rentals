from car_rental.services.auth_service import get_users
from car_rental.services.car_service import (
    get_cars,
    delete_car
)
from car_rental.services.rental_service import get_rentals


def list_users_command():

    users = get_users()

    if not users:
        print("No users found.")
        return

    print("\nUsers")
    print("-" * 60)

    for user in users:
        print(
            f"ID: {user.id} | "
            f"Username: {user.username} | "
            f"Role: {user.role}"
        )


def list_all_cars_command():

    cars = get_cars()

    if not cars:
        print("No cars found.")
        return

    print("\nCars")
    print("-" * 60)

    for car in cars:
        print(
            f"ID: {car.id} | "
            f"{car.make} {car.model} | "
            f"Registration: {car.registration_number} | "
            f"Rate: KSh {car.daily_rate} | "
            f"Status: {car.status}"
        )


def list_rentals_command():

    rentals = get_rentals()

    if not rentals:
        print("No rentals found.")
        return

    print("\nRentals")
    print("-" * 60)

    for rental in rentals:
        print(
            f"ID: {rental.id} | "
            f"User: {rental.user_id} | "
            f"Car: {rental.car_id} | "
            f"{rental.start_date} to {rental.end_date} | "
            f"KSh {rental.total_cost} | "
            f"Status: {rental.status}"
        )


def delete_car_command(car_id):

    try:
        delete_car(car_id)

        print("Car deleted successfully.")

    except ValueError as error:
        print(f"Error: {error}")
