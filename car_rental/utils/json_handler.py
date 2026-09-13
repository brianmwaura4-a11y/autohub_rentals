import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def read_json(filename):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(filename, data):
    file_path = DATA_DIR / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def append_json(filename, item):
    data = read_json(filename)
    data.append(item)
    write_json(filename, data)


def update_json(filename, item_id, updated_item):
    data = read_json(filename)

    for index, item in enumerate(data):
        if item["id"] == item_id:
            data[index] = updated_item
            write_json(filename, data)
            return True

    return False


def delete_json(filename, item_id):
    data = read_json(filename)

    updated_data = [
        item for item in data
        if item["id"] != item_id
    ]

    if len(updated_data) == len(data):
        return False

    write_json(filename, updated_data)
    return True
