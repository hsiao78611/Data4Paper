import requests
from bs4 import BeautifulSoup, SoupStrainer

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
from random import randint

from ks.individual.df_comments import df_comments
from ks.individual.df_project import df_project
from ks.individual.df_rewards import df_rewards
from ks.individual.df_updates import df_updates


class Campaign:

    def __init__(self, ks_link, id = 0):
        self.ks_link = ks_link
        self.id = id

        # need using random order

        # Speeding up BeautifulSoup by using SoupStrainer and lxml parser
        session = requests.Session()
        response = session.get(ks_link)
        strainer = SoupStrainer('main', attrs={'role':'main'})
        proj_soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)

        # projects
        self.proj = proj_soup
        print 'finished project soup'


        # rewards
        # self.rew = soup_proj.find_all(class_ = 'hover-group')
        strainer = SoupStrainer('div', class_='NS_projects__rewards_list js-project-rewards')
        rew_soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)
        self.rew = rew_soup
        print 'finished rewards soup'


        # updates
        # link_upd = urllib.urlopen(ks_link + '/updates')
        # soup_upd = BeautifulSoup(link_upd, 'html.parser')
        response = session.get(ks_link + '/updates')
        strainer = SoupStrainer('div', class_='timeline')
        upd_soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)

        self.upd = upd_soup
        print 'finished updates soup'


        # comments..... it needs more time for loading order comments by web driver
        load_more_button_Xpath = '//*[@id=\"content-wrap\"]/div[2]/section[7]/div/div/div/div[2]/div[2]/a'
        earliest_comment_Xpath = '//*[@id="content-wrap"]/div[2]/section[7]/div/div/div/div[2]/div[2]/ol/li/ol/li[@class=\"NS_comments__comment comment earliest_comment item mb3 py3\"]'

        driver = webdriver.PhantomJS()  # .Chrome()
        # driver.set_window_size(1440, 900) # set the browser size
        driver.get(ks_link + '/comments')

        def wait_for_load(input_Xpath, wait_time):
            wait = WebDriverWait(driver, wait_time)
            wait.until(EC.presence_of_element_located((By.XPATH, input_Xpath)))

        while True:
            try:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                load_more_button = driver.find_element_by_xpath(load_more_button_Xpath)
                load_more_button.click()
                time.sleep(randint(1, 3))
            except Exception as e:
                # driver.save_screenshot('screenshot.png') # for debugging
                # print e
                break
        # wait for results to appear
        wait_for_load(earliest_comment_Xpath, 5)

        # make a soup then sleep
        # soup_cmt = BeautifulSoup(driver.page_source, 'html.parser')
        strainer = SoupStrainer('ol', class_='comments')
        cmt_soup = BeautifulSoup(driver.page_source, 'lxml', parse_only = strainer)

        time.sleep(randint(1, 3))
        driver.quit()

        # cmt = soup_cmt.find_all('li', class_ = 'NS_comments__comment')
        print 'finished comments soup'
        self.cmt = cmt_soup

    def project(self):
        return df_project(self.proj, self.id)

    def rewards(self):
        return df_rewards(self.rew, self.id)

    def updates(self):
        return df_updates(self.upd, self.id)

    def comments(self):
        return df_comments(self.cmt, self.id)

    def link(self):
        return self.ks_link

    def proj(self):
        return self.proj

    def rew(self):
        return self.rew

    def upd(self):
        return self.upd

    def cmt(self):
        return self.cmt

