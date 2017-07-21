import os
import sqlite3
import time
from datetime import datetime
from random import randint
import pandas as pd

import ks.individual.proj_crawler
import ks.utils.renewip as new
import ks.utils.record as rec
import ks.utils.getlink
from ks.utils.alnum import get_current_datetime

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

# def save(df, file_name):
#     if not os.path.isfile(directory + '/' + file_name): # if file does not exist
#         df.to_csv(directory + '/' + file_name, index=False, encoding='utf-8-sig')
#     else:  # else it exists so append without writing the header
#         df.to_csv(directory + '/' + file_name, mode='a', index=False, header=False, encoding='utf-8-sig')

# Create connections.
conn_proj = sqlite3.connect(directory + '/' + 'proj.db', timeout=10.0, check_same_thread=False)
conn_rew = sqlite3.connect(directory + '/' + 'rew.db', timeout=10.0, check_same_thread=False)
conn_upd = sqlite3.connect(directory + '/' + 'upd.db', timeout=10.0, check_same_thread=False)
conn_faq = sqlite3.connect(directory + '/' + 'faq.db', timeout=10.0, check_same_thread=False)
conn_cmt = sqlite3.connect(directory + '/' + 'cmt.db', timeout=10.0, check_same_thread=False)
conn_time = sqlite3.connect(directory + '/' + 'time.db', timeout=10.0, check_same_thread=False)


# list of successful projects
pid_lnk = ks.utils.getlink.proj_links('all_date_2016')
proj_lnks = list(pid_lnk['proj_url'])
pids = list(pid_lnk['pid'])

# randomise crawling order
id_lst = range(len(proj_lnks))
random.shuffle(id_lst)

# if there exists the record, load it.
# then remove(pop) the index of crawled data
record = rec.Record('record_individual')
rec_df = record.get_record()
if not rec_df.empty:
    rec_index = list(set(list(rec_df['index'])))
    while rec_index:
        id_lst.remove(rec_index.pop())

def crawler(id):
    pid = pids[id]
    # used to record processing time
    start_time = time.time()

    proj = ks.individual.proj_crawler.Campaign(proj_lnks[id], pid)
    print 'loading ' + pid + ': ' + proj_lnks[id]

    # dataframe
    proj_rew = proj.project_rewards()
    df_proj = proj_rew[0]
    df_rew = proj_rew[1]
    df_upd = proj.updates()
    df_faq = proj.faqs()
    # df_crt = proj.creators()
    df_cmt = proj.comments()
    exe_time = time.time() - start_time
    print exe_time
    df_time = pd.DataFrame({'pid': [pid], 'exe_time': [exe_time]})

    # save to 'sqlite'
    def _save_df():
        df_proj.to_sql(name = 'projects', con = conn_proj, if_exists = 'append', index = False)
        df_rew.to_sql(name = 'rewards', con = conn_rew, if_exists = 'append', index = False)
        df_upd.to_sql(name = 'updates', con = conn_upd, if_exists = 'append', index = False)
        df_faq.to_sql(name='faqs', con=conn_faq, if_exists='append', index=False)
        df_cmt.to_sql(name = 'comments', con = conn_cmt, if_exists = 'append', index = False)
        df_time.to_sql(name = 'exe_time', con = conn_time, if_exists = 'append', index = False)
        # record what already be loaded
        record.save_record(pids[id], id, proj.total_cmt, proj.count_visible_cmt)
    # put it in a queue then get a permission
    crawler.q.put(_save_df())
    the_queue.get()

# crawling one by one

# while id_lst:
#     id = id_lst.pop()
#     crawler(id)

# crawling by multiprocessing
def worker(queue):
    print os.getpid(),' working'
    crawler.q = queue

try:
    the_queue = Queue()
    pool = Pool(cpu_count() * 2, worker,[the_queue])  # Creates a Pool with cpu_count * 2 threads.
    pool.imap(crawler, id_lst)
    pool.close()
except Exception as e:
    print e
    traceback.print_exc()
    print get_current_datetime()

conn_proj.close()
conn_rew.close()
conn_upd.close()
conn_faq.close()
conn_cmt.close()
conn_time.close()

# # def crawler(id):
# #     pid = random(1,5)
# #     crawler.the_queue.put('Doing: ' + str(pid))
#
# id_lst=range(10)
# the_queue = Queue()
# pool = Pool(cpu_count() * 2, worker,[the_queue])  # Creates a Pool with cpu_count * 2 threads.
# pool.map(crawler, id_lst)
# pool.close()

# EXPERIMENT
#
# import os
# import multiprocessing as mp
# import time
# from random import randint
#
# def crawler(x):
#     print os.getpid(), ' working ', str(x)
#     a=x*x*x
#     t=randint(3,10)
#     time.sleep(t)
#     print str(x), ' slept ', str(t),'s'
#     print os.getpid(), '-'+str(x)+' finished!'
#     crawler.q.put('Ask to save ' + str(x))
#     print the_queue.get()
#
# def f_init(q):
#     print os.getpid(), ' working'
#     crawler.q = q
#
# jobs = range(1,6)
#
# the_queue = mp.Queue()
# p = mp.Pool(3, f_init, [the_queue])
# p.imap(crawler, jobs)
# p.close()

