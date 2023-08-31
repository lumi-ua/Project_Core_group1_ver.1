
from view import AbstractView
from contact_book import AddressBook, Record, Name, Phone, Email, Birthday, Address
from note_book import NoteBook


class Console_View(AbstractView):

   # вывод в консоль ноут-буки
   def show_note_book(self, note_book: NoteBook):
      if len(note_book.data) == 0:
         print("The database is empty")
      else:
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
hello - стартове вітання
exit - завершення програми
showall - друкування всієї наявної інформації про всіх користувачів
userbook N - друкування інформації посторінково, де N - кількість записів на 1 сторінку
      example >> userbook 10
user+ - додавання нової особи до книги контактів
      example >> user+ Mike 01.01.1990 380123456789 112233445566
      example >> user+ Mike 112233445566 380123456789
user- - видалення запису вказаної особи з книги контактів
      example >> user- Mike
rename - перейменування запису вказаної особи 
      example >> rename OldName NewName
showuser - виводить повну інформацію про вказану особу
      example >> showuser Mike
phone+ - додавання нового номеру телефона для вказаної особи
      example >> phone+ Mike 380123456789
phone* - зміна номеру телефону для вказаної особи (вказати старий номер та новий номер)
      example >> phone* Mike 380123456789 112233445566
phone- - видаляє телефон для вказаної особи
      example >> phone- Mike 380123456789
birthday - виводить список контактів, у яких день народження через задану кількість днів від поточної дати
      example >> birthday 5
edit-birthday - змінює/додає Дату народження для вказаної особи
      example >> edit-birthday Mike 01.01.1990
edit-email - змінює/додає електронну адресу для вказаної особи
      example >> edit-email Mike user@mail.com
edit-address - змінює/додає географічну адресу для вказаної особи
      example >> edit-address Mike geo-address
user? - виконує пошук контактів за текстом по довідковій книзі
      example >> user? Mike
      example >> user? 3809
note+ - додає нотатку в записник нотаток
      example >> note+ My first note text
note- - видаляє нотатку із записника нотаток за вказаним ID нотатки
      example >> note- 1
note* - змінює текст нотатки за вказаним ID нотатки
      example >> note* 1 My first note text
note? - здійснює пошук нотаток за текстом
      example >> note? text_in_note
note# - здійснює пошук та сортування нотаток з текстом у ключових словах (використовується пейджинація)
      example >> note# text_in_tag
tag+ - додає нові теги до нотатки за вказаним ID нотатки
      example >> tag+ 1 tag0 tag1 tag2
tag- - видаляє теги нотатки за вказаним ID нотатки. Якщо тег не вказаний, то видаляються всі теги вказаної нотатки
      example >> tag- 1 tag0 tag1 tag2
      example >> tag- 1
showtag - виводить всі нотатки, в яких є заданий тег
      example >> showtag mytag
shownote - виводить вміст нотатки за вказаним ID нотатки
      example >> shownote 1
notebook - виводить вміст всіх нотаток записника нотаток
      example >> notebook
sort - виконує сортування файлів в указаній папці
      example >> sort folder_name
help - справочна інформація по всім командам""")
