from app.auth import register_user, login_user


def test_register_user():
    result = register_user("brian", "password123")

    assert result is True


def test_login_with_correct_credentials():
    register_user("brian", "password123")

    result = login_user("brian", "password123")

    assert result is True


def test_login_with_wrong_password():
    register_user("brian", "password123")

    result = login_user("brian", "wrongpassword")

    assert result is False


def test_register_existing_user():
    register_user("brian", "password123")

    result = register_user("brian", "anotherpassword")

    assert result is False
