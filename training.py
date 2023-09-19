import pandas as pd
import numpy as np
import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn import preprocessing as pp
import json

###################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(config['output_folder_path']) 
model_path = os.path.join(config['output_model_path'])
dataset_file = config["output_file"]
database_path = config["database_path"]
target = config["target"]
deploy_name = config["deploy_name"]
test_file = config["test_file"]


#################Function for training the model
def train_model():
    
    #use this logistic regression for training
    
    data_path = os.path.join(dataset_csv_path, dataset_file)
    train = pd.read_csv(data_path)
    
    y = train[target]
    X = train.drop([target],axis=1)
    
    del train
    
    ct = make_column_transformer((pp.Normalizer(),
                                  make_column_selector(
                                      dtype_include=np.number)))
    pipeline = make_pipeline(ct, LogisticRegression())
    #fit the logistic regression to your data
    pipeline.fit(X,y)
    #write the trained model to your workspace in a file called trainedmodel.pkl
    
    if not os.path.isdir(model_path):
        os.mkdir(model_path)
    
    model_save = os.path.join(model_path,deploy_name)
    
    pickle.dump(pipeline, open(model_save, 'wb'))

if __name__ == '__main__':
    train_model()