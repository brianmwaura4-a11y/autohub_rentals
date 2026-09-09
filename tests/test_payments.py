from app.payments import make_payment, get_payment, calculate_balance


def test_make_payment():
    payment = make_payment(
        customer_id=1,
        rental_id=1,
        amount=10500
    )

    assert payment["customer_id"] == 1
    assert payment["rental_id"] == 1
    assert payment["amount"] == 10500
    assert payment["status"] == "paid"


def test_get_payment():
    make_payment(
        customer_id=1,
        rental_id=1,
        amount=10500
    )

    payment = get_payment(1)

    assert payment is not None
    assert payment["amount"] == 10500


def test_get_nonexistent_payment():
    payment = get_payment(999)

    assert payment is None


def test_calculate_balance():
    balance = calculate_balance(
        total_cost=15000,
        amount_paid=10000
    )

    assert balance == 5000


def test_full_payment_has_zero_balance():
    balance = calculate_balance(
        total_cost=15000,
        amount_paid=15000
    )

    assert balance == 0


def test_payment_cannot_exceed_total_cost():
    balance = calculate_balance(
        total_cost=15000,
        amount_paid=20000
    )

    assert balance == 0
