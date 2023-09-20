import requests
import json
import os
import sqlite3
from datetime import datetime
from app import app
from multiprocessing import Process

server = Process(target=app.run)
server.start()


with open('config.json','r') as f:
    config = json.load(f)
    
    
database_path = config["database_path"]
test_data_path = config["test_data_path"]
test_file = config["test_file"]


test_path = os.path.join(test_data_path,test_file)
files = {'test_file': (test_path, open(test_path, 'rb'))}

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:5000"


#Call each API endpoint and store the responses
response1 = requests.post(URL+"/prediction", files=files)
response2 = requests.get(URL+"/scoring")  #put an API call here
response3 = requests.get(URL+"/summarystats") #put an API call here
response4 = requests.get(URL+"/diagnostics") #put an API call here

#combine all API responses

responses = list(map(lambda i:str(eval(f"response{i}").text),range(1,5)))

#write the responses to your workspace

responses.append(str(datetime.now()))

database = os.path.join(database_path,'diagnostics.db')
with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO diagnostics (prediction, scoring, summarystats,
            diagnostics, date) VALUES (?, ?, ?, ?, ?)""",
            responses)
        conn.commit()


server.terminate()
server.join()