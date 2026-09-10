from dataclasses import dataclassgi


@dataclass
class Rental:
    id: int
    user_id: int
    car_id: int
    start_date: str
    end_date: str
    total_cost: float
    status: str = "active"