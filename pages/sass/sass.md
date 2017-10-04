 ---
layout: default
---
#SASS phpFileStorm setup Sass
![Screenshot of setup](assets/images/Screen Shot 2017-09-05 at 3.17.44 PM.png)
```
/Users/miles/.rvm/gems/ruby-2.4.1/bin/sass
$FileName$:$FileNameWithoutExtension$.css
$FileNameWithoutExtension$.css:$FileNameWithoutExtension$.css.map
```

### Make sure that the CSS and JS optimization are off on the Performance page

# phpStorm File Watcher Setup SCSS
You need to get it to update continuously
**Program: /Users/miles/.rvm/gems/ruby-2.4.1/bin/scss**
Arguments: --no-cache --update $FileName$:$FileNameWithoutExtension$.css
Output paths to refresh: $FileNameWithoutExtension$.css:$FileNameWithoutExtension$.css.map

Sass is easier but having all of these preset css values is horrible.

I found a great trick for editing multiple lines at once in phpStorm.
The alt key adds a new cursor so you can type in two places at once.

Get rid of the .header margin
```css
#search-block-form > div > div , #edit-submit {
    margin-top: 10px;
}

#footer {
    background-color: #002654;
    color: #ffffff;
    position: absolute;
    right: 0;
    bottom: 0;
    left: 0;
    padding: 1rem;
    margin-bottom: 0;
}

*,
*:before,
*:after {
  box-sizing: inherit;
}

```

Here's a great codepen on [getting a footer to actually stick to the bottom of the page](https://codepen.io/cbracco/pen/zekgx). It recommends that you set the foother to absolute bottom and then add bottom padding to the parent element of the footer to equal height of the footer. Without that padding if the content reached the footer they would hide each other instead of pushing the footer lower. The height of the page needs to be at least 100% to push the footer off.


http://ceps.dd:8083/sites/ceps/files/default_images/3-2_0073_samuel-zeller-34751.png
