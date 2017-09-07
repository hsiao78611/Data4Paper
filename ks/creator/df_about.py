import pandas as pd
import re

def df_about(abt_soup, cid):
    df = pd.DataFrame({
        'cid': [],
        'name': [],
        'joined_date': [],
        'location': [],
        'backed_count': [],
        'created_count': [],
        'comments_count': [],
        'biography': [],
        'website_list': []
    })

    try:
        name = abt_soup.find('h2', class_='mb2').text.strip()
        joined_date = abt_soup.find('time', class_='js-adjust-time').get('datetime')
        loc_exist = abt_soup.find('span', class_='location').text.strip()
        location = loc_exist if loc_exist != None else None
        backed_count = int(re.sub('[^\d]','',abt_soup.find('span', class_='backed').text))
        crt_exist = abt_soup.find('a', class_='js-created-link')
        created_count = int(re.sub('[^\d]','', crt_exist.text)) if crt_exist != None else None
        cmt_exist = abt_soup.find('a', class_='js-comments-link')
        comments_count = int(re.sub('[^\d]', '', cmt_exist.text)) if cmt_exist != None else None
        biography = abt_soup.find('div', class_='col-full col-sm-15-20 col-md-11-16').text.strip()
        website_list = []
        website_list_html = abt_soup.find('ul', class_='menu-submenu mb6').find_all('li')
        for i in range(len(website_list_html)):
            website_list = website_list + [website_list_html[i].text.strip()]

        df = pd.DataFrame({
            'cid': [cid],
            'name': [name],
            'joined_date': [joined_date],
            'location': [location],
            'backed_count': [backed_count],
            'created_count': [created_count],
            'comments_count': [comments_count],
            'biography': [biography],
            'website_list': [website_list]
        })

    except Exception as e:
        print 'about '+ cid +' of project may have a problem.'
        print e


    return df