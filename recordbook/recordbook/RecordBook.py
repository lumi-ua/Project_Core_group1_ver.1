# 
from collections import UserDict
from collections.abc import Iterator
import re
import datetime
import pickle

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
    def value(self, value:str):
        print(value)
        if value.lower() == "none": 
            self.__value = "None"
        else:
            pattern = r"^\d{2}(\.|\-|\/)\d{2}\1\d{4}$"  # дозволені дати формату DD.MM.YYYY 
            if re.match(pattern, value):         # альтернатива для крапки: "-" "/"
                self.__value = re.sub("[-/]", ".", value)  # комбінувати символи ЗАБОРОНЕНО DD.MM-YYYY 

class Address(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value

  
class Email(Field):
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        if value.lower() == "none": 
            self.__value = "None"
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
    def __init__(self, name:Name, phones: Phone=None, email: Email=None, birthday: Birthday=None, address: Address=None) -> None:
        self.name = name            
        self.phones = [] 
        self.email = email
        self.birthday = birthday
        self.address = address
        self.phones.append(phones)
        
# ======================================================================================================
# =========================================[ add ]======================================================
# ======================================================================================================

    def add_to_birthday(self, birthday:Birthday):
        self.birthday = birthday

    def add_email(self, email:Email) -> None: 
        self.email.value = email.value

    def add_address(self, address:Address) -> None: 
        self.address.value = ' '.join(address)

# ======================================================================================================
# =========================================[ remove ]===================================================
# ======================================================================================================

    def remove_phone(self, phones:Phone) -> str:
        if len(self.phones) == 0: return "This contact has no phone numbers saved"
        
        for n in self.phones:
            if n.value == phones.value:
                if len(self.phones) == 1:
                    self.add_phone(Phone("None"))
                self.phones.remove(n)
                return phones

    def remove_birthday(self, birthday:Birthday) -> None:
        if self.birthday.value == birthday.value: self.birthday.value = "None"

    def remove_email(self, email:Email) -> None: 
        if self.email.value == email.value: self.email.value = "None"

    def remove_address(self) -> None: 
        self.address.value = "None"

# ======================================================================================================
# =========================================[ change ]===================================================
# ======================================================================================================

    def change_name(self, name:Name, new_name:Name) -> None: 
        if self.name.value == name.value: self.name = new_name

    def change_phone(self, old_phone:Phone, new_phone:Phone) -> str:
        for phones in self.phones:
            if str(old_phone) == str(phones):
                self.remove_phone(old_phone)
                self.add_phone(new_phone)
                return f"Phone {old_phone} change to {new_phone} for {self.name} contact "
        return f"Phone {old_phone} for contact {self.name} doesn`t exist"

    def change_birthday(self, birthday:Birthday, new_birthday:Birthday) -> None:
        if self.birthday.value == birthday.value: self.birthday = new_birthday

    def change_email(self, email:Email, new_email:Email) -> None: 
        if self.email.value == email.value: self.email = new_email

    def change_address(self, new_address:Address) -> None: 
        self.address.value = ' '.join(new_address.value)

    def __str__(self):
        return "{}{}{}{}{}".format(
                                   f"Name: {self.name}\n", 
                                   f'Phone: {", ".join([str(p) for p in self.phones]) if self.phones else "No phone"}\n', 
                                   'Email: ' + str(self.email.value) + "\n" if self.email is not "None" else "Email: No email\n",
                                   'Address: ' + str(self.address) + "\n" if self.address is not "None" else 'Address: No address\n',
                                   'Birthday: ' + str(self.birthday.value) + "\n" if self.birthday is not "None" else "Birthday: No birthday date\n")                       

    def __repr__(self):
        return "{}{}{}{}{}".format(
                                   f"Name: {self.name}\n", 
                                   f'Phone: {", ".join([str(p) for p in self.phones]) if self.phones else "No phone"}\n', 
                                   'Email: ' + str(self.email.value) + "\n" if self.email is not "None" else "Email: No email\n",
                                   'Address: ' + str(self.address) + "\n" if self.address is not "None" else 'Address: No address\n',
                                   'Birthday: ' + str(self.birthday.value) + "\n" if self.birthday is not "None" else "Birthday: No birthday date\n")                       



    # def __str__(self) -> str:
    #     return f"{self.name.value}|{self.birthday.value}|{', '.join(map(lambda phone: phone.value, self.phones))}" 
    
    # Done - розширюємо існуючий список телефонів особи - Done
    # НОВИМ телефоном або декількома телефонами для особи - Done
    def add_phone(self, new_phone: Phone) -> str:
        self.phones.append(new_phone)
        return f"The phones was/were added - [bold green]success[/bold green]"
    
    # # Done - видаляємо телефони із списку телефонів особи - Done!
    # def del_phone(self, del_phone: Phone) -> str:
    #     error = True
    #     for phone in self.phones:
    #             if phone.value == del_phone.value: 
    #                 self.phones.remove(phone) 
    #                 self.phones.append(Phone("None")) if self.phones == [] else self.phones 
    #                 error = False  #видалення пройшло з успіхом
    #                 break
    #     if error: return f"The error has occurred. You entered an incorrect phone number."
    #     else: return f"The phone {phone.value} was deleted - [bold green]success[/bold green]"
    
    # # Done = редагування запису(телефону) у книзі особи - Done
    # def edit_phone(self, old_phone: Phone, new_phone: Phone) -> str:
    #     index = next((i for i, obj in enumerate(self.phones) if obj.value == old_phone.value), -1)
    #     self.phones[index]= new_phone
    #     return f"The person {self.name.value} has a new phone {new_phone.value} - [bold green]success[/bold green]"
    
    # повертає кількість днів до наступного дня народження
    def days_to_birthday(self):
        if self.birthday.value:
            now_date = datetime.datetime.now()
            now_year = now_date.year
            
             # Определяем формат строки для Даты
            date_format = "%d.%m.%Y %H:%M:%S"
            # Строка с Датой народження
            date_string = f"{self.birthday.value} 00:00:00"  
            dt = datetime.datetime.strptime(date_string, date_format)
            
            birthday = datetime.datetime(day=dt.day, month=dt.month, year=now_year)
            
            if now_date > birthday:
                birthday = birthday.replace(year=now_date.year + 1)
                dif = birthday - now_date
                return f"до {birthday.strftime('%d.%m.%Y')} залишилося = {dif}"
            else:
                dif = birthday - now_date
                return f"до {birthday.strftime('%d.%m.%Y')} залишилося = {dif}"
        else: return f"We have no information about {self.name.value}'s birthday."
    
    # # змінює день народження для особи
    # def change_birthday(self, birthday: Birthday):
    #     self.birthday = birthday
    #     return f"Birthday for {self.name.value} is changed - [bold green]success[/bold green]"
    
    # перевіряє наявність 1(одного)телефону у списку
    def check_dublicate_phone(self, search_phone: str) ->bool:  
        result = list(map(lambda phone: any(phone.value == search_phone), self.data[self.name.value].phones))
        return True if result else False
    

class AddressBook(UserDict):
       
    def add_record(self, record):
        self.data[record.name.value] = record
        return "1 record was successfully added - [bold green]success[/bold green]"
    
    # завантаження записів книги із файлу
    def load_database(self, path):
        with open(path, "rb") as fr_bin:
            self.data = pickle.load(fr_bin)  # копирование Словника   load_data = pickle.load(fr_bin)
                                                                    # self.data = {**load_data}
        return f"The database has been loaded = {len(self.data)} records"
    
    #-----------------------------------------
    # збереження записів книги у файл  
    # формат збереження даних:
    #
    # Lisa|15.08.1984|+380739990022, +380677711122
    # Alex|None|+380954448899, +380506667788   
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
    
