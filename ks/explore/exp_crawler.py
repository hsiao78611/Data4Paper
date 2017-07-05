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

ks_link = 'https://www.kickstarter.com/discover/advanced?state=successful&category_id={}&goal={}&sort=end_date&seed={}&page=1'
load_more_button_Xpath = '//*[@id="projects"]/div/div[2]/a'


class Category:

    def __init__(self, id, goal):
        self.id = id
        self.goal = goal

        # set a random seed number
        rand_seed = randint(2000001, 2999999)

        # get a new agent
        agents = ua.get_user_agents()
        user_agent = list(agents)[randint(0, len(agents))]

        # setup webdriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('user-agent=' + user_agent)
        chrome_options.add_argument('--proxy-server=http://127.0.0.1:8118')
        driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        # check user agent and ip address
        driver.get('http://ipinfo.io/ip/')
        print driver.execute_script('return navigator.userAgent')
        # check ip address
        now_ip = BeautifulSoup(driver.page_source, 'lxml').text
        print now_ip
        # driver.set_window_size(1000, 1200) # set the browser size in order to click the button
        driver.get(ks_link.format(id, goal, rand_seed))

        self.total = int(re.sub('[^\d]', '', driver.find_element_by_xpath('//*[@id="projects"]/div/h3/b').text))

        count_visible_project = 0
        button_location = 6600
        each_scroll = 6634

        button_visiable = True
        count_scroll = 0
        temp_count = 0

        while button_visiable:
            try:
                driver.execute_script('window.scrollTo(0,'+str(button_location+each_scroll*count_scroll)+');') # document.body.scrollHeight);')
                count_scroll = count_scroll + 1
                load_more_button = driver.find_element_by_xpath(load_more_button_Xpath)
                load_more_button.click()
                # wait for loading more projects
                time.sleep(randint(5, 10))
                count_visible_project =  len(driver.find_elements_by_xpath('//*[@data-project_state="successful"]'))
            except Exception as e:
                # driver.save_screenshot('screenshot.png') # for debugging
                e # i don't want to see it.
                # break

            # track the state
            if count_visible_project != temp_count:
                print str(self.total) +'-'+ str(count_scroll) +'-'+ str(count_visible_project)
                temp_count = count_visible_project

            if driver.current_url.split('=')[-1] == 200:
                break

        # make a soup then sleep
        strainer = SoupStrainer('div', attrs={'id':'projects_list'})
        list_soup = BeautifulSoup(driver.page_source, 'lxml', parse_only=strainer)

        time.sleep(randint(1, 3))
        driver.quit()

        print 'finished explore soup'
        self.plist = list_soup.find_all('div', class_='js-track-project-card')


    def get_link(self):

        df = pd.DataFrame({
            'pid': [],
            'backers': [],
            'percent': [],
            'link': [],
            'category': [],
            'title': [],
            'creater': [],
            'c_link': []
        })
        # get slug and id
        for i in range(len(self.plist)):
            try:
                pid = self.plist[i].get('data-project_pid')
                backers = self.plist[i].get('data-project_backers_count')
                percent = self.plist[i].get('data-project_percent_raised')
                link = self.plist[i].find('a').get('href').split('?')[0]
                category = re.sub('^https://www.kickstarter.com/discover/categories/', '', self.plist[i].find_all('a')[1].get('href').split('?')[0])
                title = re.sub('[:$]', '',self.plist[0].find_all('a')[2].text)
                creater = self.plist[i].find_all('span')[1].text
                c_link = self.plist[i].find_all('a')[3].get('href')
            except Exception as e:
                print e
                break

            df_temp = pd.DataFrame({
                'pid': [pid],
                'backers': [backers],
                'percent': [percent],
                'link': [link],
                'category': [category],
                'title': [title],
                'creater': [creater],
                'c_link': [c_link]
            })
            df = df.append(df_temp)

        return df

# >>> df.iloc[0][0]
# '287'
# >>> df.iat[0,0]
# '287'