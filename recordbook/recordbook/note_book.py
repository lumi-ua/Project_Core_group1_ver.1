from collections import UserDict
from datetime import datetime
import json
from RecordBook import Field

class Tag(Field):

    def __init__(self, value=None):        
        super().__init__(value)
        self.value = value

        # список ключей тех ноутов, к которым тэг будет привязан
        self.notes = set()
        
    def __str__(self):
        result = str(self.value)
        if len(self.notes): result += "\nnote-keys: " + ", ".join([key for key in self.notes])
        return result
    
    def __repr__(self):
        return str(self.value)

    def sz(self):
        return len(self.notes)

    # добавляем ключ ноута в список ключей, тем самым делая привязку к ноуту 
    def link(self, note_key: str):
        self.notes.add(note_key)

    # удаляем ключ ноута, тем самым удаляем связь к ноуту (отвязываем)
    def unlink(self, note_key: str):
        self.notes.remove(note_key)

class Note(Field):

    def __init__(self, key: str, value: str):
        super().__init__(value)
        self.value = value
        self.key = key

        # список тэгов, к которым будет привязан 
        self.tags = set()

    def __str__(self):
        result = f"{str(self.value)}\nkey: {str(self.key)}"
        if len(self.tags): result += "".join(["\n#" + tag for tag in self.tags])
        return result
    
    def unlink(self, tag_key: str):
        self.tags.remove(tag_key)

    def link(self, tag_key: str):
        self.tags.add(tag_key)


class NoteBook(UserDict):

    def __init__(self):
        super().__init__()
        self.tags = dict() # dict(tag=str, Tag)
        self.max = 0

    def change_note(self, note_key: str, value: str):
        if note_key in self.data.keys():
            note = self.data[note_key]
            note.value = value
            return f"change_note: successfully note.key={note_key}"
        else: return f"change_note: wrong note.key={note_key}"


    def add_tags(self, note_key:str, tags_list:list):
        # проверяем по ключу есть ли такой ноут
        if note_key in self.data.keys():
            note = self.data[note_key]

            for tag_key in tags_list:
                # проверяем есть ли такой ключ в списке уже существующих
                if tag_key not in self.tags.keys():
                    # добавляем новый тэг по строке-ключу
                    self.tags[tag_key] = Tag(tag_key)
                tag = self.tags[tag_key]
                # привязываем к ноуту тэг
                note.link(tag_key)
                # привязываем к тэгу ноут
                tag.link(note_key)
            return f"add_tags: successfully attached tags:{len(tags_list)}"
        else: return f"add_tags: wrong note.key={note_key}"

    def del_tags(self, note_key: str, tags_list: list):
        # проверяем по ключу есть ли такой ноут
        if note_key in self.data.keys():
            note = self.data[note_key]

            if tags_list==None: tags_list = note.tags
            sz = len(tags_list)

            for tag_key in tags_list:
                note.unlink(tag_key)
                tag = self.tags[tag_key]
                tag.unlink(note_key)
                if tag.sz() == 0:
                    self.tags.pop(tag_key)

            return f"del_tags: successfully detached tags:{sz}"
        else: return f"add_tags: wrong note.key={note_key}"


    def create_note(self, value: str):
        self.max += 1
        key = str(self.max)
        note = Note(key, value)
        self.data[key] = note
        return f"Added new note, key={key}"
    
    def del_note(self, note_key: str):
        if note_key in self.data.keys():
            note = self.data.pop(note_key)
            for tag_key in note.tags:
                tag = self.tags[tag_key]
                tag.unlink(note_key)
                if tag.sz() == 0:
                    self.tags.pop(tag_key)
            return f"Deleted Note.key: {note.key}\nNote: {note.value}\nTags: {len(note.tags)}"
        return f"Wrong key={note_key} to delete Note"

    def get_tag_notes(self, tag_key: str):
        if tag_key in self.tags.keys():
            tag = self.tags[tag_key]
            notes_list = []
            for note_key in tag.notes:
                note = self.data[note_key]
                notes_list.append(f"Note[{note.key}]:{note.value}")
            return notes_list
        return []
        
    def iterator(self, group_size=15):
        notes = list(self.data.values())
        self.current_index = 0

        while self.current_index < len(notes):
            group_items = notes[self.current_index:self.current_index + group_size]
            group = [rec for rec in group_items]
            self.current_index += group_size
            yield group

    def find_notes(self, fragment:str):
        result = []
        for note in self.values():
            if note.value.lower().find(fragment.lower()) >= 0:
                result.append(note.key)
        return result

    def save_data(self, filename: str):
        with open(filename, 'w') as f:

            json.dump({
                str(note.key): (
                    str(note.value if note.value else ""),
                    "".join([tag for tag in note.tags])) for key, note in self.items()}, 
                f, indent=4)

        return f"The note_book is saved."

    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                data_dict = json.load(f)
                for key, value in data_dict.items():                    
                    note, tag = value
                    note = Note(note)
                    tag = Tag(tag)
                    self.data[tag.key] = tag

            if isinstance(self.data, dict):
                print(f"The Notebook is loaded.")
                if not len(self.data): 
                    return f"Notebook is empty"
            else:
                print("The file does not contain a valid Notebook.")
        except FileNotFoundError:
            print(f"The file {filename} does not exist")

    
if __name__ == "__main__":

    nb = NoteBook()
    #file_name = "n_book.json"
    #print(nb.load_data(file_name))
    #print(nb) 

    #key=datetime.now().replace(microsecond=0).timestamp()
    #note = Note('Create tag sorting')
    #rec = NoteRecord(key, note, Tag('Project'))
    #nb.add_record(rec)

    #print(nb.find_note('note'))
    #print(nb.save_data(file_name))
    #print(nb)