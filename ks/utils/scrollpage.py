import time
from random import randint

def _scroll_down(driver, load_more_button_Xpath, count_scroll, count_ex):
    button_location = 6600
    each_scroll = 6634
    scroll_range = button_location+each_scroll*count_scroll

    driver.execute_script('window.scrollTo(0,'+str(scroll_range)+');') # document.body.scrollHeight);')
    if count_ex == 0:
        count_scroll = count_scroll + 1
    else:
        count_scroll = count_scroll
        # let it scroll back to click button
        driver.execute_script('window.scrollTo(0,' + str(scroll_range-100) + ');')
    load_more_button = driver.find_element_by_xpath(load_more_button_Xpath)
    button_visiable = load_more_button.get_attribute('style')  # .is_displayed() may occur error
    if button_visiable != 'display: none;':
        try:
            load_more_button.click()
        except Exception as e:
            # driver.save_screenshot('screenshot.png') # for debugging
            count_ex = count_ex + 1
            print e
    # wait for loading more projects
    time.sleep(randint(5, 10))


    return [count_scroll, count_ex, button_visiable]


def scroll_down_explore(driver, total):
    load_more_button_Xpath = '//*[@id="projects"]/div/div[2]'
    button_visiable = ''
    count_scroll = 0
    count_ex = 0
    temp_count_visible_project = 0

    while button_visiable != 'display: none;':
        # scroll down and update scrolling time
        result = _scroll_down(driver, load_more_button_Xpath, count_scroll, count_ex)
        count_scroll = result[0]
        count_ex = result[1]
        button_visiable = result[2]
        # track the state
        count_visible_project = len(driver.find_elements_by_xpath('//*[@data-project_state="successful"]'))
        if count_visible_project != temp_count_visible_project:
            print str(total) + '-' + str(count_scroll) + '-' + str(count_visible_project)
            temp_count_visible_project = count_visible_project
        # reach the limited maximum pages
        if driver.current_url.split('=')[-1] == 200:
            break