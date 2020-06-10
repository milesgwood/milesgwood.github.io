---
layout: default
---

# Dreamweaver Setup References

[General Setup Tutorial](https://char.gd/blog/2017/how-to-set-up-the-perfect-modern-dev-environment-on-windows).
[Setup SASS preprocessor](https://helpx.adobe.com/dreamweaver/using/css-preprocessors.html)

## Install Hyper as bash tool

Hyper is a command line emulator based in js html and css. I installed it default and then edited one line in the .hyper.js file ` C:\Users\{userName}\.hyper.js` to make it run bash instead of windows cmd. Now that I have hyper running bash, I needed to [reset my bash password](https://askubuntu.com/questions/772050/reset-the-password-in-linux-bash-in-windows) since I had forgotten it. I had to force windows to make a new password for milesgwood [using this help](https://docs.microsoft.com/en-us/windows/wsl/user-support).

Setup modern dev environment
```
curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
sudo apt-get install nodejs
sudo apt-get update && sudo apt-get install build-essential nginx mysql-server ruby ruby-bundler nodejs git  ruby-dev
```

I found out about a windows package manager like homebrew. It's called [Chocolatey](https://chocolatey.org/).

I still need to generate a git key so that I don't need to enter a git password. [Where to put you git password.](https://github.com/settings/keys)


## Creating Dreamweaver Templates

So you need to create a dwt template for all of the home pages.
1. Create new template
2. Create the child pages from template
3. Edit the templates with correct links
4. Tools > Templates > Update Pages with new template
5. Make sidemenu links with Windows > Properties window and the Design View
6. Click HTML and then drag the target to the html page you want to edit
7. Make Editable regions (Select the area > Insert > Template > Editable Region)

# Starting local npm server

You can use a node server instead of the dreamweaver one. That way the markup is cleaner.
```
npm --version
6.10.0
npm install http-server -g
http-server /mnt/w/milesgreatwood.com
```
