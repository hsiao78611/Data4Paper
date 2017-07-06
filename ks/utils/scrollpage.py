import time
from random import randint

def _scroll_down(driver, load_more_button_Xpath, count_scroll, exception):
    button_location = 6600
    each_scroll = 6634
    scroll_range = button_location+each_scroll*count_scroll

    if exception[0] == False:
        driver.execute_script('window.scrollTo(0,' + str(scroll_range) + ');')  # document.body.scrollHeight);')
        count_scroll = count_scroll + 1
    else:
        count_scroll = count_scroll
        # let it scroll back to click button
        if exception[1] == 1:
            driver.execute_script('window.scrollTo(0,' + str(scroll_range-500-400) + ');')
            exception[0] = False
        else: # special case
            driver.execute_script('window.scrollTo(0,' + str(scroll_range - 500 - 400 - 400) + ');')
            exception[0] = False

    load_more_button = driver.find_element_by_xpath(load_more_button_Xpath)
    button_visiable = load_more_button.get_attribute('style')  # .is_displayed() may occur error
    if button_visiable != 'display: none;':
        try:
            load_more_button.click()
            if exception[1] > 0:
                exception[1] = 0
        except Exception as e:
            # driver.save_screenshot('screenshot.png') # for debugging
            if exception[1] == 0:
                exception[0] = True
                exception[1] = 1
            else:
                exception[0] = True
                exception[1] = exception[1] + 1
            print e

    # wait for loading more projects
    time.sleep(randint(1, 5))
    return [count_scroll, exception, button_visiable]


def scroll_down_explore(driver, total):
    load_more_button_Xpath = '//*[@id="projects"]/div/div[2]'
    button_visiable = ''
    count_scroll = 0
    exception = False
    temp_count_visible_item = 0

    while button_visiable != 'display: none;':
        # scroll down and update scrolling time
        result = _scroll_down(driver, load_more_button_Xpath, count_scroll, exception)
        count_scroll = result[0]
        exception = result[1]
        button_visiable = result[2]
        # track the state
        count_visible_item = len(driver.find_elements_by_xpath('//*[@data-project_state="successful"]'))
        if count_visible_item != temp_count_visible_item:
            print str(total) + '-' + str(count_scroll) + '-' + str(count_visible_item)
            temp_count_visible_item = count_visible_item
        # reach the limited maximum pages
        if driver.current_url.split('=')[-1] == '200':
            break

    return temp_count_visible_item