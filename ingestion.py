import pandas as pd
import os
import json
from datetime import datetime
import sqlite3




#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']

if not os.path.isdir(output_folder_path):
    os.mkdir(output_folder_path)




#############Function for data ingestion
def merge_multiple_dataframe(output_file="finaldata.csv"):
    #check for datasets, compile them together, and write to an output file
    
    output_file = os.path.join(output_folder_path,output_file)

    if os.path.isfile(output_file):
        final_dataframe = pd.read_csv(output_file)
    else:
        final_dataframe = pd.DataFrame()
    
    conn = sqlite3.connect('ingestion.db')
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
                (path, input_folder_path, str(datetime.now()), output_file))
            conn.commit()
    
    conn.close()
    final_dataframe.drop_duplicates(inplace=True)            
    final_dataframe.to_csv(output_file,index=False)
    


if __name__ == '__main__':
    merge_multiple_dataframe()
