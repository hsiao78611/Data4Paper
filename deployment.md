win10 + ubuntu 16.0.4
=====================
After installed ubuntu

    sudo update-grub

    sudo apt-get update
    sudo apt-get git
    sudo apt-get install python-pip

install PyCharm
===============
https://www.jetbrains.com/pycharm/download/

sqlite3 & browser
=================
    sudo apt install sqlite3
    sudo apt install sqlitebrowser

install PhantomJS
=================
    sudo apt-get update
    sudo apt-get install build-essential chrpath libssl-dev libxft-dev -y
    sudo apt-get install libfreetype6 libfreetype6-dev -y
    sudo apt-get install libfontconfig1 libfontconfig1-dev -y
    cd ~
    export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64"
    wget https://github.com/Medium/phantomjs/releases/download/v2.1.1/$PHANTOM_JS.tar.bz2
    sudo tar xvjf $PHANTOM_JS.tar.bz2
    sudo mv $PHANTOM_JS /usr/local/share
    sudo ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/
    phantomjs --version

Install ChromeDriver and Selenium on Ubuntu 16.04
=================================================
https://gist.github.com/ziadoz/3e8ab7e944d02fe872c3454d17af31a5

Crawling Anonymously with Tor in Python
=======================================
https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853

### Install Tor.
    sudo apt-get update
    sudo apt-get install tor
    sudo /etc/init.d/tor restart
Notice that the socks listener is on port 9050, so we have to enable the ControlPort listener for Tor to listen on port 9051

### You can create a hashed password out of your password using:
    brew services restart tor
    tor --hash-password my_password

### Then, update the /etc/tor/torrc with the port, hashed password, and cookie authentication.

    sudo gedit /etc/tor/torrc
or nano for Mac

    ControlPort 9051
    # hashed password below is obtained via `tor --hash-password my_password`
    HashedControlPassword 16:6C043E9B957A15C26009509310D321C815E95C4835F46713B532AAC922
    CookieAuthentication 1

    sudo nano /usr/local/etc/privoxy/config
    forward-socks5 / localhost:9050
    brew services restart privoxy

About “stem”, I installed by pyCharm

Obtain the current IP address
=============================
* http://canhazip.com

If icanhazip.com doesn’t work...
* http://ipinfo.io/ip
* http://ipecho.net/plain

Using Remote Desktop to connect to a Microsoft Azure Linux VM
=============================================================
https://docs.microsoft.com/en-us/azure/virtual-machines/linux/classic/remote-desktop

### Using xfce if you are using an Ubuntu version later than Ubuntu 12.04LTS

"Because the current version of xrdp does not support Gnome Desktop for Ubuntu versions later than Ubuntu 12.04LTS, we will use xfce Desktop instead."

To install xfce, use this command:

    sudo apt-get update
    sudo apt-get install xubuntu-desktop

Then enable xfce using this command:

    echo xfce4-session >~/.xsession

Edit the config file /etc/xrdp/startwm.sh:

    sudo vi /etc/xrdp/startwm.sh
Add the line `xfce4-session` before the line `/etc/X11/Xsession`.

To restart the xrdp service, use this:

    sudo service xrdp restart
