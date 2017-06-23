import ks.crawler
from random import randint
import pandas as pd
import os
import time
from datetime import datetime

# the list is crawled by GoogleScraper and precessed by ProjectList.py
proj_list = ['https://www.kickstarter.com/projects/312002206/the-worlds-smallest-garden-0'
             ,'https://www.kickstarter.com/projects/hello/sense-know-more-sleep-better'
             ]

id_start_from = 0
directory = os.getcwd() + '/' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

if not os.path.exists(directory):
    os.makedirs(directory)

def save(df, file_name):
    if not os.path.isfile(directory + '/' + file_name): # if file does not exist
        df.to_csv(directory + '/' + file_name, index=False, encoding='utf-8-sig')
    else:  # else it exists so append without writing the header
        df.to_csv(directory + '/' + file_name, mode='a', index=False, header=False, encoding='utf-8-sig')

for id in range(len(proj_list)):
    proj_id = 'proj_' + str(id_start_from + id)
    start_time = time.time()


    proj = ks.crawler.Campaign(proj_list[id], id_start_from + id)
    print 'loading ' + proj_id + ': ' + proj_list[id]

    # dataframe
    df_proj = proj.project()
    df_rew = proj.rewards()
    df_upd = proj.updates()
    df_cmt = proj.comments()
    exe_time = time.time() - start_time
    print exe_time
    df_time = pd.DataFrame({'proj_id': [proj_id], 'exe_time': [exe_time]})

    # save
    save(df_proj, 'projects.csv')
    save(df_rew, 'rewards.csv')
    save(df_upd, 'updates.csv')
    save(df_cmt, 'comments.csv')
    save(df_time, 'exe_time.csv')

    time.sleep(randint(1, 5))