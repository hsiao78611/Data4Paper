import os
import sqlite3
import time
from datetime import datetime
from random import randint

import pandas as pd

import ks.utils.getcategory
import ks.explore.exp_crawler
import ks.utils.renewip as new

# the list is crawled by GoogleScraper and precessed by ProjectList.py
cats = ks.utils.getcategory.get_category()
print 'got categories'

# create a directory
directory = os.getcwd() + '/' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists(directory):
    os.makedirs(directory)
# create connections of database.
conn_ov = sqlite3.connect(directory + '/' + 'overview.db')
conn_exp = sqlite3.connect(directory + '/' + 'explore.db')

# start explore each category
for i in range(len(cats)):
    cat = cats.iloc[i][0]
    cat_id = cats.iloc[i][1]

    print 'crawling: ' + cat
    start_time = time.time()
    exp = ks.explore.exp_crawler.Category(cat_id)
    # dataframe
    df_ov = pd.DataFrame({'category': [cat], 'id': [cat_id], 'total': [exp.total], 'exe_time': [exe_time]})
    df_exp = exp.get_link()
    # calculate processing time
    exe_time = time.time() - start_time
    print exe_time

    # save to 'sqlite'
    df_ov.to_sql(name='rewards', con=conn_ov, if_exists='append', index=False)
    df_exp.to_sql(name = 'projects', con = conn_exp, if_exists = 'append', index = False)

    time.sleep(randint(1, 5))
    # renew a connection
    new.renew_connection()

conn_ov.close()
conn_exp.close()
