# win10 + ubuntu 16.0.4
after installed ubuntu
sudo update-grub

sudo apt-get update
sudo apt-get git
sudo apt-get install python-pip

# install PyCharm
https://www.jetbrains.com/pycharm/download/

# sqlite3 & browser
sudo apt install sqlite3
sudo apt install sqlitebrowser

# install PhantomJS
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

# Install ChromeDriver and Selenium on Ubuntu 16.04
https://gist.github.com/ziadoz/3e8ab7e944d02fe872c3454d17af31a5

# Crawling Anonymously with Tor in Python
https://gist.github.com/KhepryQuixote/46cf4f3b999d7f658853

brew services restart tor
tor --hash-password my_password

sudo gedit /etc/tor/torrc
or nano for Mac

ControlPort 9051
# hashed password below is obtained via `tor --hash-password my_password`
HashedControlPassword 16:6C043E9B957A15C26009509310D321C815E95C4835F46713B532AAC922
CookieAuthentication 1


sudo nano /usr/local/etc/privoxy/config

forward-socks5 / localhost:9050

brew services restart privoxy

“stem” just installed by pyCharm


if icanhazip.com doesn’t work
http://ipinfo.io/ip
http://ipecho.net/plain
curl http://canhazip.com