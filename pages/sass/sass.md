---
layout: default
---

# phpStorm File Watcher Setup
You need to get it to update continuously
Program: /Users/miles/.rvm/gems/ruby-2.4.1/bin/scss
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

```css
.footer {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  padding: 1rem;
}


```




.navbar-default {
  position: fixed;
  top: 0px;
  left: 0px;
  z-index: 20000;
  background-color: #002f6c; }
  .navbar-default .navbar-header, .navbar-default .region-navigation-collapsible {
    margin: 0px auto; }
    .navbar-default .navbar-header .logo img, .navbar-default .region-navigation-collapsible .logo img {
      height: 50px;
      width: auto; }
    .navbar-default .navbar-header .navbar-brand.name, .navbar-default .region-navigation-collapsible .navbar-brand.name {
      font-family: "franklin-gothic-comp-urw", "Arial Narrow", sans-serif;
      color: #fff;
      font-size: 24px;
      line-height: 50px;
      margin: 8px;
      padding: 0px; }
    .navbar-default .navbar-header #block-coopercenter-main-menu, .navbar-default .region-navigation-collapsible #block-coopercenter-main-menu {
      width: 100% !important; }
    .navbar-default .navbar-header #ux-search, .navbar-default .region-navigation-collapsible #ux-search {
      position: absolute;
      height: 30px;
      width: 235px;
      right: 10px;
      top: 10px; }
      .navbar-default .navbar-header #ux-search #ux-search-input, .navbar-default .navbar-header #ux-search #ux-search-button, .navbar-default .region-navigation-collapsible #ux-search #ux-search-input, .navbar-default .region-navigation-collapsible #ux-search #ux-search-button {
        height: 30px;
        position: absolute;
        top: 0px; }
      .navbar-default .navbar-header #ux-search #ux-search-input, .navbar-default .region-navigation-collapsible #ux-search #ux-search-input {
        width: 200px;
        top: -100px;
        z-index: 100;
        opacity: 0;
        -webkit-transition: all 500ms;
        -moz-transition: all 500ms;
        -ms-transition: all 500ms;
        -o-transition: all 500ms;
        transition: all 500ms; }
      .navbar-default .navbar-header #ux-search #ux-search-button, .navbar-default .region-navigation-collapsible #ux-search #ux-search-button {
        width: 30px;
        font-size: 30px;
        color: #E57200;
        right: 0px;
        z-index: 200; }
      .navbar-default .navbar-header #ux-search.active #ux-search-input, .navbar-default .region-navigation-collapsible #ux-search.active #ux-search-input {
        top: 0px;
        opacity: 1; }
  .navbar-default .navbar-collapse {
    background-color: #dadada;
    margin-bottom: 0px; }
    .navbar-default .navbar-collapse .navbar-nav {
      font-family: "franklin-gothic-comp-urw", "Arial Narrow", sans-serif;
      font-size: 14px;
      width: 100%; }
      .navbar-default .navbar-collapse .navbar-nav > li {
        float: none;
        display: inline-block; }
        .navbar-default .navbar-collapse .navbar-nav > li > a {
          display: inline-block;
          color: #002f6c;
          font-family: "franklin-gothic-comp-urw", "Arial Narrow", sans-serif;
          text-transform: uppercase;
          line-height: 47px;
          padding: 0px 10px; }
        .navbar-default .navbar-collapse .navbar-nav > li.active {
          background-color: rgba(0, 0, 0, 0.1); }
          .navbar-default .navbar-collapse .navbar-nav > li.active > a {
            background-color: transparent !important; }
        .navbar-default .navbar-collapse .navbar-nav > li.open {
          background-color: rgba(255, 255, 255, 0.25); }
          .navbar-default .navbar-collapse .navbar-nav > li.open > a {
            background-color: transparent !important; }
        .navbar-default .navbar-collapse .navbar-nav > li:hover {
          background: white; }
          .navbar-default .navbar-collapse .navbar-nav > li:hover > a {
            color: #E57200; }
        .navbar-default .navbar-collapse .navbar-nav > li > .dropdown-menu {
          border: none; }
          .navbar-default .navbar-collapse .navbar-nav > li > .dropdown-menu > li > a {
            background-color: transparent !important;
            color: #002f6c; }
          .navbar-default .navbar-collapse .navbar-nav > li > .dropdown-menu > li:hover > a {
            color: #E57200; }
