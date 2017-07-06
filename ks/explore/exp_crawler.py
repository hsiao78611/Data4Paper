from bs4 import BeautifulSoup, SoupStrainer
from random import randint
import re
import time

from ks.explore.df_explore import df_explore
import ks.utils.setwebdriver as sw
import ks.utils.scrollpage as sc

ks_link = 'https://www.kickstarter.com/discover/advanced?state=successful&category_id={}&goal={}&sort=end_date&seed={}&page=1'

class Category:

    def __init__(self, id, goal):
        # set a web driver
        driver = sw.set_driver(910, 1820)
        # set a random seed number
        rand_seed = randint(2000001, 2999999)
        # get the web page
        driver.get(ks_link.format(id, goal, rand_seed))

        if driver.find_element_by_xpath('//*[@id="NS__empty_states"]').text!='':
            self.total = 0

        else:
            # get total projects number in the category
            self.total = int(re.sub('[^\d]', '', driver.find_element_by_xpath('//*[@id="projects"]/div/h3/b').text))
            # scroll down repeatedly until it cannot load more data
            sc.scroll_down_explore(driver, self.total)

        # make a soup then sleep
        strainer = SoupStrainer('div', attrs={'id':'projects_list'})
        self.list_soup = BeautifulSoup(driver.page_source, 'lxml', parse_only=strainer)
        time.sleep(randint(1, 3))

        driver.quit()
        print 'finished explore soup'

    def get_exp(self):
        return df_explore(self.list_soup)