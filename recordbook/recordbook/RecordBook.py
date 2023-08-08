# 
from collections import UserDict
from collections.abc import Iterator
import re
import pickle
from datetime import datetime
from datetime import timedelta

# батьківський клас
class Field():
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self.value)
    
# клас Ім'я
class Name(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value

  

# клас Телефон
class Phone(Field): 
    @property
    def value(self):
        return self.__value 
    
    @value.setter
    def value(self, value):
        if value.lower() == "none": 
            self.__value = "None"
            return ""   # не видаляти
        
        if value:
            correct_phone = ""
            for i in value: 
                if i in "+0123456789": correct_phone += i

            if len(correct_phone) == 13: self.__value = correct_phone # "+380123456789"
            elif len(correct_phone) == 12: self.__value = "+" + correct_phone # "380123456789"
            elif len(correct_phone) == 10: self.__value = "+38" + correct_phone # "0123456789"
            elif len(correct_phone) == 9: self.__value = "+380" + correct_phone # "123456789"
            else: raise PhoneException("Incorrect phone format")   # невірний формат телефона            

    
# клас День народження        
class Birthday(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        if value == None: 
            self.__value = None
            # raise BirthdayException("Unauthorized birthday format")
        else:
            pattern = r"^\d{2}(\.|\-|\/)\d{2}\1\d{4}$"  # дозволені дати формату DD.MM.YYYY 
            if re.match(pattern, value):         # альтернатива для крапки: "-" "/"
                self.__value = re.sub("[-/]", ".", value)  # комбінувати символи ЗАБОРОНЕНО DD.MM-YYYY 
            else: 
                self.__value = None


class Address(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        self.__value = value
  

class Email(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        if value == None: 
            self.__value = None
        else:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, value):
                raise EmailException("Invalid email address!")
            else:
                self.__value = value
      

#========================================================
# Класс Record, который отвечает за логику 
#  - добавления/удаления/редактирования
# необязательных полей и хранения обязательного поля Name
#=========================================================
class Record():
    def __init__(self, name:Name, phones: list, email: Email=None, birthday: Birthday=None, address: Address=None) -> None:
        self.name = name
        self.email = email
        self.birthday = birthday
        self.address = address
        self.phones = []            
        self.phones.extend(phones)


    def edit_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def edit_email(self, email: Email): 
        self.email = email

    def edit_address(self, address: Address): 
        self.address = address

    def change_name(self, name:Name, new_name:Name) -> None: 
        if self.name.value == name.value: self.name = new_name

    def __str__(self) -> str:
        result = f"{', '.join(map(lambda phone: phone.value, self.phones))}"
        if self.birthday.value != None:
            result = f"{self.birthday.value}|" + result
        if self.email != None and self.email.value != None:
            result = f"{self.email.value}|" + result
        if self.address != None and self.address.value != None:
            result = f"{self.address.value}|" + result

        return f"{self.name.value}|" + result
      

    # Done - розширюємо існуючий список телефонів особи - Done
    # НОВИМ телефоном або декількома телефонами для особи - Done
    def add_phone(self, list_phones) -> str:
        self.phones.extend(list_phones)
        return f"The phones was/were added - [bold green]success[/bold green]"
    
    # Done - видаляємо телефони із списку телефонів особи - Done!
    def del_phone(self, del_phone: Phone) -> str:
        error = True
        for phone in self.phones:
                if phone.value == del_phone.value: 
                    self.phones.remove(phone) 
                    self.phones.append(Phone("None")) if self.phones == [] else self.phones 
                    error = False  #видалення пройшло з успіхом
                    break
        if error: return f"The error has occurred. You entered an incorrect phone number."
        else: return f"The phone {phone.value} was deleted - [bold green]success[/bold green]"
    
    # Done = редагування запису(телефону) у книзі особи - Done
    def edit_phone(self, old_phone: Phone, new_phone: Phone) -> str:
        index = next((i for i, obj in enumerate(self.phones) if obj.value == old_phone.value), -1)
        self.phones[index]= new_phone
        return f"The person {self.name.value} has a new phone {new_phone.value} - [bold green]success[/bold green]"
    
    # повертає кількість днів до наступного дня народження
    def days_to_birthday(self):
        if self.birthday.value:
            now_date = datetime.now()
            now_year = now_date.year
            
             # Определяем формат строки для Даты
            date_format = "%d.%m.%Y %H:%M:%S"
            # Строка с Датой народження
            date_string = f"{self.birthday.value} 00:00:00"  
            dt = datetime.strptime(date_string, date_format)
            
            birthday = datetime(day=dt.day, month=dt.month, year=now_year)
            
            if now_date > birthday:
                birthday = birthday.replace(year=now_date.year + 1)
                dif = (birthday - now_date).days
                return f"до {birthday.strftime('%d.%m.%Y')} залишилося = {dif}"
            else:
                dif = (birthday - now_date).days
                return f"до {birthday.strftime('%d.%m.%Y')} залишилося = {dif}"
        else: return f"We have no information about {self.name.value}'s birthday."
    
    # перевіряє наявність 1(одного)телефону у списку
    def check_dublicate_phone(self, search_phone: str) ->bool:  
        result = list(map(lambda phone: any(phone.value == search_phone), self.data[self.name.value].phones))
        return True if result else False
    
class AddressBook(UserDict):

    def get_list_birthday(self, count_day: int):
        if count_day < 0: return []
        end_date = datetime.now() + timedelta(days=int(count_day))
        lst = [f"\nEnd date: {end_date.strftime('%d.%m.%Y')}"]
        for name, person in self.items():
            if not (person.birthday.value == "None"): 
                person_date = datetime.strptime(person.birthday.value, "%d.%m.%Y").date()
                person_month = person_date.month 
                person_day = person_date.day 
                dt = datetime(datetime.now().year, person_month, person_day) 
                if end_date >= dt > datetime.now(): 
                    lst.append(f"{name}|{person.birthday.value}|{', '.join(map(lambda phone: phone.value, person.phones))}")
        return "\n".join(lst)
       
    def add_record(self, record):
        self.data[record.name.value] = record
        return "1 record was successfully added - [bold green]success[/bold green]"
    
    # завантаження записів книги із файлу
    def load_database(self, path):
        if path.exists():
            with open(path, "rb") as fr_bin:
                self.data = pickle.load(fr_bin)  # копирование Словника   load_data = pickle.load(fr_bin)
                                                                    # self.data = {**load_data}
            return f"The database has been loaded = {len(self.data)} records"
        return ""
    
    #-----------------------------------------
    # збереження записів книги у файл  
    # формат збереження даних:
    #-------------------------------------------
    def save_database(self, path):
        with open(path, "wb") as f_out:
            pickle.dump(self.data, f_out)
        return f"The database is saved = {len(self.data)} records"    
            
    # генератор посторінкового друку
    def _record_generator(self, N=10):
        records = list(self.data.values())
        total_records = len(records)
        current_index = 0
        
        while current_index < total_records:
            batch = records[current_index: current_index + N]
            current_index += N
            yield batch

class PhoneException(Exception):
    def __init__(self, message):
        self.__message = None
        self.message = message
        #super().__init__(self.message)
    
    def __str__(self):
        return f"Attention: {self.message}"


class BirthdayException(Exception):
    def __init__(self, message):
        self.__message = None
        self.message = message
    
    def __str__(self):
        return f"Attention: {self.message}"

class EmailException(Exception):
    def __init__(self, message):
        self.__message = None
        self.message = message
    
    def __str__(self):
        return f"Attention: {self.message}"
    