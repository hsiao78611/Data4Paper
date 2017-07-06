import os
import sqlite3
import time
from datetime import datetime
import random
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

# start explore each category randomly
cats_lst = range(len(cats))
random.shuffle(cats_lst)
while cats_lst:
    i = cats_lst.pop()

    # crawling randomly
    goal_lst = range(5)
    random.shuffle(goal_lst)
    while goal_lst:
        goal = goal_lst.pop()
        cat = cats.iloc[i][0]
        cat_id = cats.iloc[i][1]

        print 'crawling: ' + cat + ' with goal ' + goal
        start_time = time.time()
        exp = ks.explore.exp_crawler.Category(cat_id, goal)

        # calculate processing time
        exe_time = time.time() - start_time
        print exe_time

        # get dataframe
        df_ov = pd.DataFrame({'category': [cat], 'id': [cat_id], 'goal': [goal], 'total': [exp.total], 'exe_time': [exe_time]})
        df_exp = exp.get_exp()

        # save to 'sqlite'
        df_ov.to_sql(name='overview', con=conn_ov, if_exists='append', index=False)
        df_exp.to_sql(name = 'explore', con = conn_exp, if_exists = 'append', index = False)

        time.sleep(randint(1, 5))
        # renew a connection
        new.renew_connection()

conn_ov.close()
conn_exp.close()
