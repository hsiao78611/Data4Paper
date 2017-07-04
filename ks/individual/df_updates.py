import pandas as pd
import re

def df_updates(upd_soup, id):
    upd_item = upd_soup.find_all(class_='timeline__item')

    df = pd.DataFrame(
        {'proj_id': [],
         'upd_number': [],
         'upd_date': [],
         'upd_title': [],
         'upd_comment_count': [],
         'upd_like_count': [],
         'upd_backer_only': []
         })

    for upd in range(len(upd_item)):
        try:
            post_meta = upd_item[upd].find_all(class_='grid-post__metadata')[0]
            comment_count = re.search('(\d+?) Comment', post_meta.text)
            like_count = re.search('(\d+?) like', post_meta.text)

            proj_id = 'proj_' + str(id)
            upd_number = upd
            upd_date = upd_item[upd].find('time').get('datetime')
            upd_title = upd_item[upd].find('h2').text.strip()
            upd_comment_count = int(comment_count.group(1)) if comment_count != None else 0
            upd_like_count = int(like_count.group(1)) if like_count != None else 0
            upd_backer_only = True if post_meta.find('b') != None else False
        except Exception as e:
            print 'update '+str(upd)+' of proj_list ' + str(id) + ' may have a problem.'
            print e
            break

        upd_temp = pd.DataFrame(
            {'proj_id': [proj_id],
             'upd_number' : [upd_number],
             'upd_date' : [upd_date],
             'upd_title' : [upd_title],
             'upd__comment_count' : [upd_comment_count],
             'upd__like_count' : [upd_like_count],
             'upd_backer_only' : [upd_backer_only]
            })

        df = df.append(upd_temp)

    return df