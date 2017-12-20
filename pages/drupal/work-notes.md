---
layout: default
---
# Work Notes

### Dec 8th

Launching the CSR site today. Activated google analytics and am working on getting all of the broken links updated through the database. There was a link checker module in Drupal 7 but there is no longer one. I'll make the changes directly in the database by searching for the broken link strings and replacing them with the correct `/sites/csr/files/...`. [I think I'll also post the python database update code I was using on drupal exchange.](https://drupal.stackexchange.com/questions/251808/how-to-properly-transfer-content-into-druapl-8-from-an-external-source)

Database update broken links
```
UPDATE node__body
SET body_value = REPLACE(body_value, '/sites/default/files', 'sites/csr/files');
UPDATE node_revision__body
SET body_value = REPLACE(body_value, '/sites/default/files', 'sites/csr/files');
```

### Dec 14

#### Composer Issues
Found an issue with the csv export on the CEPS site. I'm trying to fix with composer. [Thread](https://www.drupal.org/project/csv_serialization/issues/2728541)
```
composer require league/csv 8.x-dev
composer require drupal/csv_serialization
composer update drupal/csv_serialization
```
The error messages tell you what versions are compatible with your needed packages.

### Dec 19

Working towards finished Sorensen content. Updated the blue-button-bordered class so it works on a link directly. Also now if can be called a .bbb class.
Created a Webform that is attached to the Person content type. It grabs the email of the current person using the [current-page:url:args:last] token which is set by making the Person content type automatically generate a URL where the last argument is the email of our Person. Got the webform working properly.

The homepage has some custom html and css that gets deleted on every new save. Can't figure out why.
```
<div id="custom-social-float">
<a class="fa-icon-link" href="https://www.facebook.com/SorensenUVA/"><i aria-hidden="true" class="fa fa-facebook-square"></i></a>
<a class="fa-icon-link" href="https://twitter.com/sorensenuva?lang=en"><i aria-hidden="true" class="fa fa-twitter-square"></i></a>
</div>
```
