def register_command(auth_service, input_function=input):

    print("\n=== User Registration ===")

    username = input_function("Enter username: ")
    password = input_function("Enter password: ")
    role = input_function("Enter role: ")

    try:
        user = auth_service.register_user(
            username=username,
            password=password,
            role=role
        )

        print(f"Registration successful. Welcome, {user.username}!")
        print(f"User ID: {user.id}")
        print(f"Role: {user.role}")

        return user

    except ValueError as error:
        print(f"Registration failed: {error}")
        return None


def login_command(auth_service, session, input_function=input):

    print("\n=== User Login ===")

    username = input_function("Enter username: ")
    password = input_function("Enter password: ")

    try:
        user = auth_service.login(
            username=username,
            password=password
        )

        session["user"] = user

        print(f"Login successful. Welcome back, {user.username}!")
        print(f"Role: {user.role}")

        return user

    except ValueError as error:
        print(f"Login failed: {error}")
        return None


def logout_command(auth_service, session):

    if "user" not in session:
        print("No user is currently logged in.")
        return

    username = session["user"].username
    auth_service.logout(session)
    print(f"{username} has been logged out successfully.")

def get_current_user(session):
    return session.get("user")

def is_logged_in(session):
    return "user" in session
