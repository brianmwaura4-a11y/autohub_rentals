class User:

    VALID_ROLES = {
        "Customer",
        "Rental Staff",
        "Administrator",
        "Maintenance"
    }

    def __init__(self, user_id, username, password_hash, role):
        if role not in self.VALID_ROLES:
            raise ValueError("Invalid user role.")

        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data["id"],
            username=data["username"],
            password_hash=data["password_hash"],
            role=data["role"]
        )
