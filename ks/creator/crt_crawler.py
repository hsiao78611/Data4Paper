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

        # communicate with TOR via a local proxy (privoxy)
        new.renew_connection()

    def about(self):
        request = urllib2.Request(self.crt_link + '/about', None, headers)
        response = urllib2.urlopen(request)
        strainer = SoupStrainer('main', attrs={'role': 'main'})
        abt_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
        print 'finished about soup'
        return df_about(abt_soup, self.cid)

    #
    # it may have load more button
    # such as superbacker: https://www.kickstarter.com/profile/859880747
    #
    def backed(self):
        request = urllib2.Request(self.crt_link, None, headers)
        response = urllib2.urlopen(request)
        strainer = SoupStrainer('div', class_='mobius_page')
        bac_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
        print 'finished backed soup'
        return df_backed(bac_soup, self.cid)

    # it needs webdriver
    def created(self):
        request = urllib2.Request(self.crt_link + '/created', None, headers)
        response = urllib2.urlopen(request)
        strainer = SoupStrainer('div', class_='grid-row flex flex-wrap')
        crt_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
        print 'finished created soup'
        return df_created(crt_soup, self.cid)

    #
    # it may have load more button
    #
    def comments(self):
        # set a web driver with the size
        driver = sw.set_driver(910, 1820)
        # get the web page
        driver.get(self.crt_link + '/comments')

        # get total comment number
        try:
            self.total_cmt = driver.find_element_by_xpath('//*[@id="main_content"]/div[3]/div/div/div/ul/li[4]/a/span').text
        except Exception as e:
            self.total_cmt ='0'
            print e

        if self.total_cmt == '0':
            self.count_visible_cmt = 0
            cmt_soup = None
        else:
            # scroll down repeatedly until it cannot load more data
            # and get finally amount of visible items
            self.count_visible_cmt = sc.scroll_down_explore(driver, self.total)
            strainer = SoupStrainer('ul', class_='mobius')
            cmt_soup = BeautifulSoup(driver.page_source, 'lxml', parse_only=strainer)
        driver.quit()
        print 'finished comments soup'

        return df_comments(cmt_soup, self.pid)