import sqlite3
import os
import pandas as pd

directory = os.getcwd() + '/' + 'RECORD'  # datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

class Record:

    def __init__(self, name):
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.name = name
        self.conn = sqlite3.connect(directory + '/' + name + '.db', timeout=10.0, check_same_thread=False)

    def save_record(self, id, index, exp_num=None, get_num=None):
        df = pd.DataFrame({
            'id': [id],
            'index': [index],
            'exp_num': [exp_num],
            'get_num': [get_num]
        })
        df.to_sql(name=self.name, con=self.conn, if_exists='append', index=False)

    def get_record(self):
        tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + self.name + "'"
        if not self.conn.execute(tb_exists).fetchone():
            return pd.DataFrame()

        df = pd.read_sql_query('SELECT * FROM ' + self.name, self.conn)
        return df
