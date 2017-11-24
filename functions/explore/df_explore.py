import pandas as pd
import re

def df_explore(list_soup, goal):

    df = pd.DataFrame({
        'pid': [],
        'backers_count': [],
        'percent_raised': [],
        'proj_url': [],
        'category': [],
        'goal': [],
        'title': [],
        'creator': [],
        'creator_link': []
    })

    if list_soup != None:
        plist = list_soup.find_all('div', class_='js-track-project-card')

        for i in range(len(plist)):
            try:
                pid = plist[i].get('data-project_pid')
                backers_count = plist[i].get('data-project_backers_count')
                percent_raised = plist[i].get('data-project_percent_raised')
                proj_url = plist[i].find('a').get('href').split('?')[0]
                category = re.sub(r'^https://www.kickstarter.com/discover/categories/', '', plist[i].find_all('a')[1].get('href')).split('?')[0]
                title = re.sub('[:$]', '', plist[i].find_all('a')[2].text)
                creator = plist[i].find_all('span')[1].text
                creator_link = plist[i].find_all('a')[3].get('href')
            except Exception as e:
                print e

            df_temp = pd.DataFrame({
                'pid': [pid],
                'backers_count': [backers_count],
                'percent_raised': [percent_raised],
                'proj_url': [proj_url],
                'category': [category],
                'goal': [goal],
                'title': [title],
                'creator': [creator],
                'creator_link': [creator_link]
            })
            df = df.append(df_temp)

    return df