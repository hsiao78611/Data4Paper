'''
Adapted from: https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853
Python script to connect to Tor via Stem and Privoxy, requesting a new connection (hence a new IP as well) as desired.
'''
import urllib2

from random import randint
from selenium import webdriver
import ks.utils.useragents as ua

def _get_agent():
    # get a new agent
    agents_lst = ua.get_user_agents()
    user_agent = list(agents_lst)[randint(0, len(agents_lst) - 1)]

    return user_agent


def set_driver(width, height):
    '''
    using tor via privoxy
    options are referred to: https://s2.smu.edu/~jwadleigh/seltest/
    '''

    # setup webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-agent=' + _get_agent())
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

# def set_urllib2():
#     # communicate with TOR via a local proxy (privoxy)
#     def _set_urlproxy():
#         proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
#         opener = urllib2.build_opener(proxy_support)
#         urllib2.install_opener(opener)
#
#     # request a URL
#     # via the proxy
#     _set_urlproxy()
