from car_rental.services.rental_service import (
    create_rental,
    get_rental_by_id,
    get_active_rentals,
    return_car,
    cancel_rental
)


def rent_car_command(user_id, car_id, start_date, end_date):
    try:
        rental = create_rental(
            user_id,
            car_id,
            start_date,
            end_date
        )

        print("Car rented successfully!")
        print(f"Rental ID: {rental.id}")
        print(f"User ID: {rental.user_id}")
        print(f"Car ID: {rental.car_id}")
        print(f"Start date: {rental.start_date}")
        print(f"End date: {rental.end_date}")
        print(f"Total cost: KSh {rental.total_cost}")

        return rental

    except ValueError as error:
        print(f"Error: {error}")
        return None


def view_rental_command(rental_id):
    rental = get_rental_by_id(rental_id)

    if rental is None:
        print("Rental not found.")
        return None

    print(f"Rental ID: {rental.id}")
    print(f"User ID: {rental.user_id}")
    print(f"Car ID: {rental.car_id}")
    print(f"Start date: {rental.start_date}")
    print(f"End date: {rental.end_date}")
    print(f"Total cost: KSh {rental.total_cost}")
    print(f"Status: {rental.status}")

    return rental


def cancel_rental_command(rental_id):
    try:
        rental = cancel_rental(rental_id)

        print("Rental cancelled successfully!")
        print(f"Rental ID: {rental.id}")
        print(f"Status: {rental.status}")

        return rental

    except ValueError as error:
        print(f"Error: {error}")
        return None


def return_car_command(rental_id):
    try:
        rental = return_car(rental_id)

        print("Car returned successfully!")
        print(f"Rental ID: {rental.id}")
        print(f"Status: {rental.status}")

        return rental

    except ValueError as error:
        print(f"Error: {error}")
        return None