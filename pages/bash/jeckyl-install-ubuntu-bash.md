---
layout: default
---

Installing linux bash on windows you get a weird path to your user directory. You have to move to weirdly specific folder. I'll do most of my work in Documents.

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
