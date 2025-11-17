from models import AddressBook, Record
from functools import wraps
import pickle


def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not enough arguments provided."
    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    record.add_phone(phone)
    return message


@input_error
def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone updated."
    return "Contact not found."


@input_error
def get_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return "; ".join(phone.value for phone in record.phones)
    return "Contact not found."


@input_error
def show_all(book: AddressBook):
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, bday = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_birthday(bday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    return "Birthday not set or contact not found."


@input_error
def birthdays(args, book: AddressBook):
    result = book.get_upcoming_birthdays()
    return "\n".join(result) if result else "No birthdays this week."

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()