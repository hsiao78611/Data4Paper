import pandas as pd
import re

def df_rewards(rew_soup, id):
    rew_item = rew_soup.find_all(class_ = 'hover-group')

    df = pd.DataFrame(
        {'proj_id': [],
         'rew_number': [],
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

            proj_id = 'proj_' + str(id)
            rew_number = rew
            rew_amount_required = int(re.sub('[^\d]', '', rew_item[rew].find(class_ = 'money').text))
            rew_backer_limit = limit.text.strip() if limit != None else None
            rew_description = rew_item[rew].find_all("p")[1].text
            rew_backer_count = int(re.sub('[^\d]', '', rew_item[rew].find(class_ = 'pledge__backer-count').text))
            rew_delivery = rew_item[rew].find("time").get('datetime')
            rew_ships_to = ship_info[1].text.strip().replace('\n', ' ') if len(ship_info) == 2 else None
        except Exception as e:
            print 'reward '+ str(rew) +' of proj_list ' + str(id) + ' may have a problem.'
            print e
            break

        rew_temp = pd.DataFrame(
            {'proj_id': [proj_id],
             'rew_number': [rew_number],
             'rew_amount_required': [rew_amount_required],
             'rew_backer_limit': [rew_backer_limit],
             'rew_description': [rew_description],
             'rew_backer_count': [rew_backer_count],
             'rew_delivery': [rew_delivery],
             'rew_ships_to': [rew_ships_to]
             })

        df = df.append(rew_temp)

    return df