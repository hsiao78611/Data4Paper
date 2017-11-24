import urllib2
from random import randint
import time
from bs4 import BeautifulSoup, SoupStrainer
import signal
import pandas as pd

import packages.utils.renewip as new
import packages.utils.scrollpage as sc
import packages.utils.setwebdriver as sw
import packages.utils.useragents as ua
from packages.individual.df_comments import df_comments
from packages.individual.df_faqs import df_faqs
from packages.individual.df_project import df_project
from packages.individual.df_rewards import df_rewards
from packages.individual.df_updates import df_updates

def update(upd_link, pid, upd_id):

    # get a random agent
    agents_lst = ua.get_user_agents()
    user_agent = list(agents_lst)[randint(0, len(agents_lst) - 1)]
    headers = {'User-Agent': user_agent}

    # communicate with TOR via a local proxy (privoxy)
    new.renew_connection()

    # Speeding up BeautifulSoup by using SoupStrainer and lxml parser
    request = urllib2.Request(upd_link, None, headers)
    response = urllib2.urlopen(request)
    upd_soup = BeautifulSoup(response, 'lxml')

    response.close()

    df = pd.DataFrame(
        {'pid': [],
         'upd_id': [],
         'upd_url': [],
         'upd_body': []
         })

    try:
        upd_body = unicode(upd_soup.find('div', class_='body readability responsive-media formatted-lists'))
    except Exception as e:
        print 'update ' + str(upd) + ' of project ' + pid + ' may have a problem.'
        print e

    upd_temp = pd.DataFrame(
        {'pid': [pid],
         'upd_id': [upd_id],
         'upd_url': [upd_link],
         'upd_body': [upd_body],
         })
    df = df.append(upd_temp)

    return df

