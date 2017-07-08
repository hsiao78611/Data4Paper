import os
import sqlite3
import pandas as pd

def __init__(self):
    # create a directory
    directory = os.getcwd() + '/' + 'RECORD'
    if not os.path.exists(directory):
        os.makedirs(directory)
    # create connections of database.
    self.conn = sqlite3.connect(directory + '/' + 'explore.db')

def proj_links(self):
    df = pd.read_sql_query('SELECT link FROM explore GROUP BY link', self.conn)
    return list(df['link'])

def crt_links(self):
    df = pd.read_sql_query('SELECT c_link FROM explore GROUP BY c_link', self.conn)
    return list(df['c_link'])