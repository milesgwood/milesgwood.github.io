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

I was really hopeful for the quick edit function for sass. Unfortunatly quick edit only lets you edit the compiled css and not the sass. That sucks.

## Working request for news items
```
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

      // for (var i in response.items) {
      //   var item = response.items[i];
      //   console.log(item.title);
      //
      // }

      var item = response.items[0];
      console.log(item.title);
      console.log(item.content);
      console.log(item.pubDate);
      console.log(item.link);
      console.log(item.pubDate);
      console.log(item);

      var fragment = create("<a href='" + item.link + "'><h3>" + item.title + "</h3></a><span>" + item.pubDate + "</span><p>" + item.content + "</p>");
      // You can use native DOM methods to insert the fragment:
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

## Response to annette's Comments

Glad Cheryl seems happy. I'll definitely focus on getting more pages out faster. I spent much more time than I should have getting the Recent News to automatically populate.

 - As far as managing the scss and sass changes, I think the easiest solution would be to have separate style sheets. Right now the homepage is importing bootstrap.css, brand.css and vpr.css. I'll keep all of my changes in vpr.sass. That way I can just pull any changes you make without fear of conflicts. Our other alternative is to use a git repo but that still doesn't solve the issue of having to convert between css sass and scss. There are tools to do the conversions but I think separate stylesheets would be simpler.

 - Should I be making logos for these new pages or do they already exist somewhere? I'm all for getting to use my illustrator skills a bit to make logos. I just don't want to step on any toes if people already have logos.

 - I think you and cheryl are right about a separate News page. I'm thinking 3 news items on the front page that automatically update, a link in the footer by the social media links for the newsletter page, the news page with the last mailchimp newsletter's worth of news, and a link to an archive of old mailchimp newsletters. My main reason for wanting a link in the footer is that it is the main piece of content I see that is updated frequently and could be set up to auto-populate where needed.

- On contact/directions/location, I think all of the basic info should go in the footer with links to the pages with the same content elaborated.

- I was intending to combine the Leadership page with the staff page, under the title of Leadership. The current biography page is all about Ramasubramanian. I was expecting it to be a history of the organization, not just about him, so I think it fits better in leadership.

- On the content of the News Page. I will look into the UVA Daily site to see if there is a similar rss feed I could grab and populate our news with. For now, I'll leave it as the mailchimp rss feed.

## Start on homepage fixes

So you need to create a dwt template for all of the home pages.
1. Create new template
2. Create the child pages from template
3. Edit the templates with correct links
4. Tools > Templates > Update Pages with new template
5. Make sidemenu links with Windows > Properties window and the Design View
6. Click HTML and then drag the target to the html page you want to edit
7. Make Editable regions (Select the area > Insert > Template > Editable Region)
