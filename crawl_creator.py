import os
import sqlite3
import time
from datetime import datetime
import random
from random import randint

import pandas as pd

import ks.individual.proj_crawler
import ks.utils.renewip as new
import ks.utils.record as rec

# the list is crawled by GoogleScraper and precessed by ProjectList.py
crt_lnks = ['https://www.kickstarter.com/profile/1874897140']

# create a directory
directory = os.getcwd() + '/' + 'RECORD' # datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists(directory):
    os.makedirs(directory)

# def save(df, file_name):
#     if not os.path.isfile(directory + '/' + file_name): # if file does not exist
#         df.to_csv(directory + '/' + file_name, index=False, encoding='utf-8-sig')
#     else:  # else it exists so append without writing the header
#         df.to_csv(directory + '/' + file_name, mode='a', index=False, header=False, encoding='utf-8-sig')

# Create connections.
conn_about = sqlite3.connect(directory + '/' + 'about.db')
conn_backed = sqlite3.connect(directory + '/' + 'backed.db')
conn_created = sqlite3.connect(directory + '/' + 'created.db')

# randomise crawling order
crt_lst = range(len(crt_lnks))
random.shuffle(crt_lst)

# if there exists the record, load it.
# then remove(pop) the index of crawled data
record = rec.Record('record_creator')
rec_df = record.get_record()
if rec_df != False:
    rec_index = list(set(list(rec_df['index'])))
    while rec_index:
        crt_lst.remove(rec_index.pop())

while crt_lst:
    cid = crt_lst.pop()

    # used to record processing time
    start_time = time.time()

    crt = ks.creator.crt_crawler.Creater(crt_lst[cid], cid)
    print 'loading ' + cid + ': ' + crt_lnks[cid]

    # dataframe
    df_about = crt.about()
    df_backed = crt.backed()
    df_created = crt.created()

    # record what already be loaded
    record.save_record(crt_lst[cid], cid)

    # save to 'sqlite'
    df_about.to_sql(name = 'about', con = conn_about, if_exists = 'append', index = False)
    df_backed.to_sql(name = 'backed', con = conn_backed, if_exists = 'append', index = False)
    df_created.to_sql(name = 'created', con = conn_created, if_exists = 'append', index = False)

    time.sleep(randint(1, 5))
    # renew a connection
    new.renew_connection()

conn_about.close()
conn_backed.close()
conn_created.close()
