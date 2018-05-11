import os
import sqlite3
import re
from datetime import datetime
import random
from random import randint
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import urllib2
import time
import numpy

import packages.individual.proj_crawler
import packages.utils.renewip as new
import packages.utils.record as rec
import packages.utils.getlink
import packages.utils.useragents as ua

# thread-based Pool
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from multiprocessing import Queue
import traceback

# list of successful projects
proj_lnks = list(packages.utils.getlink.proj_links('need_fd_1227')['proj_url'])
pids = list(packages.utils.getlink.proj_links('need_fd_1227')['pid'])

# create a directory
directory = os.getcwd() + '/' + 'RECORD' # datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists(directory):
    os.makedirs(directory)

# Create connections.
# conn_date_rew = sqlite3.connect(directory + '/' + 'date_rew.db')
conn_date_fund = sqlite3.connect(directory + '/' + 'date_fund.db', timeout=10.0, check_same_thread=False)

# randomise crawling order
proj_lst = range(len(proj_lnks))
random.shuffle(proj_lst)

# if there exists the record, load it.
# then remove(pop) the index of crawled data
global count_num
count_num = 0
record = rec.Record('record_need_fd_1227')
rec_df = record.get_record()
if not rec_df.empty:
    rec_index = list(set(list(rec_df['index'])))
    count_num = len(rec_index)
    while rec_index:
        proj_lst.remove(rec_index.pop())
    print count_num
    # now proj_lst only has uncrawl cases

# while proj_lst:
#     id = proj_lst.pop()
#     pid = pids[id]
#     # make an identification
#
#     # get a random agent
#     agents_lst = ua.get_user_agents()
#     user_agent = list(agents_lst)[randint(0, len(agents_lst) - 1)]
#     headers = {'User-Agent': user_agent}
#
#     request = urllib2.Request(proj_lnks[id], None, headers)
#     response = urllib2.urlopen(request)
#     strainer = SoupStrainer('main', attrs={'role': 'main'})
#     proj_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
#     response.close()
#
#     # data frames
#     df_proj = pd.DataFrame({
#         'pid': [],
#         'proj_url': [],
#         'proj_start_date': [],
#         'proj_end_date': [],
#     })
#     # df_rew = pd.DataFrame({
#     #     'pid': [],
#     #     'rew_id': [],
#     #     'rew_amount_required': [],
#     #     'rew_backer_limit': [],
#     #     'rew_backer_count': [],
#     #     'rew_delivery': [],
#     # })
#
#     try:
#         proj_start_date = proj_soup.find('div', class_='NS_campaigns__funding_period').time.get('datetime')
#         proj_end_date = proj_soup.find('div', class_='NS_campaigns__funding_period').time.find_next().get('datetime')
#
#         # # reward
#         # rew_soup = proj_soup.find('div', class_='NS_projects__rewards_list js-project-rewards')
#         # rew_item = rew_soup.find_all(class_ = 'hover-group')
#         #
#         # for rew in range(len(rew_item)):
#         #     limit = rew_item[rew].find(class_ = 'pledge__limit')
#         #     rew_id = rew
#         #     rew_amount_required = int(re.sub('[^\d]', '', rew_item[rew].find(class_='money').text))
#         #     rew_backer_limit = limit.text.strip() if limit != None else None
#         #     rew_backer_count = int(re.sub('[^\d]', '', rew_item[rew].find(class_='pledge__backer-count').text))
#         #     ed_date = rew_item[rew].find('time')
#         #     rew_delivery = ed_date.get('datetime') if ed_date != None else None
#         #
#         #     rew_temp = pd.DataFrame({
#         #         'pid': [pid],
#         #         'rew_id': [rew_id],
#         #         'rew_amount_required': [rew_amount_required],
#         #         'rew_backer_limit': [rew_backer_limit],
#         #         'rew_backer_count': [rew_backer_count],
#         #         'rew_delivery': [rew_delivery],
#         #         })
#         #     df_rew = df_rew.append(rew_temp)
#     except Exception as e:
#         print e
#         print proj_lnks[id]
#         time.sleep(3)
#         # https://www.kickstarter.com/projects/100105516/particule-a-2-3d-mobile-survival-game-with-multipl
#         try:
#             if proj_soup.find('div', attrs={'id': 'hidden_project'}).get('id') == 'hidden_project':
#                 print 'hidden project: ' + proj_lnks[id]
#                 # rew_item = []
#                 # rew_temp = pd.DataFrame({
#                 #     'pid': [pid],
#                 #     'rew_id': ['hidden project'],
#                 #     'rew_amount_required': ['hidden project'],
#                 #     'rew_backer_limit': ['hidden project'],
#                 #     'rew_backer_count': ['hidden project'],
#                 #     'rew_delivery': ['hidden project'],
#                 # })
#                 # df_rew = df_rew.append(rew_temp)
#                 proj_start_date = 'hidden project'
#                 proj_end_date = 'hidden project'
#         except Exception as e:
#             print e
#             print 'other exception'
#
#     df_proj = pd.DataFrame({
#         'pid': [pid],
#         'proj_url': [proj_lnks[id]],
#         'proj_start_date': [proj_start_date],
#         'proj_end_date': [proj_end_date],
#         })
#
#     # record what already be loaded
#     count_num = count_num + 1
#     record.save_record(proj_lnks[id], id)#, len(rew_item), count_num)
#
#     # save to 'sqlite'
#     # df_rew.to_sql(name='date_reward', con=conn_date_rew, if_exists='append', index=False)
#     df_proj.to_sql(name='date_funding', con=conn_date_fund, if_exists='append', index=False)
#
#     print 'finished: ' + str(count_num) + ' ' + proj_lnks[id]

    # time.sleep(randint(0, 2))
    # # renew a connection
    # if count_num % 1000 == 0:
    #     new.renew_connection()


def crawler(id):
    pid = pids[id]
    # make an identification

    # get a random agent
    agents_lst = ua.get_user_agents()
    user_agent = list(agents_lst)[randint(0, len(agents_lst) - 1)]
    headers = {'User-Agent': user_agent}

    request = urllib2.Request(proj_lnks[id], None, headers)
    response = urllib2.urlopen(request)
    strainer = SoupStrainer('main', attrs={'role': 'main'})
    proj_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
    response.close()

    # data frames
    df_proj = pd.DataFrame({
        'pid': [],
        'proj_url': [],
        'proj_start_date': [],
        'proj_end_date': [],
    })

    try:
        print 'loading project: ' + proj_lnks[id]
        proj_start_date = proj_soup.find('div', class_='NS_campaigns__funding_period').time.get('datetime')
        proj_end_date = proj_soup.find('div', class_='NS_campaigns__funding_period').time.find_next().get('datetime')
    except Exception as e:
        try:
            if proj_soup.find('div', attrs={'id': 'hidden_project'}).get('id') == 'hidden_project':
                print 'hidden project: ' + proj_lnks[id]
                proj_start_date = 'hidden project'
                proj_end_date = 'hidden project'
        except Exception as e:
            print e
            proj_start_date = 'other exception'
            proj_end_date = 'other exception'
            print 'other exception'

    df_proj = pd.DataFrame({
        'pid': [pid],
        'proj_url': [proj_lnks[id]],
        'proj_start_date': [proj_start_date],
        'proj_end_date': [proj_end_date],
        })

    def _save_df():
        df_proj.to_sql(name='date_fund', con=conn_date_fund, if_exists='append', index=False)
        print 'finished: ' + proj_lnks[id]
        record.save_record(proj_lnks[id], id)  # , len(rew_item), count_num)

    # crawling one by one
    _save_df()

# crawling one by one
while proj_lst:
    id = proj_lst.pop()
    crawler(id)

#     # crawling via multiprocessing and queue
#     # put it in a queue then get a permission
#     crawler.que.put(_save_df())
#
# # crawling via multiprocessing and queue
# def worker(queue):
#     crawler.que = queue
#
# try:
#     the_queue = Queue()
#     pool = Pool(cpu_count() + 2, worker,[the_queue])  # Can create a Pool with cpu_count * 2 threads.
#     pool.imap(crawler, proj_lst)
#     pool.close()
#     while True:
#         the_queue.get(True)
# except Exception as e:
#     print e
#     traceback.print_exc()

# conn_date_rew.close()
conn_date_fund.close()
