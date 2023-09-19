import sqlite3
import json
import os

with open('config.json','r') as f:
    config = json.load(f) 
    
database_path = config["database_path"]

if not os.path.exists(database_path):
    os.makedirs(database_path)

database = os.path.join(database_path,'ingestion.db')
with sqlite3.connect(database) as conn:
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS ingestion
              (id INTEGER PRIMARY KEY, name TEXT, location TEXT,
               date TEXT, size INTEGER, details TEXT, output TEXT)""")
              
    conn.commit()


database = os.path.join(database_path,'scoring.db')
with sqlite3.connect(database) as conn:
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS scoring
              (id INTEGER PRIMARY KEY, model_name TEXT, data_location TEXT,
               model_location TEXT, date TEXT, f1_score REAL)""")
              
    conn.commit()
    
database = os.path.join(database_path,'diagnostics.db')
with sqlite3.connect(database) as conn:
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS diagnostics
              (id INTEGER PRIMARY KEY, prediction TEXT, scoring TEXT,
               summarystats TEXT, diagnostics TEXT, date TEXT)""")
              
    conn.commit()