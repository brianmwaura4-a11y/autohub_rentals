class Car:
    """Represents a car available in the rental management system."""

    VALID_STATUSES = {
        "Available",
        "Rented",
        "Maintenance"
    }

    def __init__(
        self,
        car_id,
        make,
        model,
        year,
        registration_number,
        daily_rate,
        status="Available"
    ):
        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid car status.")

        self.id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.registration_number = registration_number
        self.daily_rate = daily_rate
        self.status = status

    def to_dict(self):
        """Convert the Car object into a dictionary for JSON storage."""
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "registration_number": self.registration_number,
            "daily_rate": self.daily_rate,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Car object from a dictionary."""
        return cls(
            car_id=data["id"],
            make=data["make"],
            model=data["model"],
            year=data["year"],
            registration_number=data["registration_number"],
            daily_rate=data["daily_rate"],
            status=data["status"]
        )