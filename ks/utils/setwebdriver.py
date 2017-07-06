from random import randint
from selenium import webdriver
import ks.utils.useragents as ua


def set_driver(self, width, height):
    '''
    using tor via privoxy
    options are referred to: https://s2.smu.edu/~jwadleigh/seltest/
    '''
    # get a new agent
    agents = ua.get_user_agents()
    user_agent = list(agents)[randint(0, len(agents))]

    # setup webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-agent=' + user_agent)
    chrome_options.add_argument('--proxy-server=http://127.0.0.1:8118')
    driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
    # set the browser size in order to click the button
    driver.set_window_size(width, height)


    # # used to check the user agent and ip address
    # driver.get('http://ipinfo.io/ip/')
    # print driver.execute_script('return navigator.userAgent')
    # # check ip address
    # now_ip = BeautifulSoup(driver.page_source, 'lxml').text
    # print now_ip

    return driver