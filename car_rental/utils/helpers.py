def print_header(title):
    print()
    print("=" * 50)
    print(title)
    print("=" * 50)


def print_success(message):
    print(f"Success: {message}")


def print_error(message):
    print(f"Error: {message}")


def print_message(message):
    print(message)


def confirm_action(message):
    answer = input(f"{message} (y/n): ")

    return answer.strip().lower() in {"y", "yes"}
