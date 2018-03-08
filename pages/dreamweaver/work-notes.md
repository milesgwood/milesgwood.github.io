---
layout: default
---

# Dreamweaver Setup

I downloaded the 2017 version of Dreamweaver and it is working on my home machine as well as my laptop machine. First tutorial to follow is [this one that Annette linked me](https://char.gd/blog/2017/how-to-set-up-the-perfect-modern-dev-environment-on-windows).

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

Next Steps
- Get remote access  
- [Setup SASS preprocessor](https://helpx.adobe.com/dreamweaver/using/css-preprocessors.html)
- Create a git key?  

## Shortcuts

F12  - opens up the browser live preview
CNTRL + E - Quick edit the stylesheet from within the HTML  

I was really hopeful for the quick edit function for sass. Unfortunatley quick edit only lets you edit the compiled css and not the sass. That sucks.
