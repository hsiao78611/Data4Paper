import re
import urllib2
from random import randint

from bs4 import BeautifulSoup, SoupStrainer

import ks.utils.renewip as new
import ks.utils.scrollpage as sc
import ks.utils.setwebdriver as sw
import ks.utils.useragents as ua
from ks.individual.df_comments import df_comments
from ks.individual.df_faqs import df_faqs
from ks.individual.df_project import df_project
from ks.individual.df_rewards import df_rewards
from ks.individual.df_updates import df_updates

# get a random agent
agents_lst = ua.get_user_agents()
user_agent = list(agents_lst)[randint(0, len(agents_lst) - 1)]
headers = {'User-Agent': user_agent}

class Creator:

    def __init__(self, ks_link, pid = 0):
        self.ks_link = ks_link
        self.pid = pid
        total_cmt = 0
        count_visible_cmt = 0
        # communicate with TOR via a local proxy (privoxy)
        new.renew_connection()

    # need using random order?
    def project_rewards(self):
        # Speeding up BeautifulSoup by using SoupStrainer and lxml parser
        request = urllib2.Request(self.ks_link, None, headers)
        response = urllib2.urlopen(request)
        strainer = SoupStrainer('main', attrs={'role': 'main'})
        proj_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
        print 'finished project soup'

        # self.rew = soup_proj.find_all(class_ = 'hover-group')
        strainer = SoupStrainer('div', class_='NS_projects__rewards_list js-project-rewards')
        rew_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
        print 'finished rewards soup'

        # self.crt_id = proj_soup.find(attrs = {'data-modal-title' : 'About the creator'}).get('href').split('/')[1]

        return [df_project(proj_soup, self.pid), df_rewards(rew_soup, self.pid)]

    def updates(self):
        request = urllib2.Request(self.ks_link + '/updates', None, headers)
        response = urllib2.urlopen(request)
        strainer = SoupStrainer('div', class_='timeline')
        upd_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)

        print 'finished updates soup'

        return df_updates(upd_soup, self.pid)

    def faqs(self):
        request = urllib2.Request(self.ks_link + '/faqs', None, headers)
        response = urllib2.urlopen(request)
        strainer = SoupStrainer('ul', class_='faqs col-8')
        faq_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)

        print 'finished faqs soup'

        return df_faqs(faq_soup, self.pid)

    # def creator(self):
    #     profile = 'https://www.kickstarter.com/profile/'
    #     request = urllib2.Request(profile + self.crt_id, None, headers)
    #     response = urllib2.urlopen(request)
    #     strainer = SoupStrainer()
    #     crt_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
    #
    #     print 'finished creator soup'
    #
    #     return df_creator(crt_soup, self.pid)

    def comments(self):
        # set a web driver with the size
        driver = sw.set_driver(910, 1820)
        # get the web page
        driver.get(self.ks_link + '/comments')

        if driver.find_element_by_xpath('//*[@id="content-wrap"]/div[2]/div/div/div/div[2]/a[5]/span/data').text == '0':
            self.total_cmt = 0
            self.count_visible_cmt = 0
            cmt_soup = None
        else:
            # get total comment number
            self.total_cmt = int(re.sub('[^\d]', '', driver.find_element_by_xpath('//*[@id="content-wrap"]/div[2]/div/div/div/div[2]/a[5]/span/data').text))
            # scroll down repeatedly until it cannot load more data
            # and get finally amount of visible items
            self.count_visible_cmt = sc.scroll_down_explore(driver, self.total)

            strainer = SoupStrainer('ol', class_='comments')
            cmt_soup = BeautifulSoup(driver.page_source, 'lxml', parse_only=strainer)

        driver.quit()
        print 'finished comments soup'

        return df_comments(cmt_soup, self.pid)