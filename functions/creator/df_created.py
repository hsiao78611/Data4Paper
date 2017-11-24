import pandas as pd
import re

def df_created(crt_soup, cid):

    df = pd.DataFrame({
        'cid': [],
        'pid': [],
        'no': [],
        'backers_count': [],
        'percent_raised': [],
        'link': [],
        'category': [],
        'title': [],
        'project_state': []
    })

    if (crt_soup != None) & (crt_soup != 'non-exist'):
        plist = crt_soup.find_all('div', class_='js-track-project-card')
        total = len(plist)
        for i in range(total):
            try:
                pid = plist[i].get('data-project_pid')
                no = total - i
                backers_count = plist[i].get('data-project_backers_count')
                percent_raised = plist[i].get('data-project_percent_raised')
                link = plist[i].find('a').get('href').split('?')[0]
                category = re.sub(r'^http://www.kickstarter.com/discover/categories/', '',
                                  plist[i].find('a', class_='navy-600').get('href')).split('?')[0]

                title = re.sub('[:$]', '', plist[i].find('a', class_='navy-700').text)
                project_state = plist[i].get('data-project_state')
            except Exception as e:
                print 'created ' + cid + ' of project may have a problem.'
                print e

            df_temp = pd.DataFrame({
                'cid': [cid],
                'pid': [pid],
                'no': [no],
                'backers_count': [backers_count],
                'percent_raised': [percent_raised],
                'link': [link],
                'category': [category],
                'title': [title],
                'project_state': [project_state],
            })
            df = df.append(df_temp)

    return df