import os
import sqlite3
import time
from datetime import datetime
import random
from random import randint

import pandas as pd

import packages.creator.crt_crawler
import packages.utils.renewip as new
import packages.utils.record as rec
import packages.utils.getlink
from packages.utils.alnum import get_current_datetime

# thread-based Pool
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from multiprocessing import Queue
import traceback

# create a directory
directory = os.getcwd() + '/' + 'RECORD'  # datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists(directory):
    os.makedirs(directory)

# Create connections.
conn_about = sqlite3.connect(directory + '/' + 'about.db', timeout=10.0, check_same_thread=False)
conn_backed = sqlite3.connect(directory + '/' + 'backed.db', timeout=10.0, check_same_thread=False)
conn_created = sqlite3.connect(directory + '/' + 'created.db', timeout=10.0, check_same_thread=False)

# list of creators
crt_ids = packages.utils.getlink.crt_links('re_crt_1213')
cids = list(crt_ids['proj_creator_id'])#'cmt_profile_id'])
pids = list(crt_ids['pid'])

# randomise crawling order'
crt_lst = range(len(cids))
random.shuffle(crt_lst)

# if there exists the record, load it.
# then remove(pop) the index of crawled data
record = rec.Record('record_re_crt_1213')
rec_df = record.get_record()
if not rec_df.empty:
    rec_index = list(set(list(rec_df['index'])))
    while rec_index:
        crt_lst.remove(rec_index.pop())


def crawler(id):
    crt_lnk = 'https://www.kickstarter.com/profile/'
    cid = cids[id]
    pid = pids[id]

    # used to record processing time
    start_time = time.time()

    crt = packages.creator.crt_crawler.Creator(crt_lnk + cid, cid)
    print 'loading ' + cid + ' - project: ' + pid

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
        # record.save_record(pids[id], id)
        record.save_record(cids[id], id)

    # # crawling one by one
    # _save_df()

    # crawling via multiprocessing and queue
    # put it in a queue then get a permission
    crawler.que.put(_save_df())


# setting an attribute named 'que' on the function object 'crawler'
def worker(queue):
    crawler.que = queue

if __name__ == '__main__':

    # # crawling one by one
    # while crt_lst:
    #     id = crt_lst.pop()
    #     crawler(id)

    # crawling via multiprocessing and queue
    try:
        new.renew_connection()

        the_queue = Queue()
        pool = Pool(cpu_count() + 2, worker,[the_queue])  # Can create a Pool with cpu_count * 2 threads.
        pool.imap(crawler, crt_lst)
        pool.close()
        count = 0
        while True:
            lim = randint(2, 4)
            time.sleep(randint(3, 8))

            if count > lim:
                new.renew_connection()
                count = 0
            the_queue.get(True)
            count = count + 1
    except Exception as e:
        print e
        traceback.print_exc()
        print get_current_datetime()

    conn_about.close()
    conn_backed.close()
    conn_created.close()


