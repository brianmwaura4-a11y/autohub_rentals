from car_rental.services.car_service import (
    get_cars,
    get_available_cars,
    add_car,
    update_car,
    delete_car
)


def list_cars_command():
    

    cars = get_available_cars()

    if not cars:
        print("No cars are currently available.")
        return []

    print("\nAvailable Cars")
    print("-" * 70)

    for car in cars:
        print(
            f"ID: {car.id} | "
            f"{car.make} {car.model} | "
            f"Year: {car.year} | "
            f"Registration: {car.registration_number} | "
            f"Daily Rate: KSh {car.daily_rate}"
        )

    return cars


def list_all_cars_command():
    

    cars = get_cars()

    if not cars:
        print("No cars found.")
        return []

    print("\nAll Cars")
    print("-" * 80)

    for car in cars:
        print(
            f"ID: {car.id} | "
            f"{car.make} {car.model} | "
            f"Year: {car.year} | "
            f"Registration: {car.registration_number} | "
            f"Daily Rate: KSh {car.daily_rate} | "
            f"Status: {car.status}"
        )

    return cars


def add_car_command(
    make,
    model,
    year,
    registration_number,
    daily_rate
):
    

    try:
        car = add_car(
            make,
            model,
            year,
            registration_number,
            daily_rate
        )

        print("\nCar added successfully!")
        print(f"Car ID: {car.id}")
        print(f"Make: {car.make}")
        print(f"Model: {car.model}")
        print(f"Year: {car.year}")
        print(
            f"Registration: "
            f"{car.registration_number}"
        )
        print(
            f"Daily Rate: "
            f"KSh {car.daily_rate}"
        )
        print(f"Status: {car.status}")

        return car

    except ValueError as error:
        print(f"Error: {error}")
        return None


def update_car_command(
    car_id,
    make,
    model,
    year,
    registration_number,
    daily_rate,
    status
):
    

    try:
        car = update_car(
            car_id,
            make,
            model,
            year,
            registration_number,
            daily_rate,
            status
        )

        print("\nCar updated successfully!")
        print(f"Car ID: {car.id}")
        print(f"Make: {car.make}")
        print(f"Model: {car.model}")
        print(f"Year: {car.year}")
        print(
            f"Registration: "
            f"{car.registration_number}"
        )
        print(
            f"Daily Rate: "
            f"KSh {car.daily_rate}"
        )
        print(f"Status: {car.status}")

        return car

    except ValueError as error:
        print(f"Error: {error}")
        return None


def delete_car_command(car_id):
    

    try:
        delete_car(car_id)

        print("Car deleted successfully.")

        return True

    except ValueError as error:
        print(f"Error: {error}")

        return False
