'''
Adapted from: https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853
Python script to connect to Tor via Stem and Privoxy, requesting a new connection (hence a new IP as well) as desired.
'''

import urllib2
import time
from stem import Signal
from stem.control import Controller

requestIP = "http://icanhazip.com/" # ipinfo.io/ip/"

def _request(url):
    # communicate with TOR via a local proxy (privoxy)
    def _set_urlproxy():
        proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

    # request a URL
    # via the proxy
    _set_urlproxy()
    request = urllib2.Request(url)
    return urllib2.urlopen(request).read()

def renew_connection():
    oldIP = _request(requestIP)
    # seconds between
    # IP address checks
    secondsBetweenChecks = 2

    # signal TOR for a new connection
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='my_password')
        controller.signal(Signal.NEWNYM)
        controller.close()
    newIP = _request(requestIP)

    # elapsed seconds
    seconds = 0
    # loop until the "new" IP address
    while oldIP == newIP:
        if seconds == 30:
            break
        # sleep this thread
        # for the specified duration
        time.sleep(secondsBetweenChecks)
        # track the elapsed seconds
        seconds += secondsBetweenChecks
        # obtain the current IP address
        newIP = _request(requestIP)
        # signal that the program is still awaiting a different IP address
        print ("%d seconds elapsed awaiting a different IP address." % seconds)
