import sqlite3
import os
import pandas as pd

directory = os.getcwd() + '/' + 'RECORD'  # datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

class Record:

    def __init__(self, name):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.name = name
        self.conn = sqlite3.connect(directory + '/' + name + '.db')

    def save_record(self, id, index, exp_num, get_num):
        df = pd.DataFrame({
            'id': [id],
            'index': [index],
            'exp_num': [exp_num],
            'get_num': [get_num]
        })
        df.to_sql(name='rec_explore', con=self.conn, if_exists='append', index=False)

    def get_record(self):
        if not os.path.exists(directory + '/' + self.name + '.db'):
            return False

        df = pd.read_sql_query('SELECT * FROM ' + self.name, self.conn)
        return df
