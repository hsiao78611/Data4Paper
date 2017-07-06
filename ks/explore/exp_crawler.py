from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import re
import time
from random import randint
import pandas as pd

import ks.utils.useragents as ua
from ks.explore.df_explore import df_explore

ks_link = 'https://www.kickstarter.com/discover/advanced?state=successful&category_id={}&goal={}&sort=end_date&seed={}&page=1'
load_more_button_Xpath = '//*[@id="projects"]/div/div[2]'


class Category:

    def __init__(self, id, goal):
        '''
        using tor via privoxy
        '''
        # get a new agent
        agents = ua.get_user_agents()
        user_agent = list(agents)[randint(0, len(agents))]
        # setup webdriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('user-agent=' + user_agent)
        chrome_options.add_argument('--proxy-server=http://127.0.0.1:8118')
        driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

        # used to check the user agent and ip address
        # driver.get('http://ipinfo.io/ip/')
        # print driver.execute_script('return navigator.userAgent')
        # # check ip address
        # now_ip = BeautifulSoup(driver.page_source, 'lxml').text
        # print now_ip


        # set a random seed number
        rand_seed = randint(2000001, 2999999)
        # set the browser size in order to click the button
        driver.set_window_size(910, 1820)
        # get the web page
        driver.get(ks_link.format(id, goal, rand_seed))

        # get total projects number in the category
        total = int(re.sub('[^\d]', '', driver.find_element_by_xpath('//*[@id="projects"]/div/h3/b').text))


        button_location = 6600
        each_scroll = 6634
        count_scroll = 0
        temp_count_visible_project = 0
        button_visiable = ''

        while button_visiable != 'display: none;':
            try:
                driver.execute_script('window.scrollTo(0,'+str(button_location+each_scroll*count_scroll)+');') # document.body.scrollHeight);')
                count_scroll = count_scroll + 1
                load_more_button = driver.find_element_by_xpath(load_more_button_Xpath)
                button_visiable = load_more_button.get_attribute('style')  # .is_displayed() may occur error
                if button_visiable != 'display: none;':
                    load_more_button.click()
                # wait for loading more projects
                time.sleep(randint(5, 10))
            except Exception as e:
                # driver.save_screenshot('screenshot.png') # for debugging
                print e

            # track the state
            count_visible_project = len(driver.find_elements_by_xpath('//*[@data-project_state="successful"]'))
            if count_visible_project != temp_count_visible_project:
                print str(total) +'-'+ str(count_scroll) +'-'+ str(count_visible_project)
                temp_count_visible_project = count_visible_project
            # reach the limited maximum pages
            if driver.current_url.split('=')[-1] == 200:
                break

        # make a soup then sleep
        strainer = SoupStrainer('div', attrs={'id':'projects_list'})
        self.list_soup = BeautifulSoup(driver.page_source, 'lxml', parse_only=strainer)
        time.sleep(randint(1, 3))
        driver.quit()
        print 'finished explore soup'

    def get_exp(self):
        return df_explore(self.list_soup)
