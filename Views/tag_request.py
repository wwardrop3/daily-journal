import sqlite3
import json

from Models.Tag import Tag


def get_all_tags():
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            SELECT
                id,
                label
            FROM tags
                          """)
        
        dataset = db_cursor.fetchall()
        
        tag_list = []
        for row in dataset:
            tag = Tag(row['id'], row['label'])
            tag_list.append(tag.__dict__)
        
        return json.dumps(tag_list)
        