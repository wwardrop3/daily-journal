
import sqlite3
import json
from Models import Mood


def get_all_moods():
    
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        
        db_cursor.execute("""
            SELECT
                m.id,
                m.label
            FROM moods m
            """)
        
        dataset = db_cursor.fetchall()
        
        moods = []
        
        for row in dataset:
            mood = Mood(row['id'], row['label'])
            moods.append(mood.__dict__)
            
    return json.dumps(moods)
            
            