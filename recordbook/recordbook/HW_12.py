
from pathlib import Path
import os, sys
import platform  # для clearscrean()
from RecordBook import AddressBook, Record, Name, Phone, Email, Birthday, Address, PhoneException, BirthdayException, EmailException
from clean import sort_main
from note_book import NoteBook, Note, Tag
from datetime import datetime
import re
import readline # pip install pyreadline3

from rich import print
from rich import box
from rich.table import Table
from rich.console import Console

path_book = Path(sys.path[0]).joinpath("user_book.bin")
path_note = Path(sys.path[0]).joinpath("note_book.json")

book = AddressBook()
note_book = NoteBook()
        
# Декоратор для Обробки командної строки
def input_error(func):
    def wrapper(*args):
        result = None
        try:
            result = func(*args)
        # Обробка виключних ситуацій
        except BirthdayException as e:
            print(e)
        except PhoneException as e:
            print(e)
        except EmailException as e:
            print(e)
        except FileNotFoundError:    # Файл бази даних Відсутній
            print("The database isn't found")
        except ValueError:
            print("Incorect data or unsupported format while writing to the file")
        except KeyError:
            print("Record isn't in the database")
        except KeyboardInterrupt:
            func_exit(args)
        except TypeError:
            print("Incorect data")
        return result
    return wrapper


#=========================================================
# Блок функцій для роботи з нотатками
#=========================================================
# >> note-add <текст нотатки будь-якої довжини> <teg-ключове слово> 
# example >> note-add My first note in this bot.
#=========================================================
@input_error
def note_add(args):
    return note_book.create_note(args)

@input_error
def add_tags(args: str):
    params = args.strip().split()
    if len(params) > 1:
        note_id = params[0]
        tags_list = params[1:]
        return note_book.add_tags(note_id, tags_list)
    else: return "Expected > 1 params"

@input_error
def del_tags(args: str):
    params = args.strip().split()
    if len(params) >= 1:
        note_id = params[0]
        tags_list = params[1:] if len(params) > 1 else None
        note_book.del_tags(note_id, tags_list)
        return "del_tags successfully"
    else: return ""

#=========================================================
# >> note del <key-ідентифікатор запису>
# example >> note del 1691245959.0
#=========================================================
@input_error
def note_del(args):
    params = args.strip().split()
    if len(params) == 1:
        return note_book.del_note(params[0])
    else: return "Wrong params amount"
    

#=========================================================
# >> note change <key-record> <New notes> <tag>
# example >> note change 1691245959.0 My new notes. #Tag 
#=========================================================
@input_error
def note_change(args):
    args = args.lstrip()
    n = args.find(" ")
    key = args[:n]
    note_text = args[n+1:]
    print(f"key:{key} txt:{note_text}")
    result = note_book.change_note(key, note_text)
    return result


#=========================================================
# >> note find <fragment>
# Фрагмент має бути однією фразою без пробілів
# example >> note find word
#=========================================================
@input_error
def note_find(args):
    notes_list = note_book.find_notes(args)
    if notes_list:
        return f"Search result in notes: {len(notes_list)}"
    else:
        return f"No one notes was found for fragment: '{args}'"


#=========================================================
# >> note show <int: необов'язковий аргумент кількості рядків>
# Передається необов'язковий аргумент кількості рядків 
# example >> note show 15
#=========================================================
@input_error
def note_show(args):
    params = args.strip().split()
    if len(params) == 1:
        note_key = params[0]
        if note_key in note_book.keys():
            note = note_book.data[note_key]
            return str(note)
        else:
            print(f"note.key:{note_key} was not found")
    return ""

    if args.startswith("/") and args[1:].isdigit():
        args = int(args[1:])
    else:
        args = 5    
    for page, rec in enumerate(note_book.iterator(args), 1):
        print(f"Page {page}\n")
        for item in rec:
            print(f"{item}")
        
        input("\nFor next page press enter")
    return ""

@input_error
def tag_show(args):
    params = args.strip().split()
    if len(params) == 1:
        tag_key = params[0]
        if tag_key in note_book.tags.keys():
            tag = note_book.tags[tag_key]
            return str(tag)
    return ""

#=========================================================
# >> note sort
# Сортування нотаток по тегу
# example >> note sort
#=========================================================
@input_error
def note_sort(args):    
    result = []
    for rec in note_book.values():
        line = f"{rec.tag}  {rec.note}  {rec.key}"
        result.append(line)
    result.sort()
    count = 0
    for item in result:
        print(item)
        count += 1
        if count == 5:
            input("\nFor next page press enter\n")
            count = 0
    return ""

@input_error
def notebook_show(args):
    for note in note_book.data.values():
        print(f"[{(len(note.tags))}] {note.key}: " + note.value)
    for tag in note_book.tags.values():
        print("[" + str(tag.sz()) + "]#" + tag.value)
    return ""

#=========================================================
# >> add ...  DONE
# По этой команде бот сохраняет в памяти (в словаре например) новый контакт. 
# Вместо ... пользователь вводит ИМЯ и НОМЕР телефона, обязательно через пробел.
# example >> add Mike 02.10.1990 +380504995876
#=========================================================
@input_error
def func_new_rec(*args):

    count_prm = len(args)

    if (count_prm >= 2):
        # Якщо ключ (ІМ'Я) що користувач хоче ДОДАТИ не ІСНУЄ тобто можемо додавати
        if not args[0].capitalize() in book.keys():

            name = args[0]
            new_name = Name(args[0].capitalize())
           
            # TODO: refactor birthday-positioing
            new_birthday = Birthday(args[1])

            if new_birthday.value == None:
                args = args[1:]
            else:
                args = args[2:]
     
            if len(args) > 0:
                lst_phones = list(map(lambda phone: Phone(phone.strip()), args))
                rec = Record(name=new_name, birthday=new_birthday, phones=lst_phones)
                book.add_record(rec)
            else:
                raise PhoneException("Phone absent in arguments")
            
            return "1 record was successfully added - [bold green]success[/bold green]"
        else: return "The person is already in database"  # Повернемо помилку -> "Неможливо дадати існуючу людину"
    else:
        return f"Expected 3 arguments, but {count_prm} was given.\nHer's an example >> add Mike 02.10.1990 +380504995876"
     
     
#=========================================================
# >> show all         Done
# По этой команде бот выводит все сохраненные контакты 
# с номерами телефонов в консоль. 
#=========================================================
@input_error
def func_show_all(*args)->str:
    if len(book.data) == 0: 
        return "The database is empty"
    else: 
        table = Table(box=box.DOUBLE)
        table.add_column("Name", justify="center", style="cyan", no_wrap=True)
        table.add_column("Birthday", justify="center", style="yellow", no_wrap=True)
        table.add_column("Phone number", justify="center", style="green", no_wrap=True)
        table.add_column("Email", justify="center", style="red", no_wrap=True)
        table.add_column("Address", justify="center", style="red", no_wrap=True)
        
        console = Console()
        result = [table.add_row(str(record.name.value), str(record.birthday), str(', '.join(map(lambda phone: phone.value, record.phones))), 
            str(record.email), str(record.address)) for record in book.data.values()]        
        console.print(table)
        return ""
        
        # старий варіант друку таблиці
        # result = ""
        # result = "\n".join([f"{n}|{record.birthday.value}|{', '.join(map(lambda phone: phone.value, record.phones))}" for n, record in book.data.items()])
        # if result == "": return "The database is empty"
        # else: return result
    

#=========================================================
# >> show book /N
# Команда "show book" друкує книгу контактів по N записів
# де N - це кількість записів на одній сторінці
#=========================================================
@input_error
def func_book_pages(*args):
    # Итерируемся по адресной книге и выводим представление для каждой записи
    n = int(re.sub("\D", "", args[0]))
    n_page = 0
    for batch in book._record_generator(N=n):
        n_page += 1
        print(f"{'='*14} Page # [bold red]{n_page}[/bold red] {'='*16}")
        for record in batch:
            print("\n".join([f"{record.name.value}|{record.birthday.value}|{', '.join(map(lambda phone: phone.value, record.phones))}"]))
        print("="*40)    
        print("Press [bold red]Enter [/bold red]", end="")
        input("to continue next page...")
    return f"End of the book" 


#=========================================================
# >> change phone... Done
# По этой команде бот сохраняет в памяти новый номер телефона 
# для существующего контакта. 
# Вместо [...] пользователь вводит [Ім'я] [старий Номер телефона] [Новий номер], 
# Увага: обязательно через пробел!!!
# >> change phone Mike +38099 +38050777
#=========================================================
@input_error 
def func_change_phone(*args):
    # порахуємо кількість параметрів
    count_prm = len(args)

    if (count_prm >= 3):
        name = args[0].capitalize()

        if name in book.keys():
            if args[1].isdigit() and args[2].isdigit():   # old_phone = None
                return book[name].edit_phone(Phone(args[1]), Phone(args[2]))
        else:
            return f"The record {name} wasn't found in the database - [bold red]fail[/bold red]"
    else: 
        return f"Expected 3 arguments, but {count_prm} was given.\nHer's an example >> change phone Mike +0449587612 +380995437856"


#=========================================================
# >> "good bye", "close", "exit"
# По любой из этих команд бот завершает свою роботу 
# после того, как выведет в консоль "Good bye!".
#=========================================================
@input_error
def func_exit(*args):
    book.save_database(path_book)
    #note_book.save_data(path_note)
    print("Good bye!")
    exit(0)
    return ""


#=========================================================
# >> hello
# Отвечает в консоль "How can I help you?"
#=========================================================
@input_error
def func_hello(*args):
    return "How can I help you?"


@input_error
def no_command(*args):
    print("Unknown command")
    return func_hello(args=args)

#=========================================================
# >> phone ... Done
# По этой команде бот выводит в консоль номер телефона для указанного контакта.
# Вместо ... пользователь вводит Имя контакта, чей номер нужно показать.
# >> phone Ben
#=========================================================
@input_error
def func_phone(*args):

    if len(args) == 1:
        name = args[0].capitalize()
        if name in book.keys():
            return str(book[name])
            #return ", ".join([phone.value for phone in book[name].phones])
        else:
            return f"The {name} isn't in the database"
    else:
        return f'Missed "Name" of the person'
    

#=========================================================
# >> add phone    Done
# функція розширює новіми телефонами існуючий запис особи Mike   
# >> add phone Mike +380509998877 +380732225566
#=========================================================
# не надо добавлять запятую
@input_error
def func_add_phone(*args):
    print("func_add_phone")
    if (len(args) >= 2):
        name = args[0].capitalize()
        if name in book.keys():
            phones = args[1:]  
            return book[name].add_phone([Phone(phone) for phone in phones])
        else:
            return f"The person [bold red]{name}[/bold red] isn't in a database"
    else: return f"Expected 2 arguments\nHer's an example >> add phone Mike +380509998877"


#=========================================================
# >> change birthday    Done
# функція змінює день народження для особи    
# Example >> change birthday Mike 12.05.1990
#=========================================================
@input_error
def func_change_birthday(*args):
    if (len(args) == 2):
        name = args[0].capitalize()
        if name in book.keys():
            return book[name].edit_birthday(Birthday(args[1]))
        else: return f"The [bold red]{name}[/bold red] isn't in a database"
    else: return f"Expected 2 arguments\nHer's an example >> change birthday Mike 12.05.1990"

@input_error
def func_change_email(*args):
    if (len(args) == 2):
        name = args[0].capitalize()
        if name in book.keys():
            print(args[1])
            return book[name].edit_email(Email(args[1]))
        else: return f"The [bold red]{name}[/bold red] isn't in a database"
    else: return f"Expected 2 arguments\nHer's an example >> change birthday Mike 12.05.1990"

@input_error
def func_change_address(*args):
    if (len(args) == 2):
        name = args[0].capitalize()
        if name in book.keys():
            return book[name].edit_address(Address(args[1]))
        else: return f"The [bold red]{name}[/bold red] isn't in a database"
    else: return f"Expected 2 arguments\nHer's an example >> change birthday Mike 12.05.1990"

#=========================================================
# >> birthday    Done
# функція повертає кількість днів до Дня Народження особи    
# Example >> birthday Mike
# Example >> birthday /365
#=========================================================
# виводити список контактів, у яких день народження через задану кількість днів від поточної дати
@input_error
def func_get_birthday(*args):
    if (len(args) == 1):
        count_day = int(args[0])
        return book.get_list_birthday(count_day)

#=========================================================
# >> del phone    Done
# функція видаляє телефон або список телефонів в існуючому записі особи Mike   
# >> del phone Mike +380509998877 +380732225566
#=========================================================  
# Не надо добавлять запятую в конце каждого номера 
@input_error 
def func_del_phone(*args):
    if (len(args) == 2):
        name = args[0].capitalize()
        if name in book.keys():
            # формуємо список  об'єктів Phone, тому що на майбутнє хочу реалізувати видалення декількох телефонів 
            #lst_del_phones = list(map(lambda phone: Phone(phone), args)) 
            return book[name].del_phone(Phone(args[1]))
        else:
            return f"The name {name} isn't in database - [bold red]fail[/bold red]"
    else: return f"Expected 2 arguments\nHer's an example >> del phone Mike +380509998877"

@input_error 
def func_del_user(*args):
    if (len(args) == 1):
        name = args[0].capitalize()
        if name in book.keys():
            del book[name]
            return f"{name} is deleted from the contact book"
        else:
            return f"The name {name} isn't in database - [bold red]fail[/bold red]"
    else: return f"Expected 1 arguments\n"

@input_error 
def func_del_birthday(*args):
    if (len(args) == 1):
        name = args[0].capitalize()
        if name in book.keys():
            return book[name].edit_birthday(Birthday(None))
        else:
            return f"The name {name} isn't in database - [bold red]fail[/bold red]"
    else: return f"Expected 1 arguments"

@input_error 
def func_del_email(*args):
    if (len(args) == 1):
        name = args[0].capitalize()
        if name in book.keys():
            return book[name].edit_email(Email(None))
        else:
            return f"The name {name} isn't in database - [bold red]fail[/bold red]"
    else: return f"Expected 1 arguments"

@input_error 
def func_del_address(*args):
    if (len(args) == 1):
        name = args[0].capitalize()
        if name in book.keys():
            return book[name].edit_address(Address(None))
        else:
            return f"The name {name} isn't in database - [bold red]fail[/bold red]"
    else: return f"Expected 1 arguments"

#=========================================================
# >> search    Done
# функція виконує пошук інформації у довідковій книзі
#              example >> search Mike
#                      >> search 38073
#                      >> search none
#=========================================================
@input_error
def func_search(*args):
    lst_result = []
    rec_str = ""
    if (len(args) == 1):
        for rec in book.values():
            rec_str = str(rec)
            if args[0].lower() in rec_str.lower():
                lst_result.append(rec_str)
                
        s = "\n".join([rec for rec in lst_result])
        if lst_result: return f"[bold green]Search results:[/bold green]\n{s}"
        else: return f"No matches found for {args[0]}"
    else: return f"Expected 1 arguments, but {len(args)} was given.\nHer's an example >> search Mike"
    
    
# =========================================================
# >> sort    Done
# функція викликає модул cleanfolder виконує сортування файлів у вказаній папці
#              example >> sort Testfolder
#                      >> sort C://Testfolder/testfolder
#                      >> sort .Testfolder/testfolder
# =========================================================
# TODO: sort_main("")
@input_error
def func_sort(*args):
    if len(args) == 1:
        return sort_main(args[0])
    elif len(args) == 0:
        return sort_main("")
    else:
        return f"[bold yellow]Enter path[/bold yellow]"


@input_error
def func_help(*args):
    return """[bold red]cls[/bold red] - очищення екрану від інформації
[bold red]hello[/bold red] - вітання
[bold red]good bye, close, exit[/bold red] - завершення програми
[bold red]load[/bold red] - завантаження інформації про користувачів із файлу
[bold red]save[/bold red] - збереження інформації про користувачів у файл
[bold red]show all[/bold red] - друкування всієї наявної інформації про користувачів
[bold red]show book /N[/bold red]  - друкування інформації посторінково, де [bold red]N[/bold red] - кількість записів на 1 сторінку
[bold red]add[/bold red] - додавання користувача до бази даних. 
      example >> [bold blue]add Mike 02.10.1990 +380504995876[/bold blue]
              >> [bold blue]add Mike None +380504995876[/bold blue]
              >> [bold blue]add Mike None None[/bold blue]
[bold red]phone[/bold red] - повертає перелік телефонів для особи
      example >> [bold blue]phone Mike[/bold blue]
[bold red]add phone[/bold red] - додавання телефону для користувача
      example >> [bold blue]add phone Mike +380504995876[/bold blue]
[bold red]change phone[/bold red] - зміна номеру телефону для користувача
      Формат запису телефону: [bold green]+38ХХХ ХХХ ХХ ХХ[/bold green]
      example >> [bold blue]change phone Mike +380504995876 +380665554433[/bold blue]
[bold red]del phone[/bold red] - видаляє телефон для особи. Дозволяється видаляти одразу декілька телефонів.
      example >> [bold blue]del phone Mike +380509998877, +380732225566[/bold blue]
[bold red]birthday[/bold red] - повертає кількість днів до Дня народження
      example >> [bold blue]birthday Mike[/bold blue]
[bold red]change birthday[/bold red] - змінює/додає Дату народження для особи
      example >> [bold blue]change birthday Mike 02.03.1990[/bold blue]
[bold red]search[/bold red] - виконує пошук інформації по довідковій книзі
      example >> [bold blue]search Mike[/bold blue]
[bold red]note add[/bold red] - додає нотатку з тегом у записник нотаток
      example >> [bold blue]note add My first note Note[/bold blue]
[bold red]note del[/bold red] - видаляє нотатку за ключем із записника нотаток
      example >> [bold blue]note del 1691245959.0[/bold blue]
[bold red]note change[/bold red] - змінює нотатку з тегом за ключем у записнику нотаток
      example >> [bold blue]note change 1691245959.0 My first note Note[/bold blue]
[bold red]note find[/bold red] - здійснює пошук за фрагментом у записнику нотаток
      example >> [bold blue]note find name[/bold blue]
[bold red]note show[/bold red] - здійснює посторінковий вивід всіх нотаток
      example >> [bold blue]note show /10[/bold blue]
[bold red]note sort[/bold red] - здійснює сортування записів нотаток за тегами
      example >> [bold blue]note sort /10[/bold blue]      
[bold red]sort[/bold red] - виконує сортування файлів в указаній папці
      example >> [bold blue]sort folder_name[/bold blue]
"""
    
@input_error
def clear_screen(*args):
    os_name = platform.system().lower()
    
    if os_name == 'windows':
        os.system('cls')
    elif os_name == 'linux' or os_name == 'darwin':
        os.system('clear')
    return ""


COMMANDS = {
    func_exit: ("exit", "end", "bye",),
    func_hello: ("hello", "hy", "welcome",),
    func_new_rec: ("user+", "add+", "add-user", "new", ),
    func_del_user: ("user-", "del-user", "delete-user", ),
    func_phone: ("phone",),
    func_show_all: ("show-all", "show_all", "showall"),
    func_add_phone: ("add-phone", "add_phone",),
    func_del_phone: ("del-phone", "del_phone"),
    func_del_birthday: ("del-birthday", "del_birthday"),
    func_del_email: ("del-email", "del_email"),
    func_del_address: ("del-address", "del_address"),
    func_change_phone: ("edit-phone", "change-phone", "change_phone"),
    func_book_pages: ("show-book", "show_book", "showbook"),
    func_change_birthday: ("edit-birthday", "edit_birthday"),
    func_change_email: ("edit-email", "edit_email"),
    func_change_address: ("edit-address", "edit_address"),
    func_get_birthday: ("birthday",),
    func_help: ("help", "?",),
    func_search: ("search", "find", "seek"),
    func_sort: ("sort",),
}

COMMANDS_NOTES = {
    note_add: ("note+", "note_add", "note-add", ),
    note_del: ("note_del", "note-del",),
    note_change: ("note_change", "note-change",),
    note_find: ("note_find", "note-find",),
    note_show: ("note_show", "note-show", "noteshow",),
    #note_sort: ("note_sort", "note-sort",), 
    add_tags: ("tags+", "add_tags", "add-tags",),
    del_tags: ("tags-", "del_tags", "del-tags",),
    #tag_show: ("tag-show", "tag_show",),
    notebook_show: ("notebook",),
}

################################################################
# implementation autocomplete function
def complete(text, state):
    results = []
    if len(text) > 0:
        for cmd, kwds in COMMANDS.items():
            for kwd in kwds:
                if kwd.lower().startswith(text):
                    results.append(kwd)
        for cmd, kwds in COMMANDS_NOTES.items():
            for kwd in kwds:
                if kwd.lower().startswith(text):
                    results.append(kwd)
    results.append(None)
    return results[state]
################################################################
# set and bind autocomplete function 
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)
################################################################

def parser(text: str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data

    for cmd, kwds in COMMANDS_NOTES.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                user_text = text[len(kwd):].lstrip()
                if len(user_text) == 0: user_text = None
                return cmd, [user_text]

    return no_command, None
################################################################
def main():
    print("[white]Run >> [/white][bold red]help[/bold red] - list of the commands")
    global path_book
    book.load_database(path_book)

    while True:
        user_input = input(">>>")
        command, args = parser(user_input)
        if args != None:
            result = command(*args)
        else:
            result = command()
        
        if result: print(result)
################################################################
if __name__ == "__main__":
    main()
