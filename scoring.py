import pandas as pd
import pickle
import os
from sklearn import metrics
import json
from datetime import datetime
import sqlite3
import sys

#################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 
    
    
model_path = config['output_model_path']
dataset_file = config["output_file"]
database_path = config["database_path"]
test_data_path = config["test_data_path"]
target = config["target"]
deploy_name = config["deploy_name"]
test_file = config["test_file"]



#################Function for model scoring
def score_model():
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    #it should write the result to the latestscore.txt file
    if len(sys.argv)==2:
        test_path = sys.argv[1]
    else:
        test_path = os.path.join(test_data_path,test_file)
    
    test = pd.read_csv(test_path)
    
    y = test[target]
    X = test.drop([target],axis=1)
    
    del test
    
    if len(sys.argv)==3:
        model_save = sys.argv[2]
    else:
        model_save = os.path.join(model_path,deploy_name)
    
    with open(model_save, 'rb') as file:
        pipeline = pickle.load(file)
        
    model_name = pipeline.steps[-1][0]
    
    y_pred = pipeline.predict(X)
    
    score = metrics.f1_score(y, y_pred)
    
    time = str(datetime.now())
    
    database = os.path.join(database_path,'scoring.db')
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT OR IGNORE INTO scoring (model_name, data_location, model_location,
            date, f1_score, deployed) VALUES (?, ?, ?, ?, ?, 0)""",
            (model_name, test_path, model_save, time, score))
        conn.commit()
        
    return score
        
if __name__ == '__main__':
    print(score_model())