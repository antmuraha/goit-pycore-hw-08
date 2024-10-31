import typing
from datetime import datetime, timedelta
from collections import UserDict
from record import Record


# Define the type for a single person
class PersonCongratulation(typing.TypedDict):
    name: str
    congratulation_date: str


# Define the type for a list of such dictionaries
PeopleCongratulationList = typing.List[PersonCongratulation]


class AddressBook(UserDict):
    '''
    A class for storing and managing records.
    '''

    def __init__(self):
        self.data = {}
        self.forward_days = 7
        self.length_week = 7
        self.length_work_week = 5
        self.date_format = "%d.%m.%Y"  # DD.MM.YYYY
        self.today = datetime.today().date()

    def __str__(self):
        return "\n".join(f"{x}" for x in self.values())

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data[name]

    def delete(self, name: str):
        removed_value = self.data.pop(name)
        return removed_value

    def get_upcoming_birthdays(self) -> PeopleCongratulationList:
        upcoming: PeopleCongratulationList = []
        for name in self.data:
            record = self.data[name]
            if not record.birthday:
                continue

            birthday = record.birthday.value
            birthday_this_year = birthday.replace(year=self.today.year)

            if birthday_this_year < self.today:
                birthday_this_year = birthday_this_year.replace(
                    year=self.today.year + 1)

            diff = (birthday_this_year - self.today).days
            if diff < self.forward_days:
                weekday = birthday_this_year.weekday()
                if weekday + 1 > self.length_work_week:
                    days = self.length_week - weekday
                    birthday_this_year = birthday_this_year + \
                        timedelta(days=days)
                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": birthday_this_year.strftime(self.date_format)
                })

        return upcoming
