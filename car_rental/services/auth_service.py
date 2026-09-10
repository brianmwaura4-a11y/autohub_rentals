import hashlib
import json
import secrets
from pathlib import Path

from car_rental.models.user import User


class AuthService:

    def __init__(self, users_file=None):
        if users_file is None:
            users_file = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "users.json"
            )

        self.users_file = Path(users_file)
        self._ensure_users_file()

    def _ensure_users_file(self):
        self.users_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.users_file.exists():
            self.users_file.write_text("[]")

    def _load_users(self):
        try:
            with open(self.users_file, "r") as file:
                data = json.load(file)

            if not isinstance(data, list):
                return []

            return data

        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_users(self, users):
        with open(self.users_file, "w") as file:
            json.dump(users, file, indent=4)

    def _hash_password(self, password):
        salt = secrets.token_hex(16)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000
        )

        return f"{salt}${password_hash.hex()}"

    def _verify_password(self, password, stored_hash):
        try:
            salt, password_hash = stored_hash.split("$")

            calculated_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                100_000
            )

            return secrets.compare_digest(
                calculated_hash.hex(),
                password_hash
            )

        except (ValueError, AttributeError):
            return False

    def _generate_user_id(self, users):
        existing_ids = {user["id"] for user in users}

        while True:
            user_id = f"USR{secrets.token_hex(4).upper()}"

            if user_id not in existing_ids:
                return user_id

    def register_user(self, username, password, role):
        if not username or not username.strip():
            raise ValueError("Username cannot be empty.")

        if not password or len(password) < 6:
            raise ValueError(
                "Password must be at least 6 characters long."
            )

        if role not in User.VALID_ROLES:
            raise ValueError("Invalid user role.")

        username = username.strip()

        users = self._load_users()

        if any(
            user["username"].lower() == username.lower()
            for user in users
        ):
            raise ValueError("Username already exists.")

        user_id = self._generate_user_id(users)

        password_hash = self._hash_password(password)

        user = User(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            role=role
        )

        users.append(user.to_dict())
        self._save_users(users)

        return user

    def get_user_by_username(self, username):
        users = self._load_users()

        for user_data in users:
            if user_data["username"].lower() == username.lower():
                return User.from_dict(user_data)

        return None

    def login(self, username, password):
        user = self.get_user_by_username(username)

        if user is None:
            raise ValueError("Invalid username or password.")

        if not self._verify_password(
            password,
            user.password_hash
        ):
            raise ValueError("Invalid username or password.")

        return user

    def has_role(self, user, role):
        return user.role == role

    def logout(self, session):
        session.clear()
        