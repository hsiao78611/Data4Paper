import time
from datetime import datetime
from random import randint

def _scroll_down(driver, load_more_button_Xpath):

    # find the button
    try:
        load_more_button = driver.find_element_by_xpath(load_more_button_Xpath)
    except Exception as e:  # there may have a subscribe feature, such as 'Tuesday total body boss workout!'
        print e
        load_more_button = driver.find_element_by_xpath('//*[@id=\"content-wrap\"]/div[3]/section[7]/div/div/div/div[2]/div[2]/a')
    # scroll to the position
    load_more_button.location_once_scrolled_into_view

    # click only there exists a button
    button_visiable = load_more_button.get_attribute('style')  # .is_displayed() may occur error
    if button_visiable != 'display: none;':
        try:
            time.sleep(1)
            load_more_button.click()
        except Exception as e:
            driver.execute_script('window.scrollTo(0,0);') # 'document.body.scrollHeight'  # to the bottom
            time.sleep(10)
            driver.refresh()
            print e

    # wait for loading more projects
    time.sleep(randint(1, 3))
    return button_visiable


def scroll_down_comment(driver, total):
    load_more_button_Xpath = '//*[@id=\"content-wrap\"]/div[2]/section[7]/div/div/div/div[2]/div[2]/a'
    earliest_comment_Xpath = '//*[@id="content-wrap"]/div[2]/section[7]/div/div/div/div[2]/div[2]/ol/li/ol/li'
    req_count = total/50 + 1 if total%50 > 0 else 0
    count = 1
    start_time = datetime.now()

    # def _wait_for_load(input_Xpath, wait_time):
    #     wait = WebDriverWait(driver, wait_time)
    #     wait.until(EC.presence_of_element_located((By.XPATH, input_Xpath)))

    def _earliest_comment():
        earliest = driver.find_elements_by_xpath(earliest_comment_Xpath)[-1].get_attribute('class')
        return 'earliest_comment' in earliest

    print count, '/', req_count
    while True:
        # scroll down and click
        _scroll_down(driver, load_more_button_Xpath)
        end_time = datetime.now()
        exe_time = end_time - start_time
        count = count + 1
        print count, '/', req_count,' #', exe_time.total_seconds(),'seconds elapsed'

        if count * 50 >= total:
            # do not find element every time
            if _earliest_comment() == True:
                break

    count_visible_item = len(driver.find_elements_by_xpath(
        '//*[@id="content-wrap"]/div[2]/section[7]/div/div/div/div[2]/div[2]/ol/li/ol/li'))
    print str(total) + '-' + str(count_visible_item)

    # wait for results to appear
    # _wait_for_load(earliest_comment_Xpath, 5)

    return count_visible_item


def scroll_down_explore(driver, total):
    load_more_button_Xpath = '//*[@id="projects"]/div/div[2]'
    temp_count_visible_item = 0

    while temp_count_visible_item != total:
        # scroll down
        _scroll_down(driver, load_more_button_Xpath)

        # track the state
        count_visible_item = len(driver.find_elements_by_xpath('//*[@data-project_state="successful"]'))
        if count_visible_item != temp_count_visible_item:
            print str(total) + '-' + str(count_visible_item)
            temp_count_visible_item = count_visible_item
        # reach the limited maximum pages
        if driver.current_url.split('=')[-1] == '200':
            break

    return temp_count_visible_item


def scroll_down_backed(driver):
    total = int(driver.find_element_by_xpath('//*[@id="main_content"]/div[3]/div/div/div/ul/li[2]/a/span').text)
    page = 1
    pages = total / 36 + (1 if total % 36 > 0 else 0)
    while page != pages:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page = len(driver.find_elements_by_xpath('//*[@id="list"]/div/ul/li'))


def scroll_down_users_comment(driver):
    total = int(driver.find_element_by_xpath('//*[@id="main_content"]/div[3]/div/div/div/ul/li[3]/a/span').text)
    while total != cmt_count:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        cmt_count = len(driver.find_elements_by_xpath('//*[@id="activity"]/li'))