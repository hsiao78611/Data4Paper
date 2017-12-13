import pandas as pd
import re

def df_backed(bac_soup, cid):

    df = pd.DataFrame({
        'cid': [],
        'pid': [],
        'backers_count': [],
        'percent_raised': [],
        'link': [],
        'title': [],
        'creator': [],
        'creator_link': [],
        'project_state': []
    })

    if (bac_soup != None) & (bac_soup != 'non-exist'):
        plist = bac_soup.find_all('div', class_='js-track-project-card')

        for i in range(len(plist)):
            try:
                pid = str(plist[i].get('data-project_pid'))
                backers_count = plist[i].get('data-project_backers_count')
                percent_raised = plist[i].get('data-project_percent_raised')
                link = plist[i].find('a').get('href').split('?')[0]
                title = plist[i].find('a', class_='soft-black hover-text-underline').text
                project_state = plist[i].get('data-project_state')
                crt_name = plist[i].find('span', class_='bold')
                creator = crt_name.text if crt_name != None else plist[i].find('a', class_='soft-black hover-text-underline medium').text
                creator_link = plist[i].find_all('a')[-1].get('href') if crt_name != None else plist[i].find('a', class_='soft-black hover-text-underline medium').get('href').split('?')[0]
            except Exception as e:
                print 'backed ' + cid + ' of project may have a problem.'
                print e

            df_temp = pd.DataFrame({
                'cid': [cid],
                'pid': [pid],
                'backers_count': [backers_count],
                'percent_raised': [percent_raised],
                'link': [link],
                'title': [title],
                'project_state': [project_state],
                'creator': [creator],
                'creator_link': [creator_link]
            })
            df = df.append(df_temp)

    return df