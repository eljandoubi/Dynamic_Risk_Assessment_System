import pandas as pd
import numpy as np
import timeit
import os
import json
import pickle
import subprocess

##################Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
test_data_path = os.path.join(config['test_data_path'])
deploy_name = config["deploy_name"]
prod_deployment_path = config['prod_deployment_path']
target = config["target"]
test_file = config["test_file"]
dataset_file = config["output_file"]

##################Function to get model predictions
def model_predictions(X):
    #read the deployed model and a test dataset, calculate predictions
    
    model_save = os.path.join(prod_deployment_path,deploy_name)
    with open(model_save, 'rb') as file:
        pipeline = pickle.load(file)
    
    return pipeline.predict(X) #return value should be a list containing all predictions

##################Function to get summary statistics
def dataframe_summary():
    #calculate summary statistics here
    data_path = os.path.join(dataset_csv_path, dataset_file)
    data = pd.read_csv(data_path)
    return pd.concat([data.mean(),
            data.median(),
            data.std(),
            ],axis=1).to_numpy().tolist() #return value should be a list containing all summary statistics


##################Function to check for missing data
def missing_data():
    data_path = os.path.join(dataset_csv_path, dataset_file)
    data = pd.read_csv(data_path)
    return (data.isna().sum()/len(data)).tolist()

##################Function to get timings
def execution_time():
    #calculate timing of training.py and ingestion.py
    
    starttime = timeit.default_timer()
    os.system('python ingestion.py')
    timing1=timeit.default_timer() - starttime
    
    starttime = timeit.default_timer()
    os.system('python3 training.py')
    timing2=timeit.default_timer() - starttime
    
    return [timing1,timing2] #return a list of 2 timing values in seconds

##################Function to check dependencies
def outdated_packages_list():
    #get a list of 
    outdated = subprocess.check_output(['pip', 'list','--outdated'])
    
    outdated = str(outdated).split("\\n")
    outdated.pop(1)
    outdated.pop()
    
    return np.array(list(map(lambda x:x.split()[:-1],
                             outdated))).T.tolist()

if __name__ == '__main__':
    test_path = os.path.join(test_data_path,test_file)
    test = pd.read_csv(test_path)
    X_test = test.drop([target],axis=1)
    print(
    model_predictions(X_test),
    dataframe_summary(),
    missing_data(),
    execution_time(),
    outdated_packages_list(),
    sep="\n\n"
    )





    
