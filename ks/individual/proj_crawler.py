import re
import urllib2
from random import randint
import time
from bs4 import BeautifulSoup, SoupStrainer
import signal

import ks.utils.renewip as new
import ks.utils.scrollpage as sc
import ks.utils.setwebdriver as sw
import ks.utils.useragents as ua
from ks.individual.df_comments import df_comments
from ks.individual.df_faqs import df_faqs
from ks.individual.df_project import df_project
from ks.individual.df_rewards import df_rewards
from ks.individual.df_updates import df_updates


class Campaign:

    def __init__(self, ks_link, pid):
        self.ks_link = ks_link
        self.pid = pid

        # get a random agent
        agents_lst = ua.get_user_agents()
        user_agent = list(agents_lst)[randint(0, len(agents_lst) - 1)]
        self.headers = {'User-Agent': user_agent}

        # communicate with TOR via a local proxy (privoxy)
        new.renew_connection()

    # need using random order?
    def project_rewards(self):
        # Speeding up BeautifulSoup by using SoupStrainer and lxml parser
        request = urllib2.Request(self.ks_link, None, self.headers)
        response = urllib2.urlopen(request)
        strainer = SoupStrainer('main', attrs={'role': 'main'})
        time.sleep(randint(1, 3))
        proj_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
        rew_soup = proj_soup.find('div', class_='NS_projects__rewards_list js-project-rewards')
        response.close()
        return [df_project(proj_soup, self.pid), df_rewards(rew_soup, self.pid)]

    def updates(self):
        request = urllib2.Request(self.ks_link + '/updates', None, self.headers)
        response = urllib2.urlopen(request)
        strainer = SoupStrainer('div', class_='timeline')
        time.sleep(randint(1, 3))
        upd_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
        response.close()
        return df_updates(upd_soup, self.pid)

    def faqs(self):
        request = urllib2.Request(self.ks_link + '/faqs', None, self.headers)
        response = urllib2.urlopen(request)
        strainer = SoupStrainer('ul', class_='faqs col-8')
        time.sleep(randint(1,3))
        faq_soup = BeautifulSoup(response, 'lxml', parse_only=strainer)
        response.close()
        return df_faqs(faq_soup, self.pid)

    def comments(self):
        # set a web driver with the size
        driver = sw.set_driver(800, 880)
        # get the web page
        driver.get(self.ks_link + '/comments')
        # get total comment number
        try: # there may have a live stream video, such as 'Tuesday total body boss workout!'
            self.total_cmt = int(re.sub('[^\d]', '', driver.find_element_by_xpath(
                '//*[@id="content-wrap"]/div[2]/div/div/div/div[2]/a[5]/span/data').text))
        except Exception as e:
            print e
            self.total_cmt = int(re.sub('[^\d]', '', driver.find_element_by_xpath(
                '//*[@id="content-wrap"]/div[3]/div/div/div/div[2]/a[5]/span/data').text))
        print 'total comments: ' + str(self.total_cmt)
        if self.total_cmt == 0:
            self.total_cmt = 0
            self.count_visible_cmt = 0
            cmt_soup = None
        else:
            # scroll down repeatedly until it cannot load more data
            # and get finally amount of visible items
            if self.total_cmt > 50:
                self.count_visible_cmt = sc.scroll_down_comment(driver, self.total_cmt)
            else:
                self.count_visible_cmt = len(driver.find_elements_by_xpath('//*[@id="content-wrap"]/div[2]/section[7]/div/div/div/div[2]/div[2]/ol/li/ol/li'))

            strainer = SoupStrainer('ol', class_='comments')
            cmt_soup = BeautifulSoup(driver.page_source, 'lxml', parse_only=strainer)

        # only for PhantomJS
        driver.service.process.send_signal(signal.SIGTERM)

        driver.quit()
        print 'finished comments soup'

        return df_comments(cmt_soup, self.pid)