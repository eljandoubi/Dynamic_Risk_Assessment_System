"""
You can Query data by calling this script in the terminal followed by the databse name
"""

import sqlite3

import sys


with sqlite3.connect(sys.argv[1]) as conn:
    cursor = conn.cursor()
    
    
    cursor.execute(f"SELECT * FROM {sys.argv[1][:-3]}")
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)