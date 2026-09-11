from car_rental.services.rental_service import (
    create_rental,
    get_rental_by_id,
    get_user_rentals,
    cancel_rental,
    complete_rental,
)


def rent_car(rentals, cars, user_id, car_id, pickup_date, return_date):
    return create_rental(
        rentals,
        cars,
        user_id,
        car_id,
        pickup_date,
        return_date
    )


def view_rental(rentals, rental_id):
    return get_rental_by_id(rentals, rental_id)


def view_user_rentals(rentals, user_id):
    return get_user_rentals(rentals, user_id)


def cancel_user_rental(rentals, cars, rental_id, user_id):
    return cancel_rental(rentals, cars, rental_id, user_id)


def complete_user_rental(rentals, cars, rental_id):
    return complete_rental(rentals, cars, rental_id)