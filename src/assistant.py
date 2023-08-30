
from pathlib import Path
import os, sys
import re
import platform  # для clearscrean()
from contact_book import AddressBook, Record, Name, Phone, Email, Birthday, Address, PhoneException, BirthdayException, EmailException
from clean import sort_main
from note_book import NoteBook
from console_view import Console_View
from rich_view import Rich_View
import readline

path_book = Path(sys.path[0]).joinpath("user_book.bin")
path_note = Path(sys.path[0]).joinpath("note_book.bin")

view = Rich_View()
book = AddressBook()
note_book = NoteBook()

class ArgsAmountException(Exception):
   """Wrong arguments amount exception"""

def input_error(func):
    def wrapper(*args):
        result = None
        try:
            result = func(*args)
        except BirthdayException as e:
            print(e)
        except PhoneException as e:
            print(e)
        except EmailException as e:
            print(e)
        except ArgsAmountException as e:
            print(e)
        except FileNotFoundError:
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
# >> note+ My first text of note
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
# >> note- <key>
#=========================================================
@input_error
def note_del(args):
    params = args.strip().split()
    if len(params) == 1:
        return note_book.del_note(params[0])
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 argument")

#=========================================================
# >> note* <key> <Text>
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
# >> shownote <key>
#=========================================================
@input_error
def show_note(args):
    params = args.strip().split()
    if len(params) == 1:
        note_key = params[0]
        print(note_book.data[note_key])
        return ""
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 argument")

#=========================================================
# >> showtag <tag>
#=========================================================
@input_error
def show_tag(args):
    params = args.strip().split()
    if len(params) == 1:
        tag_key = params[0]
        notes_list = note_book.get_tag_notes(tag_key)
        for n in notes_list: print(n)
    else: raise ArgsAmountException("Wrong arguments amount. Expected 1 argument")
    return ""

#=========================================================
# >> note? <text>
#=========================================================
@input_error
def notes_search(args):
    notes_list = note_book.find_notes(args.strip())
    if notes_list:
        return f"Search result in notes: \n{str(notes_list)}"
    else:
        return f"No one notes was found for fragment: '{args}'"

#=========================================================
# >> note# <text>
# пошук та сортування нотаток за текстом в ключових словах
#=========================================================
@input_error
def notes_tag_search(args):
    search_text = args.strip()
    notes_list = note_book.search_notes_by_text_tags(search_text)

    if len(notes_list) > 0: print("="*40)
    count = 0
    for item in notes_list:
        print(item)
        print("="*40)
        count += 1
        if count == 5:
            input("\nFor next page press enter\n")
            count = 0
    return ""

#=========================================================
# >> notebook
#=========================================================
@input_error
def show_note_book(args):
    view.show_note_book(note_book=note_book)
    return ""

#=========================================================
# example >> user+ Mike 01.10.1990 +112233445566
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
            
            return "1 record was successfully added"
        else: return "The person is already in database"
    else: raise ArgsAmountException("Wrong arguments amount. Expected 3 arguments")
     
#=========================================================
# >> showall
#=========================================================
@input_error
def show_contact_book(*args):
    view.show_contact_book(contact_book=book)
    return ""

#=========================================================
# >> userbook N
# друкує книгу контактів по N записів, якщо без параметру - то по одному запису
#=========================================================
@input_error
def func_book_pages(*args):
    n = 1
    if (len(args) == 1): n = int(re.sub("\D", "", args[0]))
    n_page = 0
    for batch in book._record_generator(N=n):
        n_page += 1
        print(f"{'='*15} Page #{n_page} {'='*16}")
        for record in batch:
            print(str(record))
        if len(batch) < n: break
        print("="*40)
        print("Press Enter ", end="")
        input("to continue next page...")
    return f"End of the ContactBook" 


#=========================================================
# >> phone* Mike +112233445566 +380123456789
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
    if len(args) > 0: print(*args[0])
    return "How can I help you?"

@input_error
def no_command(*args):
    return func_hello(["Unknown command"])

#=========================================================
# >> showuser <username>
#=========================================================
@input_error
def show_user(*args):
    if len(args) == 1:
        name = args[0].capitalize()
        print(book[name])
        return ""
    else: raise ArgsAmountException('Wrong arguments amount. Missed "Name" of the person')

#========================================================= 
# >> phone+ Mike +380123456789 +112233445566
#=========================================================
@input_error
def func_add_phone(*args):
    if (len(args) >= 2):
        name = args[0].capitalize()
        phones = args[1:]  
        return book[name].add_phone([Phone(phone) for phone in phones])
    else: raise ArgsAmountException("Wrong arguments amount. Expected 2 arguments")

#=========================================================  
# >> edit-birthday Mike 01.01.1990
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
    if (len(args) == 1): count_day = int(args[0])
    user_list = book.get_list_birthday(count_day)
    print(user_list)
    return ""

#=========================================================
# видаляє телефон в існуючому записі особи   
# >> phone- Mike +112233445566
#=========================================================  
@input_error 
def func_del_phone(*args):
    if (len(args) == 2):
        name = args[0].capitalize()
        # формуємо список об'єктів Phone, на майбутнє реалізувати видалення декількох телефонів 
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
# >> search Mike
# >> search 3809
#=========================================================
@input_error
def func_search(*args):
    if (len(args) == 1):
        lst_result = book.search(args[0].strip())
        s = "\n".join([str(rec) for rec in lst_result])
        if lst_result:
            print(f"Search results:")
            print(s)
            return ""
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
        return f"Enter path"

@input_error
def show_help(*args):
    view.show_help()
    return "assistant v.129"

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
    func_new_user: ("user+", "add-user",),
    func_del_user: ("user-", "del-user",),
    func_rename_user: ("rename",),
    func_add_phone: ("phone+", "add-phone", "add_phone",),
    func_del_phone: ("phone-", "del-phone", "del_phone"),
    func_change_phone: ("phone*", "edit-phone", "change-phone",),
    func_del_birthday: ("del-birthday", "del_birthday"),
    func_del_email: ("del-email", "del_email"),
    func_del_address: ("del-address", "del_address"),
    func_book_pages: ("userbook", "showbook"),
    func_change_birthday: ("edit-birthday", "edit_birthday"),
    func_change_email: ("edit-email", "edit_email"),
    func_change_address: ("edit-address", "edit_address"),
    func_list_birthday: ("birthday",),
    func_search: ("user?", "search",),
    func_sort_files: ("sort",),
    show_user: ("showuser",),
    show_contact_book: ("showall", "show-all",),
    show_help: ("help", "?",),
}

COMMANDS_NOTES = {
    note_add:   ("note+",   "add-note",),
    note_del:   ("note-",   "del-note",),
    note_change:("note*",   "edit-note",),
    notes_search: ("note?",  "search-note",),
    notes_tag_search: ("note#",),
    add_tags:   ("tags+",   "add_tags", "add-tags",),
    del_tags:   ("tags-",   "del_tags", "del-tags",),
    show_tag:   ("showtag", "show-tag",),
    show_note:  ("shownote", "show-note",),
    show_note_book: ("notebook",),
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
