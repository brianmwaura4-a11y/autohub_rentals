from types import SimpleNamespace

from car_rental.cli import rental_commands


def test_rent_car_command_success(monkeypatch, capsys):
    rental = SimpleNamespace(
        id=1,
        user_id=2,
        car_id=3,
        start_date="2026-09-10",
        end_date="2026-09-13",
        total_cost=4500
    )

    def fake_create_rental(
        user_id,
        car_id,
        start_date,
        end_date
    ):
        return rental

    monkeypatch.setattr(
        rental_commands,
        "create_rental",
        fake_create_rental
    )

    result = rental_commands.rent_car_command(
        2,
        3,
        "2026-09-10",
        "2026-09-13"
    )

    captured = capsys.readouterr()

    assert result == rental
    assert "Car rented successfully!" in captured.out
    assert "Rental ID: 1" in captured.out
    assert "User ID: 2" in captured.out
    assert "Car ID: 3" in captured.out
    assert "Total cost: KSh 4500" in captured.out


def test_rent_car_command_failure(monkeypatch, capsys):
    def fake_create_rental(
        user_id,
        car_id,
        start_date,
        end_date
    ):
        raise ValueError("Car is not available for rental.")

    monkeypatch.setattr(
        rental_commands,
        "create_rental",
        fake_create_rental
    )

    result = rental_commands.rent_car_command(
        2,
        3,
        "2026-09-10",
        "2026-09-13"
    )

    captured = capsys.readouterr()

    assert result is None
    assert "Error: Car is not available for rental." in captured.out


def test_view_rental_command_success(monkeypatch, capsys):
    rental = SimpleNamespace(
        id=1,
        user_id=2,
        car_id=3,
        start_date="2026-09-10",
        end_date="2026-09-13",
        total_cost=4500,
        status="Active"
    )

    monkeypatch.setattr(
        rental_commands,
        "get_rental_by_id",
        lambda rental_id: rental
    )

    result = rental_commands.view_rental_command(1)

    captured = capsys.readouterr()

    assert result == rental
    assert "Rental Details" in captured.out
    assert "Rental ID: 1" in captured.out
    assert "Status: Active" in captured.out


def test_view_rental_command_not_found(monkeypatch, capsys):
    monkeypatch.setattr(
        rental_commands,
        "get_rental_by_id",
        lambda rental_id: None
    )

    result = rental_commands.view_rental_command(99)

    captured = capsys.readouterr()

    assert result is None
    assert "Rental not found." in captured.out


def test_view_user_rentals_command_success(monkeypatch, capsys):
    rentals = [
        SimpleNamespace(
            id=1,
            user_id=2,
            car_id=3,
            start_date="2026-09-10",
            end_date="2026-09-13",
            total_cost=4500,
            status="Active"
        )
    ]

    monkeypatch.setattr(
        rental_commands,
        "get_user_rentals",
        lambda user_id: rentals
    )

    result = rental_commands.view_user_rentals_command(2)

    captured = capsys.readouterr()

    assert result == rentals
    assert "User Rentals" in captured.out
    assert "Rental ID: 1" in captured.out
    assert "Car ID: 3" in captured.out


def test_view_user_rentals_command_empty(monkeypatch, capsys):
    monkeypatch.setattr(
        rental_commands,
        "get_user_rentals",
        lambda user_id: []
    )

    result = rental_commands.view_user_rentals_command(2)

    captured = capsys.readouterr()

    assert result == []
    assert "No rentals found for this user." in captured.out


def test_cancel_rental_command_success(monkeypatch, capsys):
    rental = SimpleNamespace(
        id=1,
        status="Cancelled"
    )

    monkeypatch.setattr(
        rental_commands,
        "cancel_rental",
        lambda rental_id: rental
    )

    result = rental_commands.cancel_rental_command(1)

    captured = capsys.readouterr()

    assert result == rental
    assert "Rental cancelled successfully!" in captured.out
    assert "Rental ID: 1" in captured.out
    assert "Status: Cancelled" in captured.out


def test_cancel_rental_command_failure(monkeypatch, capsys):
    def fake_cancel_rental(rental_id):
        raise ValueError("Rental is not active.")

    monkeypatch.setattr(
        rental_commands,
        "cancel_rental",
        fake_cancel_rental
    )

    result = rental_commands.cancel_rental_command(1)

    captured = capsys.readouterr()

    assert result is None
    assert "Error: Rental is not active." in captured.out


def test_return_car_command_success(monkeypatch, capsys):
    rental = SimpleNamespace(
        id=1,
        status="Completed"
    )

    monkeypatch.setattr(
        rental_commands,
        "return_car",
        lambda rental_id: rental
    )

    result = rental_commands.return_car_command(1)

    captured = capsys.readouterr()

    assert result == rental
    assert "Car returned successfully!" in captured.out
    assert "Rental ID: 1" in captured.out
    assert "Status: Completed" in captured.out


def test_return_car_command_failure(monkeypatch, capsys):
    def fake_return_car(rental_id):
        raise ValueError("Rental is not active.")

    monkeypatch.setattr(
        rental_commands,
        "return_car",
        fake_return_car
    )

    result = rental_commands.return_car_command(1)

    captured = capsys.readouterr()

    assert result is None
    assert "Error: Rental is not active." in captured.out
