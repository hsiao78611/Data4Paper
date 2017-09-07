import re
import urllib2
from random import randint

from bs4 import BeautifulSoup, SoupStrainer

import ks.utils.renewip as new
import ks.utils.scrollpage as sc
import ks.utils.setwebdriver as sw
import ks.utils.useragents as ua

from ks.individual.df_comments import df_comments
from ks.creator.df_about import df_about
from ks.creator.df_backed import df_backed
from ks.creator.df_created import df_created
from ks.creator.df_comments import df_comments

# get a random agent
agents_lst = ua.get_user_agents()
user_agent = list(agents_lst)[randint(0, len(agents_lst) - 1)]
headers = {'User-Agent': user_agent}

class Creator:

    def __init__(self, crt_link, cid):
        self.crt_link = crt_link
        self.cid = cid

        # set a web driver with the size
        self.driver = sw.set_driver(910, 1820)

        # communicate with TOR via a local proxy (privoxy)
        new.renew_connection()

        # some creator account is not existent, such as id: 128262571
        request = urllib2.Request(self.crt_link)
        response = urllib2.urlopen(request)
        strainer = SoupStrainer('main', attrs={'role': 'main'})
        soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
        self.active = 'Sorry! This person is no longer active on Kickstarter.' != soup.text.strip()

    def about(self):
        if self.active:
            request = urllib2.Request(self.crt_link + '/about', None, headers)
            response = urllib2.urlopen(request)
            strainer = SoupStrainer('main', attrs={'role': 'main'})
            abt_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
            print 'finished about soup'
        else:
            abt_soup = 'non-exist'
        return df_about(abt_soup, self.cid)

    def backed(self):
        if self.active:
            self.driver.get(self.crt_link)
            # scroll down until all of projects are visible
            sc.scroll_down_backed(self.driver)
            strainer = SoupStrainer('div', class_='mobius_page')
            bac_soup = BeautifulSoup(self.driver.page_source, 'lxml', parse_only=strainer)
            print 'finished backed soup'
        else:
            bac_soup = 'non-exist'
        return df_backed(bac_soup, self.cid)

    # it needs webdriver to get the content derived from javascript
    def created(self):
        if self.active:
            self.driver.get(self.crt_link + '/created')
            strainer = SoupStrainer('div', class_='grid-row flex flex-wrap')
            crt_soup = BeautifulSoup(self.driver.page_source, 'lxml', parse_only=strainer)
            print 'finished created soup'
            # finished 'backed' and 'created'
            self.driver.quit()
        else:
            crt_soup = 'non-exist'
        return df_created(crt_soup, self.cid)


    # def comments(self):
    #     # get the web page
    #     self.driver.get(self.crt_link + '/comments')
    #     # scroll down until all of projects are visible
    #     sc.scroll_down_users_comment()
    #     strainer = SoupStrainer('ul', class_='mobius')
    #     cmt_soup = BeautifulSoup(self.driver.page_source, 'lxml', parse_only=strainer)
    #     print 'finished comments soup'
    #     self.driver.quit()
    #     return df_comments(cmt_soup, self.pid)