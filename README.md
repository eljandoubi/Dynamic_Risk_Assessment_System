# Dynamic_Risk_Assessment_System

# Environment Set up
* conda create -n DRAS python="3.7.6" -y
* conda activate DRAS
* Install git either through conda (“conda install git”) or through your CLI, e.g. sudo apt-get git.
* Clone the repository ```git clone https://github.com/eljandoubi/Dynamic_Risk_Assessment_System.git```
* Move to folder ```cd Dynamic_Risk_Assessment_System```
* pip install -r requirements.txt
    
# Get started

* To run the Process use ```python fullprocess.py```
* To check the databse use ```python db_test.py [database_name]``` where database_name can be ingestion, scoring or diagnostics