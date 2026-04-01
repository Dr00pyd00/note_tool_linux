#!/usr/bin/env python3

from typing import List
import argparse
import sqlite3
from pathlib import Path



# =================== class db ================= #

class MyDatabase():
    def __init__(self,db_path):
        self.db_path = db_path

    def connect_to_db(self):
        return sqlite3.connect(self.db_path)
    
    def create_table_if_not_exist(self):
        conn = self.connect_to_db()
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS Notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        conn.close()

    def reset_table(self):
        conn = self.connect_to_db()
        c = conn.cursor()
        c.execute(
            """
            DROP TABLE IF EXISTS Notes
            """
        )
        conn.commit()
        conn.close()
        self.create_table_if_not_exist()

    def add_new_note(self, note_text:str):
        conn = self.connect_to_db()
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO Notes (text) VALUES (?)
            """,
            (note_text,)
        )
        conn.commit()
        conn.close()

    def delete_note_by_id(self, note_id):
        conn = self.connect_to_db()
        c = conn.cursor()
        c.execute(
            """
            DELETE FROM Notes WHERE id=(?)
            """,
            (note_id,)
        )
        conn.commit()
        conn.close()

    # recuperer:
    def get_all_notes(self):
        conn = self.connect_to_db()
        c = conn.cursor()
        c.execute("SELECT * FROM Notes")
        results = c.fetchall()
        conn.close()
        notes = [ Note(id=id, text=text, created_at=created_at) for id,text,created_at in results ]
        return notes

    def get_one_note_by_id(self, note_id):
        conn = self.connect_to_db()
        c = conn.cursor()
        c.execute("SELECT * FROM Notes WHERE id=(?)", (note_id,))
        result = c.fetchone()
        conn.close()
        if result:
            id, text, created_at = result
            return Note(id=id, text=text, created_at=created_at)
        return None




# ================== model de Note ============= # 
class Note ():
    def __init__(self,id, text, created_at):
        self.id = id
        self.text = text
        self.created_at = created_at

    def __str__(self):
        return f"id:{self.id} | text = {self.text} | created_at:{self.created_at} |"
    
    def save_note_in_db(self, db:MyDatabase):
        db.add_new_note(note_text=self.text)

    def delete_note_by_id_in_db(self, db:MyDatabase):
        db.delete_note_by_id(note_id=self.id)






def main():
    # ============ setup db ============== #
    # .home() = automatic ~/home/koko
    DB_PATH = Path.home() /  ".local" / "share" / "note" / "note.db"
    # .parent = cd .. remonte d'un cran
    DB_PATH.parent.mkdir(exist_ok=True, parents=True)

    my_note_db = MyDatabase(db_path=DB_PATH)
    my_note_db.create_table_if_not_exist()



    # ============== argparse ============= #
    my_parser = argparse.ArgumentParser("parser for notes.")
    my_parser.add_argument("text", nargs="?", help="text of your note.")
    my_parser.add_argument("-d", "--delete",type=int, help="usage: -d <note id> to delete it.")
    my_parser.add_argument("-z", "--zoom", type=int, help="usage: -z <note id> to \"zoom\" on it (get One note).")
    my_parser.add_argument("-r", "--reset", action="store_true", help="usage: -r reset the table of notes (DELETE ALL OLD NOTES).")
    parser_args = my_parser.parse_args()

    id_to_delete:int = parser_args.delete
    id_to_zoom:int = parser_args.zoom


    if parser_args.delete:
        my_note_db.delete_note_by_id(note_id=id_to_delete)
    
    elif parser_args.zoom:
        note = my_note_db.get_one_note_by_id(note_id=id_to_zoom)
        if note is None:
            print("note not exist!")
        else:
            # print(f"""
            #     # === ID: {note.id} === #

            #     {note.text}

            #     <created at: {note.created_at}> 
            # """)
            print(f"\n# === ID: {note.id} === #\n\n{note.text}\n\n<created at: {note.created_at}>")


    elif parser_args.text:
        my_note_db.add_new_note(note_text=parser_args.text)
        print("note added!")

    elif parser_args.reset:
        my_note_db.reset_table()
        print("Notes tables reset! All cleared!")

    else:
        print("# ==== Notes ========================================== #")
        notes: List[Note] = my_note_db.get_all_notes() 
        if notes == []:
            print("no notes for now...")
        else:
            for note in notes:
                print(note)

if __name__ == "__main__":
    main()





