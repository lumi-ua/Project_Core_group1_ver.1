from datetime import datetime, timedelta

def check_birthday(birthday, days_to_check, current_date):
    birthday_date = datetime.strptime(birthday, "%Y-%m-%d").date()
    future_date = current_date + timedelta(days=days_to_check)
    return birthday_date <= future_date

def find_upcoming_birthdays(contacts, days_to_check):
    current_date = datetime.now().date()
    upcoming_birthdays = []

    for contact in contacts:
        if check_birthday(contact["birthday"], days_to_check, current_date):
            upcoming_birthdays.append(contact)

    return upcoming_birthdays

contacts = [
    {"name": "Tom", "birthday": "2023-08-06"},
    {"name": "Angela", "birthday": "2023-08-07"},
    {"name": "Bill", "birthday": "2023-08-08"}
]

days_to_check = int(input("Введіть кількість днів для перевірки: "))

upcoming_birthdays = find_upcoming_birthdays(contacts, days_to_check)

for contact in upcoming_birthdays:
    print(f"{contact['name']} має день народження через {days_to_check} днів.")
