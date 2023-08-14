
from pathlib import Path
import os, sys
import platform  # для clearscrean()
from contact_book import AddressBook, Record, Name, Phone, Email, Birthday, Address, PhoneException, BirthdayException, EmailException
from clean import sort_main
from note_book import NoteBook
import re
import readline

from rich import print
from rich import box
from rich.table import Table
from rich.console import Console

path_book = Path(sys.path[0]).joinpath("user_book.bin")
path_note = Path(sys.path[0]).joinpath("note_book.bin")

book = AddressBook()
note_book = NoteBook()

class ArgsAmountException(Exception):
   """Wrong arguments amount exception"""
        
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
        except ArgsAmountException as e:
            print(e)
        except FileNotFoundError:    # Файл бази даних Відсутній
            print("The database isn't found")
        except ValueError:
            print("Incorect data or unsupported format for file")
        except KeyError:
            print("Record isn't in the database")
        except KeyboardInterrupt:
            func_exit(args)
        except TypeError:
            print("Incorect data")
        return result
    return wrapper

#=========================================================
# >> note+ My first note in this bot.
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
    else: raise ArgsAmountException("Wrong arguments amount. Expected > 1 params")

#=========================================================
# >> tags- <key>
# >> tags- <key> <tag> ...
#=========================================================
@input_error
def del_tags(args: str):
    params = args.strip().split()
    if len(params) >= 1:
        note_id = params[0]
        tags_list = params[1:] if len(params) > 1 else None
        return note_book.del_tags(note_id, tags_list)
    else: return ""

#=========================================================
# >> note-del <key>
#=========================================================
@input_error
def note_del(args):
    params = args.strip().split()
    if len(params) == 1:
        return note_book.del_note(params[0])
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 argument")

#=========================================================
# >> note-change <key> <Text>
#=========================================================
@input_error
def note_change(args):
    args = args.lstrip()
    n = args.find(" ")
    if n > 0:
        key = args[:n]
        if key.isdigit():
            note_text = args[n+1:]
            return note_book.change_note(key, note_text)
        else: raise TypeError("Note.key wrong type")
    else: raise ArgsAmountException("Unknown argument error")


#=========================================================
# >> note-find <text-fragment>
#=========================================================
@input_error
def notes_find(args):
    key_list = note_book.find_notes(args.strip())
    if key_list:
        return f"Search result in notes: {str(key_list)}"
    else:
        return f"No one notes was found for fragment: '{args}'"


#=========================================================
# >> note-show <int: необов'язковий аргумент кількості рядків>
# example >> note show 15
#=========================================================
@input_error
def note_show(args):
    params = args.strip().split()
    if len(params) == 1:
        note_key = params[0]
        return str(note_book.data[note_key])
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 argument")

@input_error
def tag_show(args):
    params = args.strip().split()
    if len(params) == 1:
        tag_key = params[0]
        notes_list = note_book.get_tag_notes(tag_key)
        for n in notes_list: print(n)
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 argument")
    return ""

#=========================================================
# >> n-search <text>
# пошук та сортування нотаток за ключовими словами
#=========================================================
@input_error
def notes_tag_search(args):
    search_text = args.strip()
    result = note_book.search_notes_by_text_tags(search_text)

    if len(result) > 0: print("="*40)
    count = 0
    for item in result:
        print(item)
        print("="*40)
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
# Создаёт новый контакт
# example >> add Mike 02.10.1990 +380504995876
#=========================================================
@input_error
def func_new_user(*args):
    count_prm = len(args)
    if (count_prm >= 2):
        if not args[0].capitalize() in book.keys():
            name = args[0]
            new_name = Name(args[0].capitalize())
           
            new_birthday = Birthday(args[1])
            if new_birthday.value == None:
                args = args[1:]
                new_birthday = None
            else:
                args = args[2:]
     
            if len(args) > 0:
                lst_phones = list(map(lambda phone: Phone(phone.strip()), args))
                rec = Record(name=new_name, birthday=new_birthday, phones=lst_phones)
                book.add_record(rec)
            else: raise PhoneException("Phone absent in arguments")
            
            return "1 record was successfully added - [bold green]success[/bold green]"
        else: return "The person is already in database"
    else: return "Wrong arguments amount. Expected 3 arguments"
     

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
        result = [table.add_row(
            str(record.name.value), 
            str(record.birthday.value if record.birthday else "---"), 
            str(', '.join(map(lambda phone: phone.value, record.phones))), 
            str(record.email.value    if record.email    else "---"), 
            str(record.address.value  if record.address  else "---")
                ) for record in book.data.values()]        
        console.print(table)
        return ""

#=========================================================
# >> show-book /N
# Команда "show-book" друкує книгу контактів по N записів
# де N - це кількість записів на одній сторінці
#=========================================================
@input_error
def func_book_pages(*args):
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
# Изменяет номер телефона
# >> change-phone Mike +38099 +38050777
#=========================================================
@input_error 
def func_change_phone(*args):
    if (len(args) == 3):
        name = args[0].capitalize()
        return book[name].edit_phone(Phone(args[1]), Phone(args[2]))
    else: raise ArgsAmountException("Wrong arguments amount. Expected 3 arguments")


@input_error
def func_exit(*args):
    book.save_database(path_book)
    note_book.save_to_file(path_note)
    print("Good bye!")
    exit(0)
    return ""

@input_error
def func_hello(*args):
    return "How can I help you?"

@input_error
def no_command(*args):
    print("Unknown command")
    return func_hello(args=args)

#=========================================================
# Выводит в консоль номера телефонов для указанного контакта.
# >> phone Ben
#=========================================================
@input_error
def func_phone(*args):
    if len(args) == 1:
        name = args[0].capitalize()
        return str(book[name])
    else: raise ArgsAmountException('Wrong arguments amount. Missed "Name" of the person')


#=========================================================
# функція розширює новіми телефонами існуючий запис особи Mike   
# >> add-phone Mike +380509998877 +380732225566
#=========================================================
@input_error
def func_add_phone(*args):
    if (len(args) >= 2):
        name = args[0].capitalize()
        phones = args[1:]  
        return book[name].add_phone([Phone(phone) for phone in phones])
    else: raise ArgsAmountException("Wrong arguments amount. Expected 2 arguments")


#=========================================================
# функція змінює день народження для особи    
# Example >> change-birthday Mike 12.05.1990
#=========================================================
@input_error
def func_change_birthday(*args):
    if (len(args) == 2):
        name = args[0].capitalize()
        return book[name].edit_birthday(Birthday(args[1]))
    else: raise ArgsAmountException("Wrong arguments amount. Expected 2 arguments")

@input_error
def func_change_email(*args):
    if (len(args) == 2):
        name = args[0].capitalize()
        return book[name].edit_email(Email(args[1]))
    else: raise ArgsAmountException("Wrong arguments amount. Expected 2 arguments")

@input_error
def func_change_address(*args):
    if (len(args) == 2):
        name = args[0].capitalize()
        return book[name].edit_address(Address(args[1]))
    else: raise ArgsAmountException("Wrong arguments amount. Expected 2 arguments")

#=========================================================
# повертає список контактів, у яких день народження через задану кількість днів від поточної дати   
# Example >> birthday 5
#=========================================================
@input_error
def func_list_birthday(*args):
    count_day = 0
    if (len(args) == 1):
        count_day = int(args[0])
    return book.get_list_birthday(count_day)

#=========================================================
# видаляє телефон або список телефонів в існуючому записі особи Mike   
# >> del phone Mike +380509998877 +380732225566
#=========================================================  
@input_error 
def func_del_phone(*args):
    if (len(args) == 2):
        name = args[0].capitalize()
        # формуємо список  об'єктів Phone, тому що на майбутнє хочу реалізувати видалення декількох телефонів 
        #lst_del_phones = list(map(lambda phone: Phone(phone), args)) 
        return book[name].del_phone(Phone(args[1]))
    else: raise ArgsAmountException("Wrong arguments amount. Expected 2 arguments")

@input_error 
def func_rename_user(*args):
    if (len(args) == 2):
        return book.rename_record(args[0].capitalize(), args[1].capitalize())
    else: raise ArgsAmountException("Wrong arguments amount. Expected 2 arguments")

@input_error 
def func_del_user(*args):
    if (len(args) == 1):
        name = args[0].capitalize()
        del book[name]
        return f"{name} is deleted from the contact book"
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 arguments")

@input_error 
def func_del_birthday(*args):
    if (len(args) == 1):
        name = args[0].capitalize()
        return book[name].edit_birthday(Birthday(None))
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 arguments")

@input_error 
def func_del_email(*args):
    if (len(args) == 1):
        name = args[0].capitalize()
        return book[name].edit_email(Email(None))
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 arguments")

@input_error 
def func_del_address(*args):
    if (len(args) == 1):
        name = args[0].capitalize()
        return book[name].edit_address(Address(None))
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 arguments")

#=========================================================
# TODO: tuning
# функція виконує пошук інформації у довідковій книзі
#              example >> search Mike
#                      >> search 38073
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
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 arguments")
    
    
# =========================================================
# сортування файлів у вказаній папці
#              example >> sort Testfolder
#                      >> sort C://Testfolder/testfolder
#                      >> sort .Testfolder/testfolder
# =========================================================
# TODO: sort_main("")
@input_error
def func_sort_files(*args):
    if len(args) == 1:
        return sort_main(args[0])
    elif len(args) == 0:
        return sort_main("")
    else:
        return f"[bold yellow]Enter path[/bold yellow]"


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
    func_new_user: ("user+", "add+", "add-user", "new", ),
    func_rename_user: ("rename",),
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
    func_list_birthday: ("birthday",),
    func_help: ("help", "?",),
    func_search: ("search", "find", "seek"),
    func_sort_files: ("sort",),
}

COMMANDS_NOTES = {
    note_add: ("note+", "note_add", "note-add", ),
    note_del: ("note_del", "note-del",),
    note_change: ("note_change", "note-change",),
    notes_find: ("note_find", "note-find",),
    note_show: ("note_show", "note-show", "noteshow",),
    notes_tag_search: ("n-search",),
    add_tags: ("tags+", "add_tags", "add-tags",),
    del_tags: ("tags-", "del_tags", "del-tags",),
    tag_show: ("tag-show", "tag_show",),
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
    global path_note
    book.load_database(path_book)
    note_book.load_file(path_note)

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
