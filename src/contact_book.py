# 
from collections import UserDict
from collections.abc import Iterator
import re
import pickle
from datetime import datetime
from datetime import timedelta


class PhoneException(Exception):
   """Phone wrong number exception"""

class BirthdayException(Exception):
   """Birthday wrong format exception"""

class EmailException(Exception):
   """Email wrong format exception"""


class Field():
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value  #call setter of inheritor
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        if self.__value:
            return self.value
        return ""

    def __repr__(self) -> str:
        return str(self.value)

class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return super().value
    
    @value.setter
    def value(self, value):
        if value == None: 
            raise PhoneException("Incorrect phone format: None")
        else:
            correct_phone = re.match(r"(?:\+\d{2})?\d{9,10}", value, re.IGNORECASE)
            if correct_phone:
                phone = correct_phone.string

                if len(phone) == 13:   correct_phone = phone          # "+380123456789"
                elif len(phone) == 12: correct_phone = "+" + phone    # "380123456789"
                elif len(phone) == 10: correct_phone = "+38" + phone  # "0123456789"
                elif len(phone) == 9:  correct_phone = "+380" + phone # "123456789"
                else: raise PhoneException("Incorrect phone format!")
                super(Phone, Phone).value.__set__(self, correct_phone)
            else:
                raise PhoneException("Incorrect phone format")


class Birthday(Field):
    @property
    def value(self):
        return super().value
    
    @value.setter
    def value(self, value: str):
        if value == None: 
            super(Birthday, Birthday).value.__set__(self, None)
        else:
            # DD.MM.YYYY, DD-MM-YYYY, DD/MM/YYYY 
            pattern = r"^\d{2}(\.|\-|\/)\d{2}\1\d{4}$"
            if re.match(pattern, value):
                # заменяем слэши и дефисы на точки - приводим к одному формату
                result = re.sub("[-/]", ".", value)
                super(Birthday, Birthday).value.__set__(self, result)
            else:
                super(Birthday, Birthday).value.__set__(self, None)
                # устанавливаем None - для валидации 
                #raise BirthdayException("Unauthorized birthday format")

    # возвращает количество дней перед днём рождения
    def days_to_birthday(self):
        if self.value:
            # возвращает количество дней до следующего дня рождения.
            # если положительное то др еще не наступил, если отрицательное то уже прошел
            current_date = datetime.now().date()

            birthday = datetime.strptime(self.value, "%d.%m.%Y")
            birthday = birthday.replace(year=current_date.year).date()
            quantity_days = (birthday - current_date).days
            return quantity_days
        else: return -1


class Address(Field):
    pass


class Email(Field):
    @property
    def value(self):
        return super().value
    
    @value.setter
    def value(self, value: str):
        if value == None: 
            super(Email, Email).value.__set__(self, None)
        else:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, value):
                raise EmailException("Invalid email address!")
            else:
                super(Email, Email).value.__set__(self, value)


class Record():
    def __init__(self, name:Name, phones: list, email: Email=None, birthday: Birthday=None, address: Address=None) -> None:
        self.name = name
        self.email = email
        self.birthday = birthday
        self.address = address
        self.phones = []
        self.phones.extend(phones)


    def edit_birthday(self, birthday: Birthday):
        if birthday.value:
            self.birthday = birthday
            return f"bithday changed to: {birthday.value}"
        # если None то интерпретируем как удаление всего поля
        self.birthday = None
        return "birthday successfully deleted"

    def edit_email(self, email: Email):
        if email.value:
            self.email = email
            return f"email changed to: {email.value}"
        # если None то интерпретируем как удаление всего поля
        self.email = None
        return "email successfully deleted"

    def edit_address(self, address: Address):
        if address.value:
            self.address = address
            return f"address changed to: {address.value}"
        # если None то интерпретируем как удаление всего поля
        self.address = None
        return "address successfully deleted"

    def __str__(self) -> str:
        result = f"{', '.join(map(lambda phone: phone.value, self.phones))}"
        if self.birthday != None:
            result = f"{self.birthday} | " + result
        if self.email != None:
            result = f"{self.email} | " + result
        if self.address != None:
            result = f"{self.address} | " + result

        return f"{self.name} | " + result


    def add_phone(self, list_phones) -> str:
        self.phones.extend(list_phones)
        return f"Phone-numbers was added successfully"
    
    def del_phone(self, del_phone: Phone) -> str:
        error = True
        for phone in self.phones:
                if phone.value == del_phone.value: 
                    self.phones.remove(phone) 
                    self.phones.append(Phone("None")) if self.phones == [] else self.phones 
                    error = False  #видалення пройшло з успіхом
                    break
        if error: return f"Entered incorrect phone number."
        else: return f"The phone {phone.value} was deleted successfully"
    
    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> str:
        index = next((i for i, obj in enumerate(self.phones) if obj.value == old_phone.value), -1)
        self.phones[index]= new_phone
        return f"User set new phone-number successfully"


    def check_dublicate_phone(self, search_phone: str) ->bool:
        result = list(map(lambda phone: any(phone.value == search_phone), self.data[self.name.value].phones))
        return True if result else False


class AddressBook(UserDict):

    def search(self, text):
        result = []
        for rec in self.values():
            if (rec.name.value.lower().find(text.lower()) >= 0):
                result.append(rec)
                continue
            for phone in rec.phones:
                if phone.value.find(text.lower()) >= 0:
                    result.append(rec)
                    break
        return result

    def get_list_birthday(self, count_day: int):
        lst = []
        if count_day < 0: return lst
        for name, person in self.items():
            if person.birthday != None:
                days = person.birthday.days_to_birthday()

                if (0 <= days) and (days <= count_day):
                    lst.append(f"{name}|{person.birthday.value}")
        return "\n".join(lst)
       
    def add_record(self, record):
        self.data[record.name.value] = record
        return "1 record was added successfully"

    def rename_record(self, old_name: str, new_name: str):
        rec = self.data.pop(old_name)
        rec.name.value = new_name
        self.data[new_name] = rec
        return f"successfully renamed from:{old_name} to:{new_name}"
    
    def load_file(self, path):
        if path.exists():
            with open(path, "rb") as fr_bin:
                self.data = pickle.load(fr_bin)
                # load_data = pickle.load(fr_bin)
                # self.data = {**load_data}
            return f"The database has been loaded = {len(self.data)} records"
        return ""
    
    def save_database(self, path):
        with open(path, "wb") as f_out:
            pickle.dump(self.data, f_out)
        return f"The database is saved = {len(self.data)} records"
            
    def _record_generator(self, N=10):
        records = list(self.data.values())
        total_records = len(records)
        current_index = 0
        
        while current_index < total_records:
            batch = records[current_index: current_index + N]
            current_index += N
            yield batch

