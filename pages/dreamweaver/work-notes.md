---
layout: default
---

# Dreamweaver Setup

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

## Shortcuts

`F12`  - opens up the browser live preview
`CNTRL + E` - Quick edit the stylesheet from within the HTML  

I was really hopeful for the quick edit function for sass. Unfortunately quick edit only lets you edit the compiled css and not the sass. That sucks.

## Dynamically creating New Items

```JavaScript
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script><script type="text/javascript">
    function create(htmlStr) {
      var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
      temp.innerHTML = htmlStr;
      while (temp.firstChild) {
        frag.appendChild(temp.firstChild);
      }
      return frag;
    }

    $.ajax({
      url: 'https://api.rss2json.com/v1/api.json',
      method: 'GET',
      dataType: 'json',
      data: {
        rss_url: 'https://us6.campaign-archive.com/feed?u=ad59b4c4385511a9ec177859c&id=16860b7f9e',
        api_key: 'ourf2jvebbdifvv8g98zaunzzdky69ciafk8fzig', // put your api key here
        count: 2
      }
    }).done(function(response) {
      if (response.status != 'ok') {
        throw response.message;
      }

      console.log('====== ' + response.feed.title + ' ======');

      var item = response.items[0];
      console.log(item.title);
      console.log(item.content);
      console.log(item.pubDate);
      console.log(item.link);
      console.log(item.pubDate);
      console.log(item);

      var fragment = create("<a href='" + item.link + "'><h3>" + item.title + "</h3></a><span>" + item.pubDate + "</span><p>" + item.content + "</p>");
      document.getElementById('rss_feed').append(fragment);
    });
  </script>
```

http://www.facebook.com/uvavpr
http://www.virginia.edu/vpr
vpresearch@virginia.edu
http://www.twitter.com/uvavpr

If the xml data contains a &nbsp the title gets split up a lot. So to check for that you check the actual charechater.

https://stackoverflow.com/questions/5237989/nonbreaking-space
```
var x = td.text();
if (x == '\xa0') { // Non-breakable space is char 0xa0 (160 dec)
  x = '';
}
```

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

2/6/20
# Adding and using bootstrap

How do I optionally add it to pages. And give me an overview of bootstrap.
