import time
from random import randint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def _scroll_down(driver, count_visible_item, load_more_button_Xpath, count_scroll, button_location):
    scroll_range = button_location
    # scroll to the position
    driver.execute_script('window.scrollTo(0,' + scroll_range + ');')
    # find the button
    load_more_button = driver.find_element_by_xpath(load_more_button_Xpath)
    button_visiable = load_more_button.get_attribute('style')  # .is_displayed() may occur error

    # click only there exists a button
    if button_visiable != 'display: none;':
        try:
            load_more_button.click()
        except Exception as e:
            # driver.save_screenshot('screenshot.png') # for debugging
            print e

    # wait for loading more projects
    time.sleep(randint(1, 5))
    return [count_scroll, button_visiable]


def scroll_down_comment(driver, total):
    load_more_button_Xpath = '//*[@id=\"content-wrap\"]/div[2]/section[7]/div/div/div/div[2]/div[2]/a'
    earliest_comment_Xpath = '//*[@id="content-wrap"]/div[2]/section[7]/div/div/div/div[2]/div[2]/ol/li/ol/li[@class=\"NS_comments__comment comment earliest_comment item mb3 py3\"]'

    count_scroll = 0
    temp_count_visible_item = 0

    # def _wait_for_load(input_Xpath, wait_time):
    #     wait = WebDriverWait(driver, wait_time)
    #     wait.until(EC.presence_of_element_located((By.XPATH, input_Xpath)))

    def _earliest_comment():
        try:
            driver.find_element_by_xpath(earliest_comment_Xpath)
            return True
        except Exception:
            return False

    while _earliest_comment() == False:
        count_visible_item = len(driver.find_elements_by_xpath('//*[@id="content-wrap"]/div[2]/section[7]/div/div/div/div[2]/div[2]/ol/li/ol/li'))
        button_location = 'document.body.scrollHeight'  # to the bottom
        # scroll down and update scrolling time
        result = _scroll_down(driver, count_visible_item, load_more_button_Xpath, count_scroll, button_location)

        count_scroll = result[0]

        # track the state
        count_visible_item = len(driver.find_elements_by_xpath('//*[@data-project_state="successful"]'))
        if count_visible_item != temp_count_visible_item:
            print str(total) + '-' + str(count_scroll) + '-' + str(count_visible_item)
            temp_count_visible_item = count_visible_item

    # wait for results to appear
    # _wait_for_load(earliest_comment_Xpath, 5)

    return temp_count_visible_item


def scroll_down_explore(driver, total):
    load_more_button_Xpath = '//*[@id="projects"]/div/div[2]'
    button_visiable = ''
    count_scroll = 0
    temp_count_visible_item = 0

    while button_visiable != 'display: none;':
        # control scrolling range by the amount of items
        count_visible_item = len(driver.find_elements_by_xpath('//*[@data-project_state="successful"]'))
        button_location = str(400 + 575 * (count_visible_item / 3))
        # scroll down and update scrolling time
        result = _scroll_down(driver, count_visible_item, load_more_button_Xpath, count_scroll, button_location)

        count_scroll = result[0]
        button_visiable = result[1]


        # track the state
        count_visible_item = len(driver.find_elements_by_xpath('//*[@data-project_state="successful"]'))
        if count_visible_item != temp_count_visible_item:
            print str(total) + '-' + str(count_scroll) + '-' + str(count_visible_item)
            temp_count_visible_item = count_visible_item
        # reach the limited maximum pages
        if driver.current_url.split('=')[-1] == '200':
            break

    return temp_count_visible_item