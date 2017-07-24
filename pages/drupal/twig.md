---
layout: default
---

# Overriding the Front page Template

What content do i want to add to the Braindead Designs homepage?
- [x] Add a New Banding region to the theme
- [x] Make a Top section for Site logo and search bar. Call it Branding
- [x] Make a Slider section below the menu

What Styling do I want to add to the homepage?
- [x] Bigger Menubar
- [ ] Better Colors #191919 yellow menu #e8e8e8 Headers #ffcc00 text #80c959 green highlight

## Variables

Name | Usage
------------ | -------------
base_path | base URL path of the Drupal installation. usually "/"
is_front | A flag indicating if the current page is the front page.
logged_in | A flag indicating if the user is registered and signed in.
is_admin | A flag indicating if the user has permission to access administration pages.


Any images need to be linked from the root directory.

`<img src="/themes/bdd_theme/images/Hitman_Logo.png">`

# Adding a New Region

1. Add a new region by adding to the THEMENAME.info.yml
2. Then add {{page.new-region}} wherever you want the region to actually print out. I've added branding and slider but only to the front page.

Instead of learning Twig, I'm going to focus on styling because the Paragraphs module has handled much of the twig work. All I need to really do is cut and paste the code of the templates that Paragraphs provides.

I found out that I can mix SASS and SCSS. I just have to make sure the file watchers are running in phpStorm.

```<link href="//maxcdn.bootstrapcdn.com/font-awesome/4.2.0/css/font-awesome.min.css" rel="stylesheet" />
<link href="http://fonts.googleapis.com/css?family=Shadows+Into+Light" rel="stylesheet" type="text/css" /><script src="https://use.fontawesome.com/bcca18a581.js"></script>
<div class="container">
	<div class="row">
    <div class="col-md-12">
      <div class="col-md-6 .col-md-offset-3">
           <ul class="social"><li class="facebook"><a href="https://www.facebook.com/BraindeadDesignShop/"><i class="fa fa-facebook fa-3x"></i></a></li>
            <li class="etsy"><a href="https://www.etsy.com/shop/BraindeadDesign"><i class="fa fa-etsy fa-3x"></i></a></li>
            <li class="twitter"><a href="https://twitter.com/braindeadpins"><i class="fa fa-twitter fa-3x"></i></a></li>

          </ul></div>
    </div>
    </div>
</div>```
