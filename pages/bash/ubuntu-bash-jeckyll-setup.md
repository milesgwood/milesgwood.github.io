---
layout: default
---

[Allow for the Linux subsystem on Windows](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/)

You need to download a linux disto from the Windows store by running
```
lxrun /install
```
After following the article linked to enable bash, type bash in the search and run it. The home of your linux distro will be in AppData and can't interact with your windows explorer browser. You can see Windows files though in bash. Windows is linked at `/mnt/c`.

`cd /mnt/c/Users/miles/Documents`

[Installing Ruby](https://www.digitalocean.com/community/tutorials/how-to-install-ruby-and-set-up-a-local-programming-environment-on-windows-10)

Install python and Ruby and these libraries one time

```
sudo -i
apt-get install python
apt-get install ruby-all-dev
gem install bundler
gem install pkg-config -v "~> 1.1.7"
apt-get install libxslt-dev libxml2-dev
apt-get install libxml2
apt-get install build-essential
gem install nokogiri -- --use-system-libraries
apt install nodejs-legacy
```

apt-get install libgmp-dev


Throw in a `apt update && apt upgrade` if it fails at any point.

Then you can run the run script in this repo which does the rest of the jeckyll serving and hosting of the local version of these pages.

## Adding things to the path
set PATH=%PATH%;C:\Ruby200-x64\bin

## Fixing Forgotten Bash Password
Run bashand make a note of your Linux username (this need not match your Windows username)
In Windows admin command prompt (Super+X, A) change the default user to root:
`lxrun /setdefaultuser root`
Now Bash on Ubuntu on Windows logs you in as root without asking password
Use passwd command in Bash to change the user password:
`passwd your_username`
Change the default user back to your normal user in Windows command prompt
`lxrun /setdefaultuser your_username`
