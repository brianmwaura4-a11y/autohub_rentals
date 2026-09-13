from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from car_rental.models import User
from car_rental.utils.json_handler import (
    read_json,
    append_json
)
from car_rental.utils.validation import (
    validate_username,
    validate_password,
    validate_role
)


USERS_FILE = "users.json"


def get_users():
    """Return all users as User objects."""

    user_data = read_json(USERS_FILE)

    return [
        User.from_dict(data)
        for data in user_data
    ]


def find_user_by_username(username):
    """Find a user by username, ignoring letter case."""

    username = username.strip().lower()

    users = get_users()

    for user in users:
        if user.username.lower() == username:
            return user

    return None


def register_user(
    username,
    password,
    role="Customer"
):
    """Register a new user."""

    validate_username(username)
    validate_password(password)
    validate_role(role)

    username = username.strip()

    if find_user_by_username(username) is not None:
        raise ValueError(
            "Username already exists."
        )

    users = get_users()

    if users:
        new_id = max(
            user.id for user in users
        ) + 1
    else:
        new_id = 1

    password_hash = generate_password_hash(
        password
    )

    user = User(
        user_id=new_id,
        username=username,
        password_hash=password_hash,
        role=role
    )

    append_json(
        USERS_FILE,
        user.to_dict()
    )

    return user


def login_user(username, password):
    """Authenticate a user."""

    validate_username(username)

    user = find_user_by_username(username)

    if user is None:
        raise ValueError(
            "Invalid username or password."
        )

    if not check_password_hash(
        user.password_hash,
        password
    ):
        raise ValueError(
            "Invalid username or password."
        )

    return user


def has_role(user, role):
    """Check whether a user has a specific role."""

    return user.role == role
