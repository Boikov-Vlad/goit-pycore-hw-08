from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must be a string of 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year=today.year).date()
                delta = (bday_this_year - today).days
                if 0 <= delta <= 7:
                    upcoming.append(f"{record.name.value} — {bday_this_year.strftime('%d.%m')}")
        return upcoming