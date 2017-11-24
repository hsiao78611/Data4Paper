import os
import json
import pandas as pd
import sqlite3

directory = os.getcwd() + '/' + 'RECORD' # datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists(directory):
    os.makedirs(directory)

FILE = os.path.join(os.path.dirname(__file__), 'record_explore.json')

conn_rec = sqlite3.connect(directory + '/' + 'rec_explore.db')

df_temp = pd.DataFrame({
    'id': [],
    'index': [],
    'exp_num': [],
    'get_num': []
})

with open(FILE, 'r') as f:record = json.load(f)

for i in range(len(record['id'])):

    df = pd.DataFrame({
        'id': [record['id'][i]],
        'index': [record['index'][i]],
        'exp_num': [record['exp_num'][i]],
        'get_num': [record['get_num'][i]]
    })

    df.to_sql(name = 'rec_explore', con = conn_rec, if_exists = 'append', index = False)

conn_rec.close()
