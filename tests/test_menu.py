from types import SimpleNamespace

from car_rental.cli import menu


def create_customer():
    return SimpleNamespace(
        id=1,
        username="brian",
        role="Customer"
    )


def create_admin():
    return SimpleNamespace(
        id=1,
        username="admin",
        role="Administrator"
    )


def test_start_user_menu_no_user(capsys):
    session = {}

    menu.start_user_menu(session)

    captured = capsys.readouterr()

    assert "No user is logged in." in captured.out


def test_start_user_menu_customer(monkeypatch):
    session = {
        "user": create_customer()
    }

    called = False

    def fake_customer_menu(current_session):
        nonlocal called
        called = True
        assert current_session == session

    monkeypatch.setattr(
        menu,
        "customer_menu",
        fake_customer_menu
    )

    menu.start_user_menu(session)

    assert called is True


def test_start_user_menu_admin(monkeypatch):
    session = {
        "user": create_admin()
    }

    called = False

    def fake_admin_menu(current_session):
        nonlocal called
        called = True
        assert current_session == session

    monkeypatch.setattr(
        menu,
        "admin_menu",
        fake_admin_menu
    )

    menu.start_user_menu(session)

    assert called is True


def test_customer_menu_view_cars(monkeypatch, capsys):
    session = {
        "user": create_customer()
    }

    called = False

    def fake_list_cars():
        nonlocal called
        called = True

    monkeypatch.setattr(
        menu,
        "list_cars_command",
        fake_list_cars
    )

    inputs = iter([
        "1",
        "7"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.customer_menu(session)

    assert called is True
    assert "CUSTOMER MENU" in capsys.readouterr().out


def test_customer_menu_view_my_rentals(monkeypatch):
    session = {
        "user": create_customer()
    }

    received_user_id = []

    def fake_view_user_rentals(user_id):
        received_user_id.append(user_id)

    monkeypatch.setattr(
        menu,
        "view_user_rentals_command",
        fake_view_user_rentals
    )

    inputs = iter([
        "3",
        "7"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.customer_menu(session)

    assert received_user_id == [1]


def test_customer_menu_invalid_choice(monkeypatch, capsys):
    session = {
        "user": create_customer()
    }

    inputs = iter([
        "99",
        "7"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.customer_menu(session)

    captured = capsys.readouterr()

    assert "Invalid choice. Please try again." in captured.out


def test_customer_menu_invalid_car_id(monkeypatch, capsys):
    session = {
        "user": create_customer()
    }

    inputs = iter([
        "2",
        "abc",
        "7"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.customer_menu(session)

    captured = capsys.readouterr()

    assert "Error: Car ID must be a number." in captured.out


def test_customer_menu_view_rental_invalid_id(
    monkeypatch,
    capsys
):
    session = {
        "user": create_customer()
    }

    inputs = iter([
        "4",
        "abc",
        "7"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.customer_menu(session)

    captured = capsys.readouterr()

    assert "Error: Rental ID must be a number." in captured.out


def test_customer_menu_logout(monkeypatch):
    session = {
        "user": create_customer()
    }

    def fake_logout(current_session):
        current_session.pop("user")

    monkeypatch.setattr(
        menu,
        "logout_command",
        fake_logout
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda message: "7"
    )

    menu.customer_menu(session)

    assert "user" not in session


def test_admin_menu_view_users(monkeypatch):
    session = {
        "user": create_admin()
    }

    called = False

    def fake_list_users():
        nonlocal called
        called = True

    monkeypatch.setattr(
        menu,
        "list_users_command",
        fake_list_users
    )

    inputs = iter([
        "1",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.admin_menu(session)

    assert called is True


def test_admin_menu_view_user_invalid_id(
    monkeypatch,
    capsys
):
    session = {
        "user": create_admin()
    }

    inputs = iter([
        "2",
        "abc",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.admin_menu(session)

    captured = capsys.readouterr()

    assert "Error: User ID must be a number." in captured.out


def test_admin_menu_change_user_role(
    monkeypatch
):
    session = {
        "user": create_admin()
    }

    calls = []

    def fake_change_user_role(user_id, role):
        calls.append((user_id, role))

    monkeypatch.setattr(
        menu,
        "change_user_role_command",
        fake_change_user_role
    )

    inputs = iter([
        "3",
        "2",
        "1",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.admin_menu(session)

    assert calls == [
        (2, "Customer")
    ]


def test_admin_menu_invalid_role(
    monkeypatch,
    capsys
):
    session = {
        "user": create_admin()
    }

    inputs = iter([
        "3",
        "2",
        "99",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.admin_menu(session)

    captured = capsys.readouterr()

    assert "Invalid role." in captured.out


def test_admin_cannot_delete_own_account(
    monkeypatch,
    capsys
):
    session = {
        "user": create_admin()
    }

    inputs = iter([
        "4",
        "1",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.admin_menu(session)

    captured = capsys.readouterr()

    assert "You cannot delete your own account." in captured.out


def test_admin_menu_delete_user_confirmed(
    monkeypatch
):
    session = {
        "user": create_admin()
    }

    calls = []

    def fake_delete_user(user_id):
        calls.append(user_id)

    monkeypatch.setattr(
        menu,
        "delete_user_command",
        fake_delete_user
    )

    inputs = iter([
        "4",
        "2",
        "y",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.admin_menu(session)

    assert calls == [2]


def test_admin_menu_delete_user_cancelled(
    monkeypatch,
    capsys
):
    session = {
        "user": create_admin()
    }

    calls = []

    monkeypatch.setattr(
        menu,
        "delete_user_command",
        lambda user_id: calls.append(user_id)
    )

    inputs = iter([
        "4",
        "2",
        "n",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.admin_menu(session)

    captured = capsys.readouterr()

    assert calls == []
    assert "User deletion cancelled." in captured.out


def test_admin_menu_view_all_cars(monkeypatch):
    session = {
        "user": create_admin()
    }

    called = False

    def fake_list_all_cars():
        nonlocal called
        called = True

    monkeypatch.setattr(
        menu,
        "list_all_cars_command",
        fake_list_all_cars
    )

    inputs = iter([
        "5",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.admin_menu(session)

    assert called is True


def test_admin_menu_view_rentals(monkeypatch):
    session = {
        "user": create_admin()
    }

    called = False

    def fake_list_rentals():
        nonlocal called
        called = True

    monkeypatch.setattr(
        menu,
        "list_rentals_command",
        fake_list_rentals
    )

    inputs = iter([
        "8",
        "9"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda message: next(inputs)
    )

    monkeypatch.setattr(
        menu,
        "logout_command",
        lambda current_session: current_session.pop("user")
    )

    menu.admin_menu(session)

    assert called is True
