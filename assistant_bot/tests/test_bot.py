import unittest
from assistant_bot import bot, COMMANDS, AddressBook


name_one = "John"
name_two = "Andy"
phone_one = "1111111111"
phone_two = "2222222222"
birthday_one = "29.10.2001"
birthday_two = "02.11.2002"


class TestBot(unittest.TestCase):

    def test_hello(self):
        contacts = AddressBook()
        command = "hello"
        callback = COMMANDS[command]
        args = []
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, "How can I help you?")

    def test_add(self):
        contacts = AddressBook()
        command = "add"
        callback = COMMANDS[command]
        args = []
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, "Please enter command in the format: add [username] [phone]")

        args = [name_one]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, "Please enter a phone.")

        args = [name_one, "bad_phone_123"]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, "Invalid phone value")

        args = [name_one, phone_one]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, "Contact added.")

        args = [name_one, phone_two]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, "Contact added.")

        args = [name_two, phone_two]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, "Contact added.")

        self._all(contacts, [
            "Contact name: John, phones: 1111111111, 2222222222",
            "Contact name: Andy, phones: 2222222222"
        ])

        return contacts

    def test_change(self):
        contacts = self.test_add()
        command = "change"
        callback = COMMANDS[command]
        args = []
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, "Please enter command in the format: change [username] [phone] [new phone]")

        args = [name_one]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, "Please enter a phone.")

        args = [name_one, phone_one]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, "Please enter a new phone.")

        args = [name_one, phone_one, "invalid_phone"]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, "Invalid phone value")

        args = [name_one, phone_one, "4444444444"]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, "Contact changed.")

        self._all(contacts, [
            "Contact name: John, phones: 4444444444, 2222222222",
            "Contact name: Andy, phones: 2222222222"
        ])

    def test_phone(self):
        contacts = self.test_add()
        command = "phone"
        callback = COMMANDS[command]
        args = []
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, "Please enter command in the format: phone [username]")

        args = ["bad_name"]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, "Contact not exist.")

        args = [name_one]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, "1111111111, 2222222222")

    def test_add_birthday(self):
        contacts = self.test_add()
        command = "add-birthday"
        callback = COMMANDS[command]
        args = []
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, "Please enter command in the format: add-birthday [username] [birthday]")

        args = [name_one, birthday_one]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, "Birthday added.")

        args = ["bad_name", birthday_one]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, "Contact with name \"bad_name\" not exist")

        return contacts

    def test_show_birthday(self):
        contacts = self.test_add()
        command = "show-birthday"
        callback = COMMANDS[command]
        args = []
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, "Please enter command in the format: show-birthday [username]")

        args = ["bad_name"]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, "Contact with name \"bad_name\" not exist")

        args = [name_one]
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(
            msg, f"Birthday for \"{name_one}\" not set yet")

        contacts = self.test_add_birthday()
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(msg, f"2001-10-29.")

        return contacts

    def test_all(self):
        contacts = self.test_show_birthday()
        self._all(contacts, [
            "Contact name: John (2001-10-29), phones: 1111111111, 2222222222",
            "Contact name: Andy, phones: 2222222222"
        ])

    def _all(self, contacts, results: list[str]):
        command = "all"
        callback = COMMANDS[command]
        args = []
        msg, complete = bot(callback, args, contacts)
        self.assertEqual(f"{msg}", "\n".join(results))


if __name__ == '__main__':
    unittest.main()
