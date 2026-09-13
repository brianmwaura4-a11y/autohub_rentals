def calculate_rental_cost(price_per_day, days):
    if days <= 0:
        raise ValueError("Rental days must be greater than 0.")

    return price_per_day * days

def create_rental(
    rentals,
    cars,
    user_id,
    car_id,
    pickup_date,
    return_date
):
   
    car = None

    for item in cars:
        if item["id"] == car_id:
            car = item
            break

    if car is None:
        raise ValueError("Car not found.")


    if not car["available"]:
        raise ValueError("Car is not available.")

        from datetime import datetime

    pickup = datetime.strptime(pickup_date, "%Y-%m-%d")
    return_day = datetime.strptime(return_date, "%Y-%m-%d")

    days = (return_day - pickup).days

    total_cost = calculate_rental_cost(
        car["price_per_day"],
        days
    )

    if rentals:
        rental_id = max(rental["id"] for rental in rentals) + 1
    else:
        rental_id = 1

    rental = {
        "id": rental_id,
        "user_id": user_id,
        "car_id": car_id,
        "pickup_date": pickup_date,
        "return_date": return_date,
        "total_cost": total_cost,
        "status": "active"
    }

    rentals.append(rental)

    car["available"] = False

    return rental

def get_rental_by_id(rentals, rental_id):
    for rental in rentals:
        if rental["id"] == rental_id:
            return rental

    return None

def get_user_rentals(rentals, user_id):
    return [
        rental
        for rental in rentals
        if rental["user_id"] == user_id
    ]

def cancel_rental(rentals, cars, rental_id, user_id):
    rental = get_rental_by_id(rentals, rental_id)

    if rental is None:
        raise ValueError("Rental not found.")

    if rental["user_id"] != user_id:
        raise PermissionError("You cannot cancel another user's rental.")

    if rental["status"] != "active":
        raise ValueError("Only active rentals can be cancelled.")

    rental["status"] = "cancelled"

    for car in cars:
        if car["id"] == rental["car_id"]:
            car["available"] = True
            break

    return rental

def complete_rental(rentals, cars, rental_id):
    rental = get_rental_by_id(rentals, rental_id)

    if rental is None:
        raise ValueError("Rental not found.")

    if rental["status"] != "active":
        raise ValueError("Only active rentals can be completed.")

    rental["status"] = "completed"

    for car in cars:
        if car["id"] == rental["car_id"]:
            car["available"] = True
            break

    return rental
