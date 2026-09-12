"""
Car model.

This file defines the Car class.

The Car class represents one car in the rental system.
It stores information such as:
- car ID
- make
- model
- year
- registration number
- category
- rental price
- availability
- rating
- inspection document
- inspection date
- document validity date
"""


class Car:
    """
    Represents a car in the car rental system.
    """

    def __init__(
        self,
        car_id,
        make,
        model,
        year,
        registration,
        category,
        price_per_day,
        available=True,
        rating=0.0,
        inspection_document="",
        inspection_date="",
        valid_until=""
    ):
        """
        Create a new Car object.

        Parameters:
            car_id:
                Unique ID of the car.

            make:
                Manufacturer of the car.
                Example: Toyota

            model:
                Model of the car.
                Example: Corolla

            year:
                Manufacturing year.
                Example: 2022

            registration:
                Vehicle registration number.
                Example: KDA 123A

            category:
                Type/category of the car.
                Example: Sedan, SUV, Van

            price_per_day:
                Rental price charged per day.

            available:
                Shows whether the car is currently available
                for renting.

            rating:
                Overall car rating from 0 to 5.

            inspection_document:
                Name/path/reference of the inspection document.

            inspection_date:
                Date when the car was inspected.

            valid_until:
                Date when the inspection/document expires.
        """

        # Store the unique car ID.
        self.car_id = car_id

        # Store the car manufacturer.
        self.make = make

        # Store the car model.
        self.model = model

        # Store the manufacturing year.
        self.year = year

        # Store the registration number.
        self.registration = registration

        # Store the category of the car.
        self.category = category

        # Store the amount charged per rental day.
        self.price_per_day = price_per_day

        # True means the car can currently be rented.
        self.available = available

        # Store the car's rating.
        self.rating = rating

        # Store the inspection/service document.
        self.inspection_document = inspection_document

        # Store the date the car was inspected.
        self.inspection_date = inspection_date

        # Store the date the inspection becomes invalid.
        self.valid_until = valid_until

    def to_dict(self):
        """
        Convert the Car object into a dictionary.

        Why?

        JSON files cannot directly store Python objects.
        Therefore, before saving a Car to cars.json,
        we convert it into a dictionary.

        Returns:
            A dictionary containing all car information.
        """

        return {
            "id": self.car_id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "registration": self.registration,
            "category": self.category,
            "price_per_day": self.price_per_day,
            "available": self.available,
            "rating": self.rating,
            "inspection_document": self.inspection_document,
            "inspection_date": self.inspection_date,
            "valid_until": self.valid_until
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a Car object from dictionary data.

        This is the opposite of to_dict().

        When we read a car from cars.json, we get a dictionary.
        This method converts that dictionary back into a Car object.

        Parameters:
            data:
                Dictionary containing car information.

        Returns:
            A Car object.
        """

        return cls(
            car_id=data["id"],
            make=data["make"],
            model=data["model"],
            year=data["year"],
            registration=data["registration"],
            category=data["category"],
            price_per_day=data["price_per_day"],

            # .get() gives a default value if the field
            # does not exist in the JSON file.
            available=data.get("available", True),

            rating=data.get("rating", 0.0),

            inspection_document=data.get(
                "inspection_document",
                ""
            ),

            inspection_date=data.get(
                "inspection_date",
                ""
            ),

            valid_until=data.get(
                "valid_until",
                ""
            )
        )

    