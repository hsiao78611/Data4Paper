import os
import sqlite3
import pandas as pd

def _conn():
    # create a directory
    directory = os.getcwd() + '/' + 'RECORD'
    if not os.path.exists(directory):
        os.makedirs(directory)
    # create connections of database.
    conn = sqlite3.connect(directory + '/' + 'explore.db')
    return conn

def proj_links():
    conn = _conn()
    df = pd.read_sql_query('SELECT link FROM explore GROUP BY link', conn)
    return list(df['link'])

def crt_links():
    conn = _conn()
    df = pd.read_sql_query('SELECT c_link FROM explore GROUP BY c_link', conn)
    return list(df['c_link'])