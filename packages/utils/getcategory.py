import requests
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import re

ks_link = 'https://www.kickstarter.com/discover/advanced?state=successful&category_id=1&sort=end_date&seed=2498718&page=1'

session = requests.Session()
response = session.get(ks_link)
strainer = SoupStrainer('div', class_='subcategories_container full-height absolute border-box pt3 pt5-sm pb3 pb7-sm pl3 pl7-sm pr3 pr5-sm')
cat_soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)
par = cat_soup.find_all('ul', class_='list-inline')

def get_category():
    df = pd.DataFrame({'category': [], 'id': [], 'parent':[]})
    for i in range(len(par)):
        par_id = re.sub('[^\d]', '', par[i].get('id'))
        parent = re.sub('More in\n', '', par[i].find('li', class_='title').text.strip())
        cats = par[i].find_all('li', class_='subcategory')
        for j in range(len(cats)):
            try:
                cat = cats[j].find('a').text
                id = re.search('(?<=id\":)\d+', cats[j].get('data-category')).group(0)
            except Exception as e:
                print e
                break
            df_temp = pd.DataFrame({'category': [cat], 'id': [id], 'parent': [parent], 'par_id': [par_id]})
            df = df.append(df_temp)

    return df