import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd

ks_link = 'https://www.kickstarter.com/discover/advanced?ref=discovery_overlay'

session = requests.Session()
response = session.get(ks_link)
strainer = SoupStrainer('div', class_='root-categories')
cat_soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)

cats = cat_soup.find_all('li', class_='category')

def get_category():
    df = pd.DataFrame({'category': [], 'id': []})
    # get slug and id
    for i in range(len(cats)):
        try:
            cat = cats[i].find('a').text
            id = cats[i].find('a').get('data-id')
        except Exception as e:
            print e
            break
        df_temp = pd.DataFrame({'category': [cat], 'id': [id]})
        df = df.append(df_temp)

    return df

# >>> df.iat[14,0]
# u'Theater'
# >>> df.iloc[14][0]
# u'Theater'