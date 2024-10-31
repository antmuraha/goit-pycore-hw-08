from enum import Enum
from address_book import AddressBook
from record import Record
from entities import FieldNameValueError, FieldBirthdayValueError, FieldPhoneValueError
from store import load_data, save_data


class BOT_COMMANDS(Enum):
    ADD_CONTACT = "cmd_add_contact"
    CMD_CHANGE_CONTACT = "cmd_change_contact"
    CMD_PHONE = "cmd_phone"
    CMD_ADD_BIRTHDAY = "cmd_add_birthday"
    CMD_SHOW_BIRTHDAY = "cmd_show_birthday"
    CMD_ALL = "cmd_all"


class CMD_TEMPLATES(Enum):
    cmd_add_contact = "add [username] [phone]"
    cmd_add_contact_desc = "The add contact."
    cmd_change_contact = "change [username] [phone] [new phone]"
    cmd_change_contact_desc = "The change contact."
    cmd_phone = "phone [username]"
    cmd_phone_desc = "To change phone for contact"
    cmd_add_birthday = "add-birthday [username] [birthday]"
    cmd_add_birthday_desc = "Adding a birthday for contact"
    cmd_show_birthday = "show-birthday [username]"
    cmd_show_birthday_desc = "Show birthday for contact"
    cmd_all = "all"
    cmd_all_desc = "Show all contacts"


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def get_enter_command_message(cmd: str):
    return f"Please enter command in the format: {CMD_TEMPLATES[cmd].value}"


def input_error(func):
    def validate(*args):
        params = args[0]
        contacts = args[1]
        func_name = func.__name__
        if func_name == BOT_COMMANDS.ADD_CONTACT.value:
            if len(params) == 0:
                msg = get_enter_command_message(func_name)
                complete = False
                return (msg, complete)

            if len(params) == 1:
                msg = "Please enter a phone."
                complete = False
                return (msg, complete)

        if func_name == BOT_COMMANDS.CMD_CHANGE_CONTACT.value:
            if len(params) == 0:
                msg = get_enter_command_message(func_name)
                complete = False
                return (msg, complete)

            if len(params) == 1:
                msg = "Please enter a phone."
                complete = False
                return (msg, complete)

            if len(params) == 2:
                msg = "Please enter a new phone."
                complete = False
                return (msg, complete)

            name, phone, new_phone = params
            if not contacts.get(name):
                msg = "Contact not exist"
                complete = False
                return (msg, complete)

        if func_name == BOT_COMMANDS.CMD_PHONE.value:
            if len(params) == 0:
                msg = get_enter_command_message(func_name)
                complete = False
                return (msg, complete)

            name = params[0]
            phone = contacts.get(name)
            if not phone:
                msg = "Contact not exist."
                complete = False
                return (msg, complete)

        if func_name == BOT_COMMANDS.CMD_ADD_BIRTHDAY.value:
            if len(params) == 0:
                msg = get_enter_command_message(func_name)
                complete = False
                return (msg, complete)
            if len(params) == 1:
                msg = "Please enter a birthday."
                complete = False
                return (msg, complete)

        if func_name == BOT_COMMANDS.CMD_SHOW_BIRTHDAY.value:
            if len(params) == 0:
                msg = get_enter_command_message(func_name)
                complete = False
                return (msg, complete)

        if func_name == BOT_COMMANDS.CMD_ALL.value:
            if len(contacts) == 0:
                msg = "Contacts list is empty"
                complete = False
                return (msg, complete)

        return func(*args)

    return validate


def cmd_hello(*args):
    msg = "How can I help you?"
    complete = False
    return (msg, complete)


def cmd_exit(*args):
    msg = "Good bye!"
    complete = True
    return (msg, complete)


@input_error
def cmd_add_contact(args, contacts):
    name, phone = args

    try:
        exist_record = contacts.get(name)
        if exist_record:
            exist_record.add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            contacts[name] = record

        msg = "Contact added."
        complete = False
        return (msg, complete)
    except FieldPhoneValueError as e:
        return (f"Invalid phone value", False)
    except FieldNameValueError as e:
        return (f"Invalid name value", False)


@input_error
def cmd_change_contact(args, contacts):
    name, phone, new_phone = args
    try:
        record = contacts.get(name)
        record.edit_phone(phone, new_phone)
        msg = "Contact changed."
        complete = False
        return (msg, complete)
    except FieldPhoneValueError as e:
        return (f"Invalid phone value", False)
    except FieldNameValueError as e:
        return (f"Invalid name value", False)


@input_error
def cmd_phone(args, contacts):
    name = args[0]
    record = contacts.get(name)
    phones = ", ".join(list(map(lambda p: p.value, record.phones)))
    msg = phones
    complete = False
    return (msg, complete)


@input_error
def cmd_add_birthday(args, contacts):
    name = args[0]
    birthday = args[1]
    try:
        record = contacts.get(name)
        if not record:
            return (f"Contact with name \"{name}\" not exist", False)
        record.add_birthday(birthday)
        return ("Birthday added.", False)
    except FieldBirthdayValueError as e:
        return ("Invalid birthday value. Must be in DD.MM.YYYY format", False)


@input_error
def cmd_show_birthday(args, contacts):
    name = args[0]
    record = contacts.get(name)

    if not record:
        return (f"Contact with name \"{name}\" not exist", False)

    field = record.birthday

    if not field:
        return (f"Birthday for \"{name}\" not set yet", False)

    return (f"{field.value}.", False)


@input_error
def cmd_birthdays(args, contacts: AddressBook):
    congratulations = contacts.get_upcoming_birthdays()
    msg = "\n".join(list(map(
        lambda x: f"{x.get('name')}: {x.get('congratulation_date')}", congratulations)))
    complete = False
    return (msg, complete)


@input_error
def cmd_all(args, contacts):
    msg = contacts
    complete = False
    return (msg, complete)


COMMANDS = {
    "hello": cmd_hello,
    "add": cmd_add_contact,
    "change": cmd_change_contact,
    "phone": cmd_phone,
    "add-birthday": cmd_add_birthday,
    "show-birthday": cmd_show_birthday,
    "birthdays": cmd_birthdays,
    "all": cmd_all,
    "close": cmd_exit,
    "exit": cmd_exit,
}


def bot(callback, args: list[str], contacts: AddressBook):
    msg, complete = callback(args, contacts)
    return msg, complete


def main():
    contacts = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        try:
            if not len(user_input.strip()):
                print("Please enter a command.")
                continue

            command, *args = parse_input(user_input)
            callback = COMMANDS.get(command)
            if callback:
                msg, complete = bot(callback, args, contacts)
                if msg:
                    print(msg)
                if complete:
                    save_data(contacts)
                    exit(0)
            else:
                print("Invalid command.")
        except Exception as e:
            print("Internal error", e)
