import os
import sqlite3
import time
from datetime import datetime
import random
from random import randint

import pandas as pd

import ks.creator.crt_crawler
import ks.utils.renewip as new
import ks.utils.record as rec
import ks.utils.getlink
from ks.utils.alnum import get_current_datetime

# thread-based Pool
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from multiprocessing import Queue
import traceback



crt_lnk = 'https://www.kickstarter.com/profile/'

# create a directory
directory = os.getcwd() + '/' + 'RECORD' # datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists(directory):
    os.makedirs(directory)

# Create connections.
conn_about = sqlite3.connect(directory + '/' + 'about.db')
conn_backed = sqlite3.connect(directory + '/' + 'backed.db')
conn_created = sqlite3.connect(directory + '/' + 'created.db')

# list of creators
crt_ids = ks.utils.getlink.crt_links('crt_ids')
cids = list(crt_ids['proj_creator_id'])
pids = list(crt_ids['pid'])

# randomise crawling order
crt_lst = range(len(cids))
random.shuffle(crt_lst)

# if there exists the record, load it.
# then remove(pop) the index of crawled data
record = rec.Record('record_creator')
rec_df = record.get_record()
if not rec_df.empty:
    rec_index = list(set(list(rec_df['index'])))
    while rec_index:
        crt_lst.remove(rec_index.pop())

def crawler(id):
    cid = cids[id]

    # used to record processing time
    start_time = time.time()

    crt = ks.creator.crt_crawler.Creator(crt_lnk + cid, cid)
    print 'loading ' + cid + '- project: ' + pids[id]

    # dataframe
    df_about = crt.about()
    df_backed = crt.backed()
    df_created = crt.created()

    exe_time = time.time() - start_time
    print exe_time

    # save to 'sqlite'
    def _save_df():
        df_about.to_sql(name = 'about', con = conn_about, if_exists = 'append', index = False)
        df_backed.to_sql(name = 'backed', con = conn_backed, if_exists = 'append', index = False)
        df_created.to_sql(name = 'created', con = conn_created, if_exists = 'append', index = False)
        # record what already be loaded
        record.save_record(pids[id], id)

    # crawling via multiprocessing and queue
    # put it in a queue then get a permission
    crawler.que.put(_save_df())

    ## crawling one by one
    # _save_df()

## crawling one by one
# while crt_lst:
#     id = crt_lst.pop()
#     crawler(id)

# crawling via multiprocessing and queue
def worker(queue):
    crawler.que = queue

try:
    the_queue = Queue()
    pool = Pool(cpu_count() + 2, worker,[the_queue])  # Can create a Pool with cpu_count * 2 threads.
    pool.imap(crawler, crt_lst)
    pool.close()
    while True:
        the_queue.get(True)
except Exception as e:
    print e
    traceback.print_exc()
    print get_current_datetime()

conn_about.close()
conn_backed.close()
conn_created.close()
