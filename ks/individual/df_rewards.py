import pandas as pd
import re

def df_rewards(rew_soup, pid):
    rew_item = rew_soup.find_all(class_ = 'hover-group')

    df = pd.DataFrame(
        {'id': [],
         'rew_id': [],
         'rew_amount_required': [],
         'rew_backer_limit': [],
         'rew_description': [],
         'rew_backer_count': [],
         'rew_delivery': [],
         'rew_ships_to': []
         })

    for rew in range(len(rew_item)):
        try:
            limit = rew_item[rew].find(class_ = 'pledge__limit')
            ship_info = rew_item[rew].find_all(class_ = 'pledge__detail-info')
            rew_id = rew
            rew_amount_required = int(re.sub('[^\d]', '', rew_item[rew].find(class_ = 'money').text))
            rew_backer_limit = limit.text.strip() if limit != None else None
            rew_description = rew_item[rew].find_all("p")[1].text
            rew_backer_count = int(re.sub('[^\d]', '', rew_item[rew].find(class_ = 'pledge__backer-count').text))
            ed_date = rew_item[rew].find("time")
            rew_delivery = ed_date.get('datetime') if ed_date != None else None
            rew_ships_to = ship_info[1].text.strip().replace('\n', ' ') if len(ship_info) == 2 else None
        except Exception as e:
            print 'reward '+ str(rew) +' of project ' + pid + ' may have a problem.'
            print e
            break

        rew_temp = pd.DataFrame(
            {'pid': [pid],
             'rew_id': [rew_id],
             'rew_amount_required': [rew_amount_required],
             'rew_backer_limit': [rew_backer_limit],
             'rew_description': [rew_description],
             'rew_backer_count': [rew_backer_count],
             'rew_delivery': [rew_delivery],
             'rew_ships_to': [rew_ships_to]
             })
        df = df.append(rew_temp)

    return df