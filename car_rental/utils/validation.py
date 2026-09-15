from datetime import datetime


def validate_username(username):
    if not isinstance(username, str):
        raise ValueError("Username must be a string.")

    username = username.strip()

    if not username:
        raise ValueError("Username cannot be empty.")

    if len(username) < 3:
        raise ValueError("Username must be at least 3 characters long.")

    return True


def validate_password(password):
    if not isinstance(password, str):
        raise ValueError("Password must be a string.")

    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long.")

    return True


def validate_role(role):
    valid_roles = {
        "Customer",
        "Rental Staff",
        "Administrator",
        "Maintenance"
    }

    if role not in valid_roles:
        raise ValueError("Invalid user role.")

    return True


def validate_car_data(
    make,
    model,
    year,
    registration_number,
    daily_rate
):
    if not isinstance(make, str) or not make.strip():
        raise ValueError("Car make cannot be empty.")

    if not isinstance(model, str) or not model.strip():
        raise ValueError("Car model cannot be empty.")

    if not isinstance(year, int):
        raise ValueError("Car year must be an integer.")

    current_year = datetime.now().year

    if year < 1900 or year > current_year + 1:
        raise ValueError("Invalid car year.")

    if not isinstance(registration_number, str):
        raise ValueError("Registration number must be a string.")

    if not registration_number.strip():
        raise ValueError("Registration number cannot be empty.")

    if not isinstance(daily_rate, (int, float)):
        raise ValueError("Daily rate must be a number.")

    if daily_rate <= 0:
        raise ValueError("Daily rate must be greater than zero.")

    return True


def validate_dates(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            "Dates must use the YYYY-MM-DD format."
        )

    if end < start:
        raise ValueError(
            "End date cannot be before start date."
        )

    return True


def validate_positive_number(value, field_name):
    if not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number.")

    if value <= 0:
        raise ValueError(
            f"{field_name} must be greater than zero."
        )

    return True
