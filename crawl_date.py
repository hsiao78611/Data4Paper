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

import ks.individual.proj_crawler
import ks.utils.renewip as new
import ks.utils.record as rec
import ks.utils.getlink
import ks.utils.useragents as ua


# list of successful projects
proj_lnks = list(ks.utils.getlink.proj_links()['link'])
pids = list(ks.utils.getlink.proj_links()['pid'])

# create a directory
directory = os.getcwd() + '/' + 'RECORD' # datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
if not os.path.exists(directory):
    os.makedirs(directory)

# Create connections.
conn_date_rew = sqlite3.connect(directory + '/' + 'date_rew.db')
conn_date_fund = sqlite3.connect(directory + '/' + 'date_fund.db')

# randomise crawling order
proj_lst = range(len(proj_lnks))
random.shuffle(proj_lst)

# if there exists the record, load it.
# then remove(pop) the index of crawled data
count_num = 0
record = rec.Record('record_date')
rec_df = record.get_record()
if not rec_df.empty:
    rec_index = list(set(list(rec_df['index'])))
    count_num = len(rec_index)
    while rec_index:
        proj_lst.remove(rec_index.pop())
    # now proj_lst only has uncrawl cases

def crawler(work_lst):
    while work_lst:
        id = work_lst.pop()
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

        try:
            proj_start_date = proj_soup.find('div', class_='NS_campaigns__funding_period').time.get('datetime')
            proj_end_date = proj_soup.find('div', class_='NS_campaigns__funding_period').time.find_next().get('datetime')
        except Exception as e:
            print e
            time.sleep(2)
            proj_start_date = proj_soup.find('div', class_='NS_campaigns__funding_period').time.get('datetime')
            proj_end_date = proj_soup.find('div', class_='NS_campaigns__funding_period').time.find_next().get('datetime')

        # reward
        rew_soup = proj_soup.find('div', class_='NS_projects__rewards_list js-project-rewards')
        rew_item = rew_soup.find_all(class_ = 'hover-group')

        df_rew = pd.DataFrame({
            'pid': [],
            'rew_id': [],
            'rew_amount_required': [],
            'rew_backer_limit': [],
            'rew_backer_count': [],
            'rew_delivery': [],
            })

        for rew in range(len(rew_item)):
            limit = rew_item[rew].find(class_ = 'pledge__limit')
            rew_id = rew
            rew_amount_required = int(re.sub('[^\d]', '', rew_item[rew].find(class_='money').text))
            rew_backer_limit = limit.text.strip() if limit != None else None
            rew_backer_count = int(re.sub('[^\d]', '', rew_item[rew].find(class_='pledge__backer-count').text))
            ed_date = rew_item[rew].find("time")
            rew_delivery = ed_date.get('datetime') if ed_date != None else None

            rew_temp = pd.DataFrame({
                'pid': [pid],
                'rew_id': [rew_id],
                'rew_amount_required': [rew_amount_required],
                'rew_backer_limit': [rew_backer_limit],
                'rew_backer_count': [rew_backer_count],
                'rew_delivery': [rew_delivery],
                })
            df_rew = df_rew.append(rew_temp)

        # dataframe
        df_proj = pd.DataFrame({
            'pid': [pid],
            'proj_url': [proj_lnks[id]],
            'proj_start_date': [proj_start_date],
            'proj_end_date': [proj_end_date],
            })

        # record what already be loaded
        count_num = count_num + 1
        record.save_record(proj_lnks[id], id, len(rew_item), count_num)

        # save to 'sqlite'
        df_rew.to_sql(name='date_reward', con=conn_date_rew, if_exists='append', index=False)
        df_proj.to_sql(name='date_funding', con=conn_date_fund, if_exists='append', index=False)

        print 'finished: ' + str(count_num) + ' ' + proj_lnks[id]

        # renew a connection
        if count_num % 1000 == 0:
            new.renew_connection()

conn_date_rew.close()
conn_date_fund.close()
