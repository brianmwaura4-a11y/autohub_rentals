from car_rental.services.auth_service import (
    register_user,
    login_user
)


def register_command(username, password, role="Customer"):
    try:
        user = register_user(
            username=username,
            password=password,
            role=role
        )

        print("Registration successful!")
        print(f"User ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Role: {user.role}")

        return user

    except ValueError as error:
        print(f"Registration failed: {error}")
        return None


def login_command(username, password, session):
    try:
        user = login_user(
            username=username,
            password=password
        )

        session["user"] = user

        print("Login successful!")
        print(f"Welcome, {user.username}!")
        print(f"Role: {user.role}")

        return user

    except ValueError as error:
        print(f"Login failed: {error}")
        return None


def logout_command(session):
    if "user" not in session:
        print("No user is currently logged in.")
        return

    username = session["user"].username
    session.pop("user")

    print(f"{username} has been logged out successfully.")


def get_current_user(session):
    return session.get("user")


def is_logged_in(session):
    return "user" in session
