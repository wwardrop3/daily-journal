import sqlite3
import json

from Models import Entry
from Models.Mood import Mood
from Models.Tag import Tag


def get_all_entries():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        entries = []
        
        
        db_cursor.execute("""
            SELECT
                j.id,
                j.concept,
                j.entry,
                j.date,
                j.mood_id,
                m.label mood_label


            FROM JournalEntries j
            JOIN moods m
            ON j.mood_id = m.id 
            """)
        
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'])
            
            mood_empty = Mood(row['mood_id'], row['mood_label'])
        
            entry.mood_label = mood_empty.__dict__
            
            
            db_cursor.execute("""
                SELECT
                    e.id,
                    e.entry_id,
                    e.tag_id,
                    t.label tag_label
                FROM EntryTags e
                JOIN Tags t
                ON t.id = e.tag_id
                WHERE e.entry_id = ?
                              """, (row['id'], ))
            
            data = db_cursor.fetchall()
            
            tags = []
            
            for result in data:
                tag = Tag(result['tag_id'], result['tag_label'])
                tags.append(tag.__dict__)
            
            entry.tags = tags
            
            
            entries.append(entry.__dict__)
            
            
            
            
            
        return json.dumps(entries)    
        
def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            SELECT    
                j.id,
                j.concept,
                j.entry,
                j.date,
                j.mood_id
            FROM JournalEntries j
            WHERE j.id = ?
                        """, (id, ))
    
    data = db_cursor.fetchone()
    
    entry = Entry(data['id'], data['concept'], data['entry'], data['date'], data['moodId'])
    
    return json.dumps(entry.__dict__)


def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            DELETE
            FROM JournalEntries
            WHERE id = ?
            """,(id, ))
        

def create_new_entry(new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            INSERT INTO JournalEntries
                (concept, entry, date, mood_id)
            VALUES 
            ( ?, ?, ?, ?); 
            """, (new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['moodId'])); #new entry is json format, so moodId needs to match the front end formatting

        
        new_id = db_cursor.lastrowid
        new_entry['id'] = new_id
        
        
        db_cursor.execute("""
            SELECT *
            FROM Tags""")
        
        tag_results = db_cursor.fetchall()
        
        for result in tag_results:
            print(result)
        return json.dumps(new_entry)

def get_entries_by_search_term(term):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            SELECT *
            FROM JournalEntries j
            WHERE j.entry LIKE ?       
                          
                          """, (f"%{term}%", ))
        
        dataset = db_cursor.fetchall()
        results = []
        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'])
            results.append(entry.__dict__)
        
        return json.dumps(results)
    
def update_entry(updated_entry, id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            UPDATE JournalEntries
            SET
                concept = ?,
                entry = ?,
                date = ?,
                mood_id = ?
            
            WHERE id = ?
                """, (updated_entry['concept'], updated_entry['entry'], updated_entry['date'], updated_entry['moodId'], id, ))
            
        
        rows_affected = db_cursor.rowcount
        
        if rows_affected > 0:
            return True
        else:
            return False
        
        

        
        
        
        