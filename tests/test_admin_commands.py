from types import SimpleNamespace

from car_rental.cli import admin_commands


def test_list_users_command_success(monkeypatch, capsys):
    users = [
        SimpleNamespace(
            id=1,
            username="admin",
            role="Administrator"
        ),
        SimpleNamespace(
            id=2,
            username="brian",
            role="Customer"
        )
    ]

    monkeypatch.setattr(
        admin_commands,
        "get_users",
        lambda: users
    )

    result = admin_commands.list_users_command()

    captured = capsys.readouterr()

    assert result == users
    assert "Users" in captured.out
    assert "admin" in captured.out
    assert "brian" in captured.out
    assert "Administrator" in captured.out
    assert "Customer" in captured.out


def test_list_users_command_empty(monkeypatch, capsys):
    monkeypatch.setattr(
        admin_commands,
        "get_users",
        lambda: []
    )

    result = admin_commands.list_users_command()

    captured = capsys.readouterr()

    assert result == []
    assert "No users found." in captured.out


def test_view_user_command_success(monkeypatch, capsys):
    user = SimpleNamespace(
        id=1,
        username="admin",
        role="Administrator"
    )

    monkeypatch.setattr(
        admin_commands,
        "get_user_by_id",
        lambda user_id: user
    )

    result = admin_commands.view_user_command(1)

    captured = capsys.readouterr()

    assert result == user
    assert "User Details" in captured.out
    assert "ID: 1" in captured.out
    assert "Username: admin" in captured.out
    assert "Role: Administrator" in captured.out


def test_view_user_command_not_found(monkeypatch, capsys):
    monkeypatch.setattr(
        admin_commands,
        "get_user_by_id",
        lambda user_id: None
    )

    result = admin_commands.view_user_command(99)

    captured = capsys.readouterr()

    assert result is None
    assert "User not found." in captured.out


def test_change_user_role_command_success(
    monkeypatch,
    capsys
):
    user = SimpleNamespace(
        id=2,
        username="brian",
        role="Administrator"
    )

    monkeypatch.setattr(
        admin_commands,
        "update_user_role",
        lambda user_id, role: user
    )

    result = admin_commands.change_user_role_command(
        2,
        "Administrator"
    )

    captured = capsys.readouterr()

    assert result == user
    assert "User role updated successfully." in captured.out
    assert "Username: brian" in captured.out
    assert "New role: Administrator" in captured.out


def test_change_user_role_command_failure(
    monkeypatch,
    capsys
):
    def fake_update_user_role(user_id, role):
        raise ValueError("User not found.")

    monkeypatch.setattr(
        admin_commands,
        "update_user_role",
        fake_update_user_role
    )

    result = admin_commands.change_user_role_command(
        99,
        "Administrator"
    )

    captured = capsys.readouterr()

    assert result is None
    assert "Error: User not found." in captured.out


def test_delete_user_command_success(monkeypatch, capsys):
    monkeypatch.setattr(
        admin_commands,
        "delete_user",
        lambda user_id: True
    )

    result = admin_commands.delete_user_command(2)

    captured = capsys.readouterr()

    assert result is True
    assert "User deleted successfully." in captured.out


def test_delete_user_command_failure(monkeypatch, capsys):
    def fake_delete_user(user_id):
        raise ValueError("User not found.")

    monkeypatch.setattr(
        admin_commands,
        "delete_user",
        fake_delete_user
    )

    result = admin_commands.delete_user_command(99)

    captured = capsys.readouterr()

    assert result is False
    assert "Error: User not found." in captured.out


def test_list_all_cars_command_success(monkeypatch, capsys):
    cars = [
        SimpleNamespace(
            id=1,
            make="Toyota",
            model="Corolla",
            registration_number="KDA123A",
            daily_rate=1500,
            status="Available"
        )
    ]

    monkeypatch.setattr(
        admin_commands,
        "get_cars",
        lambda: cars
    )

    result = admin_commands.list_all_cars_command()

    captured = capsys.readouterr()

    assert result == cars
    assert "Cars" in captured.out
    assert "Toyota Corolla" in captured.out
    assert "KDA123A" in captured.out
    assert "KSh 1500" in captured.out
    assert "Available" in captured.out


def test_list_all_cars_command_empty(monkeypatch, capsys):
    monkeypatch.setattr(
        admin_commands,
        "get_cars",
        lambda: []
    )

    result = admin_commands.list_all_cars_command()

    captured = capsys.readouterr()

    assert result == []
    assert "No cars found." in captured.out


def test_delete_car_command_success(monkeypatch, capsys):
    monkeypatch.setattr(
        admin_commands,
        "delete_car",
        lambda car_id: True
    )

    result = admin_commands.delete_car_command(1)

    captured = capsys.readouterr()

    assert result is True
    assert "Car deleted successfully." in captured.out


def test_delete_car_command_failure(monkeypatch, capsys):
    def fake_delete_car(car_id):
        raise ValueError("Car not found.")

    monkeypatch.setattr(
        admin_commands,
        "delete_car",
        fake_delete_car
    )

    result = admin_commands.delete_car_command(99)

    captured = capsys.readouterr()

    assert result is False
    assert "Error: Car not found." in captured.out


def test_list_rentals_command_success(monkeypatch, capsys):
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
        admin_commands,
        "get_rentals",
        lambda: rentals
    )

    result = admin_commands.list_rentals_command()

    captured = capsys.readouterr()

    assert result == rentals
    assert "Rentals" in captured.out
    assert "User: 2" in captured.out
    assert "Car: 3" in captured.out
    assert "KSh 4500" in captured.out
    assert "Active" in captured.out


def test_list_rentals_command_empty(monkeypatch, capsys):
    monkeypatch.setattr(
        admin_commands,
        "get_rentals",
        lambda: []
    )

    result = admin_commands.list_rentals_command()

    captured = capsys.readouterr()

    assert result == []
    assert "No rentals found." in captured.out
