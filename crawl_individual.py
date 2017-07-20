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
import ks.utils.getlink

from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count


# the list is crawled by GoogleScraper and precessed by ProjectList.py
# proj_lnks = ['https://www.kickstarter.com/projects/312002206/the-worlds-smallest-garden-0'
#              ,'https://www.kickstarter.com/projects/hello/sense-know-more-sleep-better'
#              ]

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
conn_proj = sqlite3.connect(directory + '/' + 'proj.db')
conn_rew = sqlite3.connect(directory + '/' + 'rew.db')
conn_upd = sqlite3.connect(directory + '/' + 'upd.db')
conn_faq = sqlite3.connect(directory + '/' + 'faq.db')
conn_cmt = sqlite3.connect(directory + '/' + 'cmt.db')
conn_time = sqlite3.connect(directory + '/' + 'time.db')


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
    df_proj = proj.project_rewards()[0]
    df_rew = proj.project_rewards()[1]
    df_upd = proj.updates()
    df_faq = proj.faqs()
    # df_crt = proj.creators()
    df_cmt = proj.comments()
    exe_time = time.time() - start_time
    print exe_time
    df_time = pd.DataFrame({'pid': [pid], 'exe_time': [exe_time]})

    # record what already be loaded
    record.save_record(id_lst[id], id, proj.total_cmt, proj.count_visible_cmt)

    # save to 'sqlite'
    df_proj.to_sql(name = 'projects', con = conn_proj, if_exists = 'append', index = False)
    df_rew.to_sql(name = 'rewards', con = conn_rew, if_exists = 'append', index = False)
    df_upd.to_sql(name = 'updates', con = conn_upd, if_exists = 'append', index = False)
    df_faq.to_sql(name='faqs', con=conn_faq, if_exists='append', index=False)
    df_cmt.to_sql(name = 'comments', con = conn_cmt, if_exists = 'append', index = False)
    df_time.to_sql(name = 'exe_time', con = conn_time, if_exists = 'append', index = False)

    time.sleep(randint(1, 5))
    # renew a connection
    new.renew_connection()

# crawling one by one
while id_lst:
    id = id_lst.pop()
    crawler(id)

# crawling by multiprocessing
# pool = Pool(cpu_count() * 2)  # Creates a Pool with cpu_count * 2 threads.
# pool.map(crawler, id_lst)

conn_proj.close()
conn_rew.close()
conn_upd.close()
conn_faq.close()
conn_cmt.close()
conn_time.close()