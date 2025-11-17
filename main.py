from models import AddressBook
from handlers import (
    add_contact, change_phone, get_phone, show_all,
    add_birthday, show_birthday, birthdays, save_data, load_data
)


def parse_input(user_input):
    parts = user_input.strip().split()
    return parts[0].lower(), parts[1:]


COMMANDS = {
    "hello": lambda args, book: "How can I help you?",
    "add": add_contact,
    "change": change_phone,
    "phone": get_phone,
    "all": lambda args, book: show_all(book),
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
}


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            save_data(book)
            print("Good bye!")
            break

        handler = COMMANDS.get(command)

        if handler:
            print(handler(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()