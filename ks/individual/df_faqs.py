import pandas as pd
import re

def df_faqs(faq_soup, pid):
    faq_item = faq_soup.find_all('li', class_='js-faq')

    df = pd.DataFrame({
        'pid': [],
        'faq_id': [],
        'faq_date': [],
        'faq_title': [],
        'faq_content': []
    })

    if faq_item != []:
        total = len(faq_item)
        for faq in range(total):
            try:
                faq_id = pid + '.' + str(total - faq)
                faq_title = faq_item[faq].find('a', class_='js-faq-question-toggle').text.strip()
                faq_content = faq_item[faq].find('div', class_='type-14 navy-700 normal').text.strip()
                faq_date = faq_item[faq].find('time').get('datetime')
            except Exception as e:
                print 'faq '+str(faq)+' of project ' + pid + ' may have a problem.'
                print e
                break

            faq_temp = pd.DataFrame({
                'pid': [pid],
                'faq_id': [faq_id],
                'faq_date': [faq_date],
                'faq_title': [faq_title],
                'faq_content': [faq_content]
            })
            df = df.append(faq_temp)

    return df