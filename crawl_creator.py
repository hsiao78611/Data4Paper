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
conn_proj = sqlite3.connect(directory + '/' + 'proj.db')
conn_rew = sqlite3.connect(directory + '/' + 'rew.db')
conn_upd = sqlite3.connect(directory + '/' + 'upd.db')
conn_faq = sqlite3.connect(directory + '/' + 'faq.db')
# conn_crt = sqlite3.connect(directory + '/' + 'crt.db')
conn_cmt = sqlite3.connect(directory + '/' + 'cmt.db')
conn_time = sqlite3.connect(directory + '/' + 'time.db')

# randomise crawling order
proj_lst = range(len(crt_lnks))
random.shuffle(proj_lst)

# if there exists the record, load it.
# then remove(pop) the index of crawled data
record = rec.Record('record_individual')
rec_df = record.get_record()
if rec_df != False:
    rec_index = list(set(list(rec_df['index'])))
    while rec_index:
        proj_lst.remove(rec_index.pop())

while proj_lst:
    pid = proj_lst.pop()

    # make an identification
    proj_id = 'proj_' + str(pid)

    # used to record processing time
    start_time = time.time()

    proj = ks.individual.proj_crawler.Campaign(proj_lst[pid], pid)
    print 'loading ' + proj_id + ': ' + crt_lnks[pid]

    # dataframe
    df_proj = proj.project_rewards()[0]
    df_rew = proj.project_rewards()[1]
    df_upd = proj.updates()
    df_faq = proj.faqs()
    # df_crt = proj.creators()
    df_cmt = proj.comments()
    exe_time = time.time() - start_time
    print exe_time
    df_time = pd.DataFrame({'proj_id': [proj_id], 'exe_time': [exe_time]})

    # record what already be loaded
    record.save_record(proj_lst[pid], pid, proj.total_cmt, proj.count_visible_cmt)

    # save to 'sqlite'
    df_proj.to_sql(name = 'projects', con = conn_proj, if_exists = 'append', index = False)
    df_rew.to_sql(name = 'rewards', con = conn_rew, if_exists = 'append', index = False)
    df_upd.to_sql(name = 'updates', con = conn_upd, if_exists = 'append', index = False)
    df_faq.to_sql(name='updates', con=conn_faq, if_exists='append', index=False)
    # df_crt.to_sql(name='updates', con=conn_crt, if_exists='append', index=False)
    df_cmt.to_sql(name = 'comments', con = conn_cmt, if_exists = 'append', index = False)
    df_time.to_sql(name = 'exe_time', con = conn_time, if_exists = 'append', index = False)

    time.sleep(randint(1, 5))
    # renew a connection
    new.renew_connection()

conn_proj.close()
conn_rew.close()
conn_upd.close()
conn_faq.close()
# conn_crt.close()
conn_cmt.close()
conn_time.close()