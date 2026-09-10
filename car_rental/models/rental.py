class Rental:
    """Represents a car rental transaction."""

    VALID_STATUSES = {
        "Active",
        "Completed",
        "Cancelled"
    }

    def __init__(
        self,
        rental_id,
        user_id,
        car_id,
        start_date,
        end_date,
        total_cost,
        status="Active"
    ):
        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid rental status.")

        self.id = rental_id
        self.user_id = user_id
        self.car_id = car_id
        self.start_date = start_date
        self.end_date = end_date
        self.total_cost = total_cost
        self.status = status

    def to_dict(self):
        """Convert the Rental object into a dictionary for JSON storage."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "car_id": self.car_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_cost": self.total_cost,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Rental object from a dictionary."""
        return cls(
            rental_id=data["id"],
            user_id=data["user_id"],
            car_id=data["car_id"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            total_cost=data["total_cost"],
            status=data["status"]
        )
