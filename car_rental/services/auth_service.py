from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from car_rental.models import User

from car_rental.utils.json_handler import (
    read_json,
    append_json,
    update_json,
    delete_json
)

from car_rental.utils.validation import (
    validate_username,
    validate_password,
    validate_role
)


USERS_FILE = "users.json"


def get_users():

    user_data = read_json(USERS_FILE)

    return [
        User.from_dict(data)
        for data in user_data
    ]


def find_user_by_username(username):

    username = username.strip().lower()

    users = get_users()

    for user in users:
        if user.username.lower() == username:
            return user

    return None


def find_user(username):

    return find_user_by_username(username)


def register_user(
    username,
    password,
    role="Customer"
):

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


def get_user_by_id(user_id):

    users = get_users()

    for user in users:
        if user.id == user_id:
            return user

    return None


def has_role(user, role):

    return user is not None and user.role == role


def is_admin(user):

    return (
        user is not None
        and user.role == "Administrator"
    )


def update_user_role(user_id, new_role):

    validate_role(new_role)

    user = get_user_by_id(user_id)

    if user is None:
        raise ValueError("User not found.")

    updated_user = User(
        user_id=user.id,
        username=user.username,
        password_hash=user.password_hash,
        role=new_role
    )

    success = update_json(
        USERS_FILE,
        user_id,
        updated_user.to_dict()
    )

    if not success:
        raise ValueError(
            "User could not be updated."
        )

    return updated_user


def delete_user(user_id):

    user = get_user_by_id(user_id)

    if user is None:
        raise ValueError("User not found.")

    success = delete_json(
        USERS_FILE,
        user_id
    )

    if not success:
        raise ValueError(
            "User could not be deleted."
        )

    return True
def logout_user(session):

    if "user" in session:
        session.pop("user")
        return True

    return False
