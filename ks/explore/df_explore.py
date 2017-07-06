import pandas as pd
import re

def df_explore(list_soup):
    plist = list_soup.find_all('div', class_='js-track-project-card')

    df = pd.DataFrame({
        'pid': [],
        'backers': [],
        'percent': [],
        'link': [],
        'category': [],
        'title': [],
        'creater': [],
        'c_link': []
    })

    for i in range(len(plist)):
        try:
            pid = plist[i].get('data-project_pid')
            backers = plist[i].get('data-project_backers_count')
            percent = plist[i].get('data-project_percent_raised')
            link = plist[i].find('a').get('href').split('?')[0]
            category = re.sub('^https://www.kickstarter.com/discover/categories/', '', plist[i].find_all('a')[1].get('href').split('?')[0])
            title = re.sub('[:$]', '', plist[0].find_all('a')[2].text)
            creater = plist[i].find_all('span')[1].text
            c_link = plist[i].find_all('a')[3].get('href')
        except Exception as e:
            print e

        df_temp = pd.DataFrame({
            'pid': [pid],
            'backers': [backers],
            'percent': [percent],
            'link': [link],
            'category': [category],
            'title': [title],
            'creater': [creater],
            'c_link': [c_link]
        })
        df = df.append(df_temp)

    return df

    # >>> df.iloc[0][0]
    # '287'
    # >>> df.iat[0,0]
    # '287'