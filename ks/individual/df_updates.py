import pandas as pd
import re

def df_updates(upd_soup, pid):
    upd_item = upd_soup.find_all(class_='timeline__item')
    upd_sys_item = upd_soup.find_all(class_='timeline__divider')

    df = pd.DataFrame(
        {'pid': [],
         'upd_id': [],
         'upd_date': [],
         'upd_title': [],
         'upd_comment_count': [],
         'upd_like_count': [],
         'upd_backer_only': [],
         'upd_url': []
         })

    if upd_item != []:
        total = len(upd_item)
        for upd in range(total):
            try:
                post_meta = upd_item[upd].find_all(class_='grid-post__metadata')[0]
                comment_count = re.search('(\d+?) Comment', post_meta.text)
                like_count = re.search('(\d+?) like', post_meta.text)

                upd_id = pid + '.' + str(total - upd)

                upd_date = upd_item[upd].find('time').get('datetime')
                upd_title = upd_item[upd].find('h2').text.strip()
                upd_comment_count = int(comment_count.group(1)) if comment_count != None else 0
                upd_like_count = int(like_count.group(1)) if like_count != None else 0
                upd_backer_only = True if post_meta.find('b') != None else False

                upd_url = upd_item[upd].find('a').get('href')
            except Exception as e:
                print 'update '+str(upd)+' of project ' + pid + ' may have a problem.'
                print e
                break

            upd_temp = pd.DataFrame(
                {'pid': [pid],
                 'upd_id' : [upd_id],
                 'upd_date' : [upd_date],
                 'upd_title' : [upd_title],
                 'upd__comment_count' : [upd_comment_count],
                 'upd__like_count' : [upd_like_count],
                 'upd_backer_only' : [upd_backer_only],
                 'upd_url': [upd_url]
                })
            df = df.append(upd_temp)

        total_sys = len(upd_sys_item)
        for upd_sys in range(total_sys):
            if (not any('month' in elem for elem in upd_sys_item[upd_sys].get('class'))) \
                    and upd_sys_item[upd_sys].find('div', class_='timeline__divider--month-range') == None:
                try:
                    upd_id = pid + '.sys_' + str(total_sys - upd_sys)
                    upd_sys_date = upd_sys_item[upd_sys].find('time').get('datetime')
                    f3 = upd_sys_item[upd_sys].find('div', class_='f3')
                    f2 = upd_sys_item[upd_sys].find('div', class_='f2')
                    upd_sys_title = f3.text.encode("ascii", "ignore").strip() if f3 != None \
                        else (f2.text.strip() if f2 != None else upd_sys_item[upd_sys].find('b').text)
                except Exception as e:
                    print 'update sys '+str(upd_sys)+' of project ' + pid + ' may have a problem.'
                    print e
                    break

                upd_sys_temp = pd.DataFrame(
                    {'pid': [pid],
                     'upd_id': [upd_id],
                     'upd_date': [upd_sys_date],
                     'upd_title': [upd_sys_title],
                     'upd__comment_count': [None],
                     'upd__like_count': [None],
                     'upd_backer_only': [None],
                     'upd_url': [None]
                     })
                df = df.append(upd_sys_temp)

    return df