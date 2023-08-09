from collections import UserDict
from datetime import datetime
import json
from RecordBook import Field

class Tag(Field):

    def __init__(self, value=None):        
        super().__init__(value)
        self.value = value
        self.notes = set()
        
    def __str__(self):
        result = str(self.value)
        if len(self.notes): result += "\nnote-keys: " + ", ".join([key for key in self.notes])
        return result
    
    def __repr__(self):
        return str(self.value)

    def link(self, note_key: str):
        self.notes.add(note_key)

    def unlink(self, note_key: str):
        self.notes.remove(note_key)

class Note(Field):

    def __init__(self, key: str, value: str):
        super().__init__(value)
        self.value = value
      
        self.key = key
        self.tags = set()

    def __str__(self):
        result = f"{str(self.value)}\nkey: {str(self.key)}"
        if len(self.tags): result += "\n#" + " #".join([tag for tag in self.tags])
        return result
    
    def unlink(self, tag_key: str):
        # удаляет тэг по ключу из списка своих тэгов
        pass

    def link(self, tag_key: str):
        self.tags.add(tag_key)


class NoteBook(UserDict):

    def __init__(self):
        super().__init__()
        self.tags = dict() # dict(tag=str, Tag)
        self.max = 1

    def change_note(self, note_key: str, value: str):
        if note_key in self.data.keys():
            note = self.data[note_key]
            note.value = value   
        #return f"\nDeleted note: {old_note}\nNew note: {new_note}\nNew Tag: {self.tag}\n"


    def add_tags(self, note_key:str, tags_list:list):
        if note_key in self.data.keys():
            note = self.data[note_key]

            for tag_key in tags_list:
                if tag_key not in self.tags.keys():
                    self.tags[tag_key] = Tag(tag_key)
                tag = self.tags[tag_key]
                note.link(tag_key)
                tag.link(note_key)
        return "add_tags: Done"


    def del_tags(self, note_id: str, tags_list: list):
        # TODO:
        pass

    def add_note(self, value: str):
        key = str(self.max)
        self.max += 1
        #str(datetime.now().replace(microsecond=0).timestamp())
        note = Note(key, value)
        self.data[key] = note
        return f"Added new note, key={key}"
    
    def del_note(self, key: str):
        if key in self.data.keys():
            note = self.data.pop(key)
            for tag in note.tags:
                tag.unlink(key)
            return f"\nDeleted Note.key: {note.key}\nNote: {note.value}\nTags: {len(note.tags)}"
        return f"Wrong key={key} to delete Note"
        
    def iterator(self, group_size=15):
        records = list(self.data.values())
        self.current_index = 0

        while self.current_index < len(records):
            group_items = records[self.current_index:self.current_index + group_size]
            group = [rec for rec in group_items]
            self.current_index += group_size
            yield group

    def save_data(self, filename):
        with open(filename, 'w') as f:

            json.dump({str(note.key): (str(note.value  if note.value else ""), str(note.tag if note.tag else "")) for key, note in self.items()}, f, indent=4)

        return f"The note_book is saved."

    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                data_dict = json.load(f)
                for key, value in data_dict.items():                    
                    note, tag = value
                    note = Note(note)
                    tag = Tag(tag)
                    record = NoteRecord(key, note, tag)
                    self.data[record.key] = record

            if isinstance(self.data, dict):
                print(f"The Notebook is loaded.")
                if not len(self.data): 
                    return f"Notebook is empty"
            else:
                print("The file does not contain a valid Notebook.")
        except FileNotFoundError:
            print(f"The file {filename} does not exist")


    def find_note(self, fragment:str):
        count = 0
        result = ""
        for rec in self.values():
            line = str(rec) + "\n"
            if fragment in line.lower():
                result += line
                count += 1
        if result:            
            result = f"\nSearch result {str(count)} records:\nNotes:\n{result}Search string: {fragment}"
        else:
            result = f"No records was found for the fragment '{fragment}' \n"
        return result
    
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