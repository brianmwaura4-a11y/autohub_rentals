from car_rental.cli import main as main_module


def test_main_no_command(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["car_rental"]
    )

    main_module.main()

    captured = capsys.readouterr()

    assert "AutoHub Car Rental Management System" in captured.out
    assert "register" in captured.out
    assert "register-admin" in captured.out
    assert "login" in captured.out


def test_main_register(monkeypatch):
    calls = {}

    def fake_register_command(
        username,
        password,
        role="Customer"
    ):
        calls["username"] = username
        calls["password"] = password
        calls["role"] = role

    monkeypatch.setattr(
        main_module,
        "register_command",
        fake_register_command
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "car_rental",
            "register",
            "brian",
            "password123"
        ]
    )

    main_module.main()

    assert calls["username"] == "brian"
    assert calls["password"] == "password123"
    assert calls["role"] == "Customer"


def test_main_register_admin(monkeypatch):
    calls = {}

    def fake_register_command(
        username,
        password,
        role="Customer"
    ):
        calls["username"] = username
        calls["password"] = password
        calls["role"] = role

    monkeypatch.setattr(
        main_module,
        "register_command",
        fake_register_command
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "car_rental",
            "register-admin",
            "admin",
            "password123"
        ]
    )

    main_module.main()

    assert calls["username"] == "admin"
    assert calls["password"] == "password123"
    assert calls["role"] == "Administrator"


def test_main_login_success(monkeypatch):
    calls = {}

    user = type(
        "User",
        (),
        {
            "username": "brian",
            "role": "Customer"
        }
    )()

    def fake_login_command(
        username,
        password,
        session
    ):
        calls["username"] = username
        calls["password"] = password
        calls["session"] = session
        return user

    def fake_start_user_menu(session):
        calls["menu_session"] = session

    monkeypatch.setattr(
        main_module,
        "login_command",
        fake_login_command
    )

    monkeypatch.setattr(
        main_module,
        "start_user_menu",
        fake_start_user_menu
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "car_rental",
            "login",
            "brian",
            "password123"
        ]
    )

    main_module.main()

    assert calls["username"] == "brian"
    assert calls["password"] == "password123"
    assert calls["menu_session"] == calls["session"]


def test_main_login_failure(monkeypatch):
    menu_called = False

    def fake_login_command(
        username,
        password,
        session
    ):
        return None

    def fake_start_user_menu(session):
        nonlocal menu_called
        menu_called = True

    monkeypatch.setattr(
        main_module,
        "login_command",
        fake_login_command
    )

    monkeypatch.setattr(
        main_module,
        "start_user_menu",
        fake_start_user_menu
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "car_rental",
            "login",
            "brian",
            "wrongpassword"
        ]
    )

    main_module.main()

    assert menu_called is False
