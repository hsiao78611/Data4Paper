'''
Adapted from: https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853
Python script to connect to Tor via Stem and Privoxy, requesting a new connection (hence a new IP as well) as desired.
'''
import time
import urllib2

from stem import Signal
from stem.control import Controller

from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer

import ks.utils.useragents as ua
from random import randint

# initialize some HTTP headers
# for later usage in URL requests
agents = ua.get_user_agents()
user_agent = list(agents)[randint(0, len(agents))]
headers={'User-Agent':user_agent}

# initialize some
# holding variables
oldIP = "0.0.0.0"
newIP = "0.0.0.0"

# how many IP addresses
# through which to iterate?
nbrOfIpAddresses = 3

# seconds between
# IP address checks
secondsBetweenChecks = 2

# request a URL
def request(url):
    # communicate with TOR via a local proxy (privoxy)
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

    # request a URL
    # via the proxy
    _set_urlproxy()
    request = urllib2.Request(url, None, headers)
    return urllib2.urlopen(request).read()

# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password = 'my_password')
        controller.signal(Signal.NEWNYM)
        controller.close()

# cycle through
# the specified number
# of IP addresses via TOR
for i in range(0, nbrOfIpAddresses):

    # if it's the first pass
    if newIP == "0.0.0.0":
        # renew the TOR connection
        renew_connection()
        # obtain the "new" IP address
        newIP = request("http://icanhazip.com/")
    # otherwise
    else:
        # remember the
        # "new" IP address
        # as the "old" IP address
        oldIP = newIP
        # refresh the TOR connection
        renew_connection()
        # obtain the "new" IP address
        newIP = request("http://icanhazip.com/")

    # zero the
    # elapsed seconds
    seconds = 0

    # loop until the "new" IP address
    # is different than the "old" IP address,
    # as it may take the TOR network some
    # time to effect a different IP address
    while oldIP == newIP:
        # sleep this thread
        # for the specified duration
        time.sleep(secondsBetweenChecks)
        # track the elapsed seconds
        seconds += secondsBetweenChecks
        # obtain the current IP address
        newIP = request("http://icanhazip.com/")
        # signal that the program is still awaiting a different IP address
        print ("%d seconds elapsed awaiting a different IP address." % seconds)
    # output the
    # new IP address
    print ("")
    print ("newIP: %s" % newIP)

# using webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('user-agent='+user_agent)
chrome_options.add_argument('--proxy-server=http://127.0.0.1:8118')

driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
driver.get('http://ipinfo.io/ip/')
print driver.execute_script('return navigator.userAgent')
print BeautifulSoup(driver.page_source, 'lxml').text