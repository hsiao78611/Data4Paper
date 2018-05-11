import os
import sqlite3
import time
from datetime import datetime
import random
from random import randint
import pandas as pd

import packages.individual.upd_crawler
import packages.utils.renewip as new
import packages.utils.record as rec
import packages.utils.getlink
from packages.utils.alnum import get_current_datetime

# thread-based Pool
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from multiprocessing import Queue
import traceback

print get_current_datetime()

# create a directory
directory = os.getcwd() + '/' + 'RECORD'
if not os.path.exists(directory):
    os.makedirs(directory)

# Create connections.
conn_upd = sqlite3.connect(directory + '/' + 'upd_body_0511.db', timeout=10.0, check_same_thread=False)


# list of successful projects
pid_lnk = packages.utils.getlink.upd_links('re_ub_0511')
pids = list(pid_lnk['pid'])
upd_ids = list(pid_lnk['upd_id'])
upd_lnks = list(pid_lnk['upd_url'])

# randomise crawling order
id_lst = range(len(upd_lnks))
random.shuffle(id_lst)

# if there exists the record, load it.
# then remove(pop) the index of crawled data
record = rec.Record('record_upd_body_0103')
rec_df = record.get_record()
if not rec_df.empty:
    rec_index = list(set(list(rec_df['index'])))
    while rec_index:
        id_lst.remove(rec_index.pop())

def crawler(id):
    pid = pids[id]
    upd_id = upd_ids[id]
    upd_lnk = upd_lnks[id]
    # used to record processing time
    start_time = time.time()

    # dataframe
    if upd_lnk != None:
        df_upd = packages.individual.upd_crawler.update('https://www.kickstarter.com' + upd_lnk, pid, upd_id)
        print 'loading ' + pid + ': ' + str(upd_id) + ': https://www.kickstarter.com' + upd_lnk
    else:
        df_upd = pd.DataFrame(
            {'pid': [pid],
             'upd_id': [str(upd_id)],
             'upd_url': ['sys_upd'],
             'upd_body': ['sys_upd']
             })
        print 'loading ' + pid + ': ' + str(upd_id) + ' None'
    exe_time = time.time() - start_time
    print exe_time

    # save to 'sqlite'
    def _save_df():
        df_upd.to_sql(name = 'upd_body_0103', con = conn_upd, if_exists = 'append', index = False)
        record.save_record(pids[id], id)

    # # crawling via multiprocessing and queue
    # # put it in a queue then get a permission
    # crawler.que.put(_save_df())

    # crawling one by one
    _save_df()

# crawling one by one
while id_lst:
    id = id_lst.pop()
    crawler(id)

# # crawling via multiprocessing and queue
# def worker(queue):
#     crawler.que = queue
#
# try:
#     the_queue = Queue()
#     pool = Pool(cpu_count() + 2, worker,[the_queue])  # Can create a Pool with cpu_count * 2 threads.
#     pool.imap(crawler, id_lst)
#     pool.close()
#     while True:
#         the_queue.get(True)
# except Exception as e:
#     print e
#     traceback.print_exc()
#     print get_current_datetime()

conn_upd.close()
