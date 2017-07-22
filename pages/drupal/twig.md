---
layout: default
---

# Overriding the Front page Template

What content do i want to add to the Braindead Designs homepage?
- [x] Add a New Banding region to the theme
- [x] Make a Top section for Site logo and search bar. Call it Branding
- [ ] Make a Slider section below the menu

What Styling do I want to add to the homepage?
- [ ] Bigger Menubar
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

Add a new region by adding to the THEMENAME.info.yml and then adding {{page.new-region}} wherever you want the region to actually print out. I've added branding but only to the front page.

Instead of learning Twig, I'm going to focus on styling because the Paragraphs module has handled much of the twig work. All I need to really do is cut and paste the code of the templates that Paragraphs provides.

I found out that I can mix SASS and SCSS. I just have to make sure the file watchers are running in phpStorm.
