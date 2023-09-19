from flask import Flask, request

import pandas as pd
from scoring import score_model
import diagnostics as dg
import json
from io import StringIO



with open('config.json','r') as f:
    config = json.load(f)
    
target = config["target"]


######################Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'



#######################Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():        
    #call the prediction function you created in Step 3
    test_file = request.files['test_file']
    file_content = test_file.read().decode('utf-8')
    test = pd.read_csv(StringIO(file_content))
    X_test = test.drop([target],axis=1,errors="ignore")
    return str(dg.model_predictions(X_test)) #add return value for prediction outputs

#######################Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def score():        
    #check the score of the deployed model
    return str(score_model()) #add return value (a single F1 score number)

#######################Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def stats():        
    #check means, medians, and modes for each column
    return str(dg.dataframe_summary()) #return a list of all calculated summary statistics

#######################Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def diagno():        
    #check timing and percent NA values
    
    res = [dg.execution_time(),dg.missing_data(),dg.outdated_packages_list()]
    
    return "\n\n\n".join(map(str,res)) #add return value for all diagnostics

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
