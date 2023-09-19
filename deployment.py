import os
import json
import sqlite3
import shutil
from datetime import datetime



##################Load config.json and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 

model_path = os.path.join(config['output_model_path'])
prod_deployment_path = os.path.join(config['prod_deployment_path']) 
database_path = config["database_path"]

####################function for deployment
def store_model_into_pickle():
    #copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory
    
    if not os.path.isdir(prod_deployment_path):
        os.mkdir(prod_deployment_path)
    
    database = os.path.join(database_path,'scoring.db')
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM scoring ORDER BY id DESC LIMIT 1")
        latest_row = cursor.fetchone()
        
        if latest_row is not None:
        
            if latest_row[3].startswith(model_path):
                model_save = latest_row[3].replace(model_path,prod_deployment_path)
                row = list(latest_row)
                row[3] = model_save
                
                shutil.copy(latest_row[3],row[3])
                
                row[4]=str(datetime.now())
                
                cursor.execute(
                    "INSERT INTO scoring (model_name, data_location, model_location, date, f1_score) VALUES (?, ?, ?, ?, ?)",
                    row[1:])
                conn.commit()

        

if __name__ == '__main__':
    store_model_into_pickle()