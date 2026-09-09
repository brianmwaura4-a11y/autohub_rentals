from app.customers import add_customer, get_customer


def test_add_customer():
    customer = add_customer(
        "Brian",
        "brian@example.com",
        "0712345678"
    )

    assert customer["name"] == "Brian"
    assert customer["email"] == "brian@example.com"
    assert customer["phone"] == "0712345678"


def test_get_customer():
    add_customer(
        "Brian",
        "brian@example.com",
        "0712345678"
    )

    customer = get_customer(1)

    assert customer is not None
    assert customer["name"] == "Brian"


def test_get_nonexistent_customer():
    customer = get_customer(999)

    assert customer is None
