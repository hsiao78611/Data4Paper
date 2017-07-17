import ks.utils.getlink
import re
import os
import sqlite3
import pandas as pd

# create a directory
directory = os.getcwd() + '/' + 'RECORD'
if not os.path.exists(directory):
    os.makedirs(directory)

# list of successful projects
proj_lnks = list(ks.utils.getlink.proj_links()['link'])
pids = list(ks.utils.getlink.proj_links()['pid'])

# for date_funding
# create connections of database.
conn_fund = sqlite3.connect(directory + '/' + 'date_fund.db')
new_conn_fund = sqlite3.connect(directory + '/' + 'new_date_fund.db')
df_fund = pd.read_sql_query('SELECT * FROM date_funding', conn_fund)
proj_id = list(df_fund['proj_id'])
id = []
pid = []
while proj_id:
    id = id + [re.sub('[^\d]', '', proj_id.pop())] # in reverse order
while id:
    pid = pid + [pids[int(id.pop())]]

df_proj = pd.DataFrame({
        'pid': pid,
        'proj_url': list(df_fund['proj_url']),
        'proj_start_date': list(df_fund['proj_start_date']),
        'proj_end_date': list(df_fund['proj_end_date'])
        })
conn_fund.close()
new_conn_fund.close()

# for date_reward
# create connections of database.
conn_rew = sqlite3.connect(directory + '/' + 'date_rew.db')
new_conn_rew = sqlite3.connect(directory + '/' + 'new_date_rew.db')
df_rew = pd.read_sql_query('SELECT * FROM date_reward', conn_rew)
rew_proj_id = list(df_rew['proj_id']) # it more than previous one
id = []
pid = []
while rew_proj_id:
    id = id + [re.sub('[^\d]', '', rew_proj_id.pop())] # in reverse order
while id:
    pid = pid + [pids[int(id.pop())]]

rew_temp = pd.DataFrame({
            'pid': pid,
            'rew_id': list(df_rew['rew_number']),
            'rew_amount_required': list(df_rew['rew_amount_required']),
            'rew_backer_limit': list(df_rew['rew_backer_limit']),
            'rew_backer_count': list(df_rew['rew_backer_count']),
            'rew_delivery': list(df_rew['rew_delivery']),
            })

# save to 'sqlite'
df_proj.to_sql(name='date_funding', con=new_conn_fund, if_exists='append', index=False)
rew_temp.to_sql(name='date_reward', con=new_conn_rew, if_exists='append', index=False)

conn_rew.close()
new_conn_rew.close()