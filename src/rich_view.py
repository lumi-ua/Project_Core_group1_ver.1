
from view import AbstractView
from contact_book import AddressBook, Record, Name, Phone, Email, Birthday, Address
from note_book import NoteBook

from rich import print
from rich import box
from rich.table import Table
from rich.console import Console


class Rich_View(AbstractView):

   # вывод в консоль ноут-буки
   def show_note_book(self, note_book: NoteBook):
      if len(note_book.data) == 0: 
         print("The database is empty")
      else:
         table = Table(box=box.DOUBLE)
         table.add_column("ID", justify="left", no_wrap=True)
         table.add_column("Note", justify="center", style="cyan", no_wrap=True)
         table.add_column("Tags", justify="center", style="blue", no_wrap=True)
         console = Console()
         result = [table.add_row(
               note.key,
               str(note.value), 
               str("---") if len(note.tags) == 0 else " ".join(["#" + tag for tag in note.tags])
            ) for note in note_book.data.values()]
         console.print(table)

   # вывод в консоль контакт-буки
   def show_contact_book(self, contact_book: AddressBook):
      if len(contact_book.data) == 0:
         print("The database is empty")
      else: 
         table = Table(box=box.DOUBLE)
         table.add_column("Name", justify="center", style="cyan", no_wrap=True)
         table.add_column("Birthday", justify="center", style="yellow", no_wrap=True)
         table.add_column("Phone number", justify="center", style="green", no_wrap=True)
         table.add_column("Email", justify="center", style="red", no_wrap=True)
         table.add_column("Address", justify="center", style="red", no_wrap=True)
         
         console = Console()
         result = [table.add_row(
               str(record.name),
               str(record.birthday if record.birthday else "---"),
               str(', '.join(map(lambda phone: phone.value, record.phones))),
               str(record.email    if record.email    else "---"),
               str(record.address  if record.address  else "---")
            ) for record in contact_book.data.values()]
         console.print(table)

   # вывод в консоль хэлпа
   def show_help(self):
         print("""[bold red]cls[/bold red] - очищення екрану від інформації
[bold red]hello[/bold red] - стартове вітання
[bold red]exit[/bold red] - завершення програми
[bold red]showall[/bold red] - друкування всієї наявної інформації про всіх користувачів
[bold red]userbook N[/bold red] - друкування інформації посторінково, де [bold red]N[/bold red] - кількість записів на 1 сторінку
      example >> [bold blue]userbook 10[/bold blue]
[bold red]user+[/bold red] - додавання нової особи до книги контактів
      example >> [bold blue]user+ Mike 01.01.1990 380123456789 112233445566[/bold blue]
      example >> [bold blue]user+ Mike 112233445566 380123456789[/bold blue]
[bold red]user-[/bold red] - видалення запису вказаної особи з книги контактів
      example >> [bold blue]user- Mike[/bold blue]
[bold red]rename[/bold red] - перейменування запису вказаної особи 
      example >> [bold blue]rename OldName NewName[/bold blue]
[bold red]showuser[/bold red] - виводить повну інформацію про вказану особу
      example >> [bold blue]showuser Mike[/bold blue]
[bold red]phone+[/bold red] - додавання нового номеру телефона для вказаної особи
      example >> [bold blue]phone+ Mike 380123456789[/bold blue]
[bold red]phone*[/bold red] - зміна номеру телефону для вказаної особи (вказати старий номер та новий номер)
      example >> [bold blue]phone* Mike 380123456789 112233445566[/bold blue]
[bold red]phone-[/bold red] - видаляє телефон для вказаної особи
      example >> [bold blue]phone- Mike 380123456789[/bold blue]
[bold red]birthday[/bold red] - виводить список контактів, у яких день народження через задану кількість днів від поточної дати
      example >> [bold blue]birthday 5[/bold blue]
[bold red]edit-birthday[/bold red] - змінює/додає Дату народження для вказаної особи
      example >> [bold blue]edit-birthday Mike 01.01.1990[/bold blue]
[bold red]edit-email[/bold red] - змінює/додає електронну адресу для вказаної особи
      example >> [bold blue]edit-email Mike user@mail.com[/bold blue]
[bold red]edit-address[/bold red] - змінює/додає географічну адресу для вказаної особи
      example >> [bold blue]edit-address Mike geo-address[/bold blue]
[bold red]user?[/bold red] - виконує пошук контактів за текстом по довідковій книзі
      example >> [bold blue]user? Mike[/bold blue]
      example >> [bold blue]user? 3809[/bold blue]
[bold red]note+[/bold red] - додає нотатку в записник нотаток
      example >> [bold blue]note+ My first note text[/bold blue]
[bold red]note-[/bold red] - видаляє нотатку із записника нотаток за вказаним ID нотатки
      example >> [bold blue]note- 1[/bold blue]
[bold red]note*[/bold red] - змінює текст нотатки за вказаним ID нотатки
      example >> [bold blue]note* 1 My first note text[/bold blue]
[bold red]note?[/bold red] - здійснює пошук нотаток за текстом
      example >> [bold blue]note? text_in_note[/bold blue]
[bold red]note#[/bold red] - здійснює пошук та сортування нотаток з текстом у ключових словах (використовується пейджинація)
      example >> [bold blue]note# text_in_tag[/bold blue]
[bold red]tag+[/bold red] - додає нові теги до нотатки за вказаним ID нотатки
      example >> [bold blue]tag+ 1 tag0 tag1 tag2[/bold blue]
[bold red]tag-[/bold red] - видаляє теги нотатки за вказаним ID нотатки. Якщо тег не вказаний, то видаляються всі теги вказаної нотатки
      example >> [bold blue]tag- 1 tag0 tag1 tag2[/bold blue]
      example >> [bold blue]tag- 1[/bold blue]
[bold red]showtag[/bold red] - виводить всі нотатки, в яких є заданий тег
      example >> [bold blue]showtag mytag[/bold blue]
[bold red]shownote[/bold red] - виводить вміст нотатки за вказаним ID нотатки
      example >> [bold blue]shownote 1[/bold blue]
[bold red]notebook[/bold red] - виводить вміст всіх нотаток записника нотаток
      example >> [bold blue]notebook[/bold blue]
[bold red]sort[/bold red] - виконує сортування файлів в указаній папці
      example >> [bold blue]sort folder_name[/bold blue]
[bold red]help[/bold red] - справочна інформація по всім командам""")

