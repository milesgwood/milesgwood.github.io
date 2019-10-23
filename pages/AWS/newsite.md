---
layout: default
---

# New Website Time

Got the IP address and the key from launching the EC2 instance with Ubuntu Bitnami Wordpress installed.

## Connecting to Cloud9

Connecting Cloud9 to it requires me to add the ssh key to authorized keys on the server and install node js.
```
sudo apt-get install nodejs

nodejs -v
v4.2.6
```

[NVM tutorial](https://tecadmin.net/install-nodejs-with-nvm/)

```
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.bashrc

nvm -v
v0.35.0
```

I didn't actually end up using nvm. The first install worked and this is the location that you need to enter for cloud9 to work.

```
which nodejs

/usr/bin/nodejs
```

## Cloud9 installing python 2.7

Cloud9 requires python 2.7 to work. [Here's a tutorial on how to install python 2.7](https://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/) without replacing the python3 version that already exists on the system.

```
sudo apt-get update
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

cd /usr/src
sudo wget https://www.python.org/ftp/python/2.7.17/Python-2.7.17.tgz
sudo tar xzf Python-2.7.17.tgz

cd Python-2.7.17
sudo ./configure --enable-optimizations
sudo make altinstall
```

Finally check the version that installed:

```
python2.7 -V
Python 2.7.17

which python2.7
/usr/local/bin/python2.7
```

At this point in the installation cloud9 succeeds in the installation of the required packages! Time to start actually creating pages!

# Creating a HTML directory for a custom coded HTML site
