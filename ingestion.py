import pandas as pd
import os
import json
from datetime import datetime
import sqlite3
import sys




#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']
output_file = config["output_file"]
database_path = config["database_path"]



#############Function for data ingestion
def merge_multiple_dataframe():
    #check for datasets, compile them together, and write to an output file
    
    if not os.path.isdir(output_folder_path):
        os.mkdir(output_folder_path)
    
    output_path = os.path.join(output_folder_path,output_file)
    
    ingestion_database = os.path.join(database_path,sys.argv[0][:-3]+'.db')

    if os.path.isfile(output_path):
        final_dataframe = pd.read_csv(output_path)
    else:
        final_dataframe = pd.DataFrame()
    
    conn = sqlite3.connect(ingestion_database)
    c = conn.cursor()
    
    for file in os.listdir(input_folder_path):
        if file.endswith(".csv"):
            path = os.path.join(input_folder_path,file)
            df = pd.read_csv(path)
            
            if final_dataframe.empty:
                final_dataframe = df.copy()
            else:
                final_dataframe=final_dataframe.append(df)
                
            c.execute(
                "INSERT INTO ingestion (name, location, date, output) VALUES (?, ?, ?, ?)",
                (path, input_folder_path, str(datetime.now()), output_path))
            conn.commit()
    
    conn.close()
    final_dataframe.drop_duplicates(inplace=True)            
    final_dataframe.to_csv(output_path,index=False)
    


if __name__ == '__main__':
    merge_multiple_dataframe()
