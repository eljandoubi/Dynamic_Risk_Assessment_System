import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from diagnostics import model_predictions


###############Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

test_data_path = config['test_data_path']
output_model_path = config["output_model_path"]
target = config["target"]
test_file = config["test_file"]
plot_name = config["plot_name"]




##############Function for reporting
def score_model():
    #calculate a confusion matrix using the test data and the deployed model
    #write the confusion matrix to the workspace

    test_path = os.path.join(test_data_path,test_file)
    test = pd.read_csv(test_path)
    y_true = test[target]
    X = test.drop([target],axis=1)
    del test
    
    y_pred = model_predictions(X)

    cm = metrics.confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(5, 5))
    sns.heatmap(cm, annot=True, fmt='g', cmap='Blues')
    plt.title('Confusion Matrix')
    tick_marks = np.arange(2)  # Number of classes
    plt.xticks(tick_marks, ['Class 0', 'Class 1'])
    plt.yticks(tick_marks, ['Class 0', 'Class 1'], rotation=90)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    fig_path = os.path.join(output_model_path, plot_name)
    plt.savefig(fig_path)
    



if __name__ == '__main__':
    score_model()
