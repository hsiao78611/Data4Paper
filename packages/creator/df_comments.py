import pandas as pd
import re

def df_comments(cmt_soup, cid):

    df = pd.DataFrame(
        {'cid': [],
         'cmt_id': [],
         'cmt_datetime': [],
         'cmt_proj_title': [],
         'cmt_content': [],
         'cmt_url': []
         })

    if cmt_soup != None:
        cmt_item = cmt_soup.find_all('li', class_='activity-comment-project')
        rh = lambda html: html.get_text()

        for cmt in range(len(cmt_item)):
            try:
                cmt_id = cmt
                cmt_datetime = cmt_item[cmt].find('time').get('datetime')
                cmt_proj_title = cmt_item[cmt].find('b').text
                cmt_content = cmt_item[cmt].find_all('p')[0].text
                cmt_url = cmt_item[cmt].find('a').get('href')
            except Exception as e:
                print 'comment '+ str(cmt) +' of creator ' + cid + ' may have a problem.'
                print e
                break

            cmt_temp = pd.DataFrame(
            {'cid': [cid],
             'cmt_id' : [cmt_id],
             'cmt_datetime' : [cmt_datetime],
             'cmt_proj_title' : [cmt_proj_title],
             'cmt_content' : [cmt_content],
             'cmt_url' : [cmt_url],
            })

        df = df.append(cmt_temp)

    return df