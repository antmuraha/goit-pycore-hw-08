import pickle
from address_book import AddressBook

DEFAULT_FILENAME = "addressbook.pkl"


def save_data(book, filename=DEFAULT_FILENAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename=DEFAULT_FILENAME):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        # Return a new address book if the file is not found
        return AddressBook()
