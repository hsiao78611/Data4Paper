import pandas as pd
import re

def df_comments(cmt_soup, id):
    cmt_item = cmt_soup.find_all('li', class_ = 'NS_comments__comment')
    rh = lambda html: html.get_text()

    df = pd.DataFrame(
        {'proj_id': [],
         'cmt_id': [],
         'cmt_datetime': [],
         'cmt_profile_id': [],
         'cmt_collaborator': [],
         'cmt_superbaker': [],
         'cmt_content': [],
         'cmt_exe_time_sec': []
         })

    for cmt in range(len(cmt_item)):
        try:
            proj_id = 'proj_' + str(id)
            cmt_id = cmt_item[cmt].get('id') if cmt_item[cmt].get('id') != None else 'comment-earliest'
            cmt_datetime = cmt_item[cmt].find('data').get('data-value')
            cmt_profile_id = cmt_item[cmt].find('a', href=re.compile('/profile/')).get('href').split('/')[-1]
            cmt_collaborator = u'collaborator' in cmt_item[cmt].get('class')
            cmt_superbaker = True if cmt_item[cmt].find('div', class_='superbacker-badge') != None else False
            cmt_content = ''.join(map(rh, cmt_item[cmt].find_all('p')))
        except Exception as e:
            print 'comment '+str(cmt)+' of proj_list ' + str(id) + ' may have a problem.'
            print e
            break

        cmt_temp = pd.DataFrame(
        {'proj_id': [proj_id],
         'cmt_id' : [cmt_id],
         'cmt_datetime' : [cmt_datetime],
         'cmt_profile_id' : [cmt_profile_id],
         'cmt_collaborator' : [cmt_collaborator],
         'cmt_superbaker' : [cmt_superbaker],
         'cmt_content' : [cmt_content]
        })

        df = df.append(cmt_temp)

    return df




