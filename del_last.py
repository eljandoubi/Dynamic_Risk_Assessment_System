"""
You can delete last row by calling this script in the terminal followed by the databse name
"""

import sqlite3
import json
import sys
import os

with open('config.json','r') as f:
    config = json.load(f)

database_path = config["database_path"]

database_name = os.path.join(database_path,sys.argv[1]+".db")

with sqlite3.connect(database_name) as conn:
    cursor = conn.cursor()

    # Find the last row
    cursor.execute(f"SELECT id FROM {sys.argv[1]} ORDER BY id DESC LIMIT 1")
    last_row = cursor.fetchone()

    if last_row is not None:
        last_row_id = last_row[0]

        # Delete the last row
        cursor.execute(f"DELETE FROM {sys.argv[1]} WHERE id = ?", (last_row_id,))
        conn.commit()
        print(f"Deleted row with id {last_row_id}")
    else:
        print("The table is empty")
