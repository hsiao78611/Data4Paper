import ks.main_crawler
from random import randint
import pandas as pd
import os
import time
from datetime import datetime
import sqlite3

# the list is crawled by GoogleScraper and precessed by ProjectList.py
proj_list = ['https://www.kickstarter.com/projects/312002206/the-worlds-smallest-garden-0'
             ,'https://www.kickstarter.com/projects/hello/sense-know-more-sleep-better'
             ]

id_start_from = 0
# create a directory
directory = os.getcwd() + '/' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

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
conn_cmt = sqlite3.connect(directory + '/' + 'cmt.db')
conn_time = sqlite3.connect(directory + '/' + 'time.db')

for id in range(len(proj_list)):
    proj_id = 'proj_' + str(id_start_from + id)
    start_time = time.time()


    proj = ks.main_crawler.Campaign(proj_list[id], id_start_from + id)
    print 'loading ' + proj_id + ': ' + proj_list[id]

    # dataframe
    df_proj = proj.project()
    df_rew = proj.rewards()
    df_upd = proj.updates()
    df_cmt = proj.comments()
    exe_time = time.time() - start_time
    print exe_time
    df_time = pd.DataFrame({'proj_id': [proj_id], 'exe_time': [exe_time]})

    # save to 'csv'
    # save(df_proj, 'projects.csv')
    # save(df_rew, 'rewards.csv')
    # save(df_upd, 'updates.csv')
    # save(df_cmt, 'comments.csv')
    # save(df_time, 'exe_time.csv')

    # save to 'sqlite'
    df_proj.to_sql(name = 'projects', con = conn_proj, if_exists = 'append', index = False)
    df_rew.to_sql(name = 'rewards', con = conn_rew, if_exists = 'append', index = False)
    df_upd.to_sql(name = 'updates', con = conn_upd, if_exists = 'append', index = False)
    df_cmt.to_sql(name = 'comments', con = conn_cmt, if_exists = 'append', index = False)
    exe_time.to_sql(name = 'exe_time', con = conn_time, if_exists = 'append', index = False)

    time.sleep(randint(1, 5))

conn_proj.close()
conn_rew.close()
conn_upd.close()
conn_cmt.close()
conn_time.close()