---
layout: default
---

[Allow for the Linux subsystem on Windows](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/)

You need to download a linux disto from the Windows store by running
```
lxrun /install
```
After enabling it, type bash in the search and run it.

`cd /mnt/c/Users/miles/Documents`

[Installing Ruby](https://www.digitalocean.com/community/tutorials/how-to-install-ruby-and-set-up-a-local-programming-environment-on-windows-10)

```bash
sudo apt-get install python
gem install bundler
gem install pkg-config -v "~> 1.1.7"
sudo apt-get install libxslt-dev libxml2-dev
sudo apt-get install libxml2
gem install nokogiri -- --use-system-libraries
sudo apt install nodejs-legacy
```

## Installing ruby and adding things to the path
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
