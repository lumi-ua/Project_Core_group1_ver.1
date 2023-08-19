
from view import AbstractView
from contact_book import AddressBook, Record, Name, Phone, Email, Birthday, Address, PhoneException, BirthdayException, EmailException
from note_book import NoteBook


class Console_View(AbstractView):

   # вывод в консоль ноут-буки
   def show_note_book(self, note_book: NoteBook):
      for note in note_book.data.values():
         print(f"[{(len(note.tags))}] {note.key}: " + note.value)
      for tag in note_book.tags.values():
         print("[" + str(tag.sz()) + "]#" + tag.value)

   # вывод в консоль контакт-буки
   def show_contact_book(self, contact_book: AddressBook):
      if len(contact_book.data) == 0: 
         print("The database is empty")
      else:
         for rec in contact_book.values(): print(rec)

   # вывод в консоль хэлпа
   def show_help(self):
      print("""cls - очищення екрану від інформації
hello - вітання
good bye, close, exit - завершення програми
showall - друкування всієї наявної інформації про користувачів
show book /N  - друкування інформації посторінково, де N - кількість записів на 1 сторінку
add - додавання користувача до бази даних. 
      example >> add Mike 02.10.1990 +380504995876
            >> add Mike +380504995876
            >> add Mike
phone - повертає перелік телефонів для особи
      example >> phone Mike
add phone - додавання телефону для користувача
      example >> add phone Mike +380504995876
change phone - зміна номеру телефону для користувача
      Формат запису телефону: +38ХХХ ХХХ ХХ ХХ
      example >> change phone Mike +380504995876 +380665554433
del phone - видаляє телефон для особи. Дозволяється видаляти одразу декілька телефонів.
      example >> del phone Mike +380509998877, +380732225566
birthday - повертає кількість днів до Дня народження
      example >> birthday Mike
change birthday - змінює/додає Дату народження для особи
      example >> change birthday Mike 02.03.1990
search - виконує пошук інформації по довідковій книзі
      example >> search Mike
note add - додає нотатку з тегом у записник нотаток
      example >> note add My first note Note
note del - видаляє нотатку за ключем із записника нотаток
      example >> note del 1691245959.0
note change - змінює нотатку з тегом за ключем у записнику нотаток
      example >> note change 1691245959.0 My first note Note
note find - здійснює пошук за фрагментом у записнику нотаток
      example >> note find name
note show - здійснює посторінковий вивід всіх нотаток
      example >> note show /10
note sort - здійснює сортування записів нотаток за тегами
      example >> note sort /10    
sort - виконує сортування файлів в указаній папці
      example >> sort folder_name
""")
