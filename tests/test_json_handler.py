import json

from car_rental.utils.json_handler import (
    read_json,
    write_json,
    append_json,
    update_json,
    delete_json
)


def test_read_json():
    data = read_json("users.json")
    assert isinstance(data, list)


def test_write_json():
    test_data = [
        {
            "id": 1,
            "username": "testuser",
            "password_hash": "hash",
            "role": "Customer"
        }
    ]

    write_json("users.json", test_data)

    data = read_json("users.json")

    assert data == test_data


def test_append_json():
    test_data = [
        {
            "id": 1,
            "username": "testuser",
            "password_hash": "hash",
            "role": "Customer"
        }
    ]

    write_json("users.json", test_data)

    new_user = {
        "id": 2,
        "username": "anotheruser",
        "password_hash": "hash2",
        "role": "Customer"
    }

    append_json("users.json", new_user)

    data = read_json("users.json")

    assert len(data) == 2
    assert data[1] == new_user


def test_update_json():
    test_data = [
        {
            "id": 1,
            "username": "testuser",
            "password_hash": "hash",
            "role": "Customer"
        }
    ]

    write_json("users.json", test_data)

    updated_user = {
        "id": 1,
        "username": "updateduser",
        "password_hash": "newhash",
        "role": "Customer"
    }

    result = update_json("users.json", 1, updated_user)

    assert result is True
    assert read_json("users.json")[0] == updated_user


def test_delete_json():
    test_data = [
        {
            "id": 1,
            "username": "testuser",
            "password_hash": "hash",
            "role": "Customer"
        },
        {
            "id": 2,
            "username": "anotheruser",
            "password_hash": "hash2",
            "role": "Customer"
        }
    ]

    write_json("users.json", test_data)

    result = delete_json("users.json", 1)

    assert result is True
    assert len(read_json("users.json")) == 1
    assert read_json("users.json")[0]["id"] == 2
