"""
You can Query data by calling this script in the terminal followed by the databse name
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
    
    
    cursor.execute(f"SELECT * FROM {sys.argv[1]}")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)