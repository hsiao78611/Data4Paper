import os
import sqlite3
import pandas as pd

def _conn(name):
    # create a directory
    directory = os.getcwd() + '/' + 'RECORD'
    if not os.path.exists(directory):
        os.makedirs(directory)
    # create connections of database.
    conn = sqlite3.connect(directory + '/' + name + '.db')
    return conn

def proj_links(name):
    conn = _conn(name)
    df = pd.read_sql_query('SELECT proj_url, pid FROM '+ name +' GROUP BY proj_url', conn)
    return df

def crt_links(name):
    conn = _conn(name)
    df = pd.read_sql_query('SELECT * FROM '+ name, conn)
    return df

def upd_links(name):
    conn = _conn(name)
    df = pd.read_sql_query('SELECT upd_url, pid, upd_id FROM '+ name, conn)
    return df