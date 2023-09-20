# Dynamic_Risk_Assessment_System

## Overview
In this repository, I have developed a solution for a large company facing attrition risk among its 10,000 corporate clients. The primary concern is the potential loss of clients and revenue when contracts are terminated. To address this issue, I've created an end-to-end machine learning (ML) model for risk assessment.

The ML model's purpose is to estimate attrition risk for all 10,000 clients. By accurately identifying clients at the highest risk, the company's client management team can prioritize their efforts, preventing contract exits, and preserving revenue.

However, the work doesn't stop with model creation and deployment. The industry in which the company operates is dynamic and constantly changing. Therefore, a robust monitoring system has been implemented in this repository. It includes processes and scripts for regular model retraining, redeployment, monitoring, and reporting. This ensures that the ML model remains accurate and up-to-date, allowing the company to minimize client attrition effectively.

## Environment Set up
* conda create -n DRAS python="3.7.6" -y
* conda activate DRAS
* Install git either through conda (“conda install git”) or through your CLI, e.g. sudo apt-get git.
* Clone the repository ```git clone https://github.com/eljandoubi/Dynamic_Risk_Assessment_System.git```
* Move to folder ```cd Dynamic_Risk_Assessment_System```
* pip install -r requirements.txt
    
## Get started
* To run the Process use ```python fullprocess.py```
* To check the databse use ```python db_test.py [database_name]``` where database_name can be ingestion, scoring or diagnostics
