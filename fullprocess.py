import subprocess
import os
import json
import sqlite3
import sys
import pandas as pd


subprocess.run(["python","dbsetup.py"])

with open('config.json','r') as f:
    config = json.load(f)
    
    
input_folder_path = config['input_folder_path']
database_path = config["database_path"]


toingest_files = set(map(lambda x:os.path.join(input_folder_path, x),
                os.listdir(input_folder_path)))

database_name = os.path.join(database_path,"ingestion.db")
with sqlite3.connect(database_name) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT location, name FROM ingestion")
    rows = cursor.fetchall()
    conn.commit()
    
if rows is not None:
    
    ingested_files = set(map(lambda x:os.path.join(*x),rows))
    
    toingest_files-=ingested_files
    
    if len(toingest_files)==0:
        sys.exit()
        

subprocess.run(["python","ingestion.py"])


database_name = os.path.join(database_path,"scoring.db")
with sqlite3.connect(database_name) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT f1_score FROM scoring WHERE deployed=1")
    rows = cursor.fetchall()
    conn.commit()
    
try:
    score=max(rows)[0]
except ValueError:
    pass
else:
    
    final_dataframe = pd.DataFrame()
    for file in toingest_files:
        if file.endswith(".csv"):
            df = pd.read_csv(file)
            final_dataframe=final_dataframe.append(df)
            
    final_dataframe.drop_duplicates(inplace=True)            
    final_dataframe.to_csv("temp.csv",index=False)
    
    prod_deployment_path = config["prod_deployment_path"]
    deploy_name = config["deploy_name"]
    model_save = os.path.join(prod_deployment_path,deploy_name)
    
    s=subprocess.run(["python","scoring.py","temp.csv",model_save],
                     capture_output=True)
    
    os.remove("temp.csv")
    
    test_score = float(s.stdout)
    
    if test_score >= score:
        sys.exit()
        
        
subprocess.run(["python","training.py"])
    
subprocess.run(["python","deployment.py"])

subprocess.run(["python","reporting.py"])

subprocess.run(["python","apicalls.py"])








