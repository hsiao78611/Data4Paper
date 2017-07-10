import pandas as pd
import re

def df_project(proj_soup, pid):
    try:
        proj_title = proj_soup.find('a', class_ = 'hero__link').text
            # soup_proj.find('meta', attrs={'property': 'og:title'}).get('content')
        proj_description = proj_soup.find_all('span', class_ = 'relative')[1].text.strip()
            # soup_proj.find('meta', attrs={'property': 'og:description'}).get('content')
        proj_url = 'https: // www.kickstarter.com' + proj_soup.find('a', class_ = 'hero__link').get('href')
            # soup_proj.find('meta', attrs={'property': 'og:url'}).get('content')
        proj_goal = int(re.sub('[^\d]', '', proj_soup.find(class_='medium').text))
        proj_amount_pledged = int(re.sub('[^\d]', '', proj_soup.find('h3', class_='mb0').text))
        proj_currency = re.search('of (.+?)\d', proj_soup.find(class_='medium').text).group(1)
        proj_start_date = proj_soup.find('div', class_='NS_campaigns__funding_period').time.get('datetime')
        proj_end_date = proj_soup.find('div', class_='NS_campaigns__funding_period').time.find_next().get('datetime')
        proj_category = re.split('/|\?', proj_soup.find(class_='mr3', href=re.compile('/discover/categories/')).get('href'))[3]
        proj_subcategory = proj_soup.find(class_='mr3', href=re.compile('/discover/categories/')).text.strip()
        proj_backer_count = int(re.sub('[^\d]', '', proj_soup.find_all('h3', class_='mb0')[1].text))
        proj_comment_count = int(re.sub('[^\d]', '', proj_soup.find(class_='js-load-project-comments').text))
        proj_update_count = int(re.sub('[^\d]', '', proj_soup.find(class_='js-load-project-updates').text))
        find_faq = proj_soup.find(class_='js-load-project-faqs').findChildren()[0]
        proj_faq_count = int(re.sub('[^\d]', '', find_faq.text)) if find_faq != None else 0
        proj_creator_id = proj_soup.find(attrs = {'data-modal-title' : 'About the creator'}).get('href').split('/')[1]
            # proj_soup.find('meta', attrs={'property': 'kickstarter:creator'}).get('content').split('/')[-1]
        proj_creator_name = proj_soup.find(attrs = {'data-modal-title' : 'About the creator'}).text.strip()
        proj_location = proj_soup.find(class_ = 'mr3', href=re.compile('/discover/places/')).text.strip()
    except Exception as e:
        print 'project: ' + pid + 'may have a problem.'
        print e

    df = pd.DataFrame(
    {'pid': [pid],
     'proj_title': [proj_title],
     'proj_description': [proj_description],
     'proj_url': [proj_url],
     'proj_goal': [proj_goal],
     'proj_amount_pledged': [proj_amount_pledged],
     'proj_currency': [proj_currency],
     'proj_start_date': [proj_start_date],
     'proj_end_date': [proj_end_date],
     'proj_category': [proj_category],
     'proj_subcategory': [proj_subcategory],
     'proj_backer_count': [proj_backer_count],
     'proj_comment_count': [proj_comment_count],
     'proj_update_count': [proj_update_count],
     'proj_faq_count': [proj_faq_count],
     'proj_creator_id': [proj_creator_id],
     'proj_creator_name': [proj_creator_name],
     'proj_location': [proj_location]
    })

    return df