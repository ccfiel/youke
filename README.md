# youke
Kodi Youtube Videoke/Karaoke 

# How to install
```
sudo apt-get -y install git
sudo apt-get -y install virtualenv
sudo apt-get -y install python-pip
sudo apt-get -y install monit
sudo pip install youtube-dl
git clone https://github.com/ccfiel/youke.git
cd youke
./install.sh
sudo nano /etc/rc.local
    put this /home/xbian/youke/youke.sh &
    this save
```

default username and password
```
username: xbian
password: raspberry
```