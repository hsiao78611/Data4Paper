from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
from random import randint

class Scroll:

    def __init__(self, driver, total):
        self.driver
        self.total

    def _scroll_down(self, load_more_button_Xpath, count_scroll):
        button_location = 6600
        each_scroll = 6634
        scroll_range = button_location+each_scroll*count_scroll

        try:
            self.driver.execute_script('window.scrollTo(0,'+str(scroll_range)+');') # document.body.scrollHeight);')
            count_scroll = count_scroll + 1
            load_more_button = self.driver.find_element_by_xpath(load_more_button_Xpath)
            button_visiable = load_more_button.get_attribute('style')  # .is_displayed() may occur error
            if button_visiable != 'display: none;':
                load_more_button.click()
            # wait for loading more projects
            time.sleep(randint(5, 10))
        except Exception as e:
            # driver.save_screenshot('screenshot.png') # for debugging
            print e

        return count_scroll


    def scrolldown_explore(self):
        load_more_button_Xpath = '//*[@id="projects"]/div/div[2]'
        button_visiable = ''
        count_scroll = 0
        temp_count_visible_project = 0

        while button_visiable != 'display: none;':
            # scroll down and update scrolling time
            count_scroll = self._scroll_down(load_more_button_Xpath, count_scroll)
            # track the state
            count_visible_project = len(self.driver.find_elements_by_xpath('//*[@data-project_state="successful"]'))
            if count_visible_project != temp_count_visible_project:
                print str(self.total) + '-' + str(count_scroll) + '-' + str(count_visible_project)
                temp_count_visible_project = count_visible_project
            # reach the limited maximum pages
            if self.driver.current_url.split('=')[-1] == 200:
                break