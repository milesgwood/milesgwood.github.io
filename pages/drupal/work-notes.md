---
layout: default
---
# Work Notes

## Dec 8th

Launching the CSR site today. Activated google analytics and am working on getting all of the broken links updated through the database. There was a link checker module in Drupal 7 but there is no longer one. I'll make the changes directly in the database by searching for the broken link strings and replacing them with the correct `/sites/csr/files/...`. [I think I'll also post the python database update code I was using on drupal exchange.](https://drupal.stackexchange.com/questions/251808/how-to-properly-transfer-content-into-druapl-8-from-an-external-source)

Database update broken links
```
UPDATE node__body
SET body_value = REPLACE(body_value, '/sites/default/files', 'sites/csr/files');
UPDATE node_revision__body
SET body_value = REPLACE(body_value, '/sites/default/files', 'sites/csr/files');
```

## Dec 14

#### Composer Issues
Found an issue with the csv export on the CEPS site. I'm trying to fix with composer. [Thread](https://www.drupal.org/project/csv_serialization/issues/2728541)
```
composer require league/csv 8.x-dev
composer require drupal/csv_serialization
composer update drupal/csv_serialization
```
The error messages tell you what versions are compatible with your needed packages.

## Dec 19

Working towards finished Sorensen content. Updated the blue-button-bordered class so it works on a link directly. Also now if can be called a .bbb class.
Created a Webform that is attached to the Person content type. It grabs the email of the current person using the [current-page:url:args:last] token which is set by making the Person content type automatically generate a URL where the last argument is the email of our Person. Got the webform working properly.

The homepage has some custom html and css that gets deleted on every new save. Can't figure out why.
```
<div id="custom-social-float">
<a class="fa-icon-link" href="https://www.facebook.com/SorensenUVA/"><i aria-hidden="true" class="fa fa-facebook-square"> </i> </a>
<a class="fa-icon-link" href="https://twitter.com/sorensenuva?lang=en"><i aria-hidden="true" class="fa fa-twitter-square"> </i> </a>
</div>
```


scp -rp -i ssh_old_drupal_sites.pem ubuntu@sorensen.coopercenter.org://var/www/html/sorensen.coopercenter.org/*  sorensen-old


## Jan 16

Transferring the remaining scrapped sites to my local machine.
1. vdot.cooper.virginia.edu
2. taxrates.coopercenter.org
3. dev.coopercenter.org

```
scp -i bitnamidrupal.pem ubuntu@www.sorenseninstitute.org://home/ubuntu/migrate/taxrates_d7.sql .
scp -i bitnamidrupal.pem ubuntu@www.sorenseninstitute.org://home/ubuntu/migrate/dev_d7.sql .
scp -i bitnamidrupal.pem ubuntu@www.sorenseninstitute.org://home/ubuntu/migrate/vdot_d7.sql .

scp -rp -i bitnamidrupal.pem ubuntu@www.sorenseninstitute.org://var/www/html/vdot.cooper.virginia.edu/* vdot/
scp -rp -i bitnamidrupal.pem ubuntu@www.sorenseninstitute.org://var/www/html/dev.coopercenter.org/sites/all/* dev2/
scp -rp -i bitnamidrupal.pem ubuntu@www.sorenseninstitute.org://var/www/html/dev.coopercenter.org/* dev2/
scp -rp -i bitnamidrupal.pem ubuntu@www.sorenseninstitute.org://var/www/html/taxrates.coopercenter.org/* taxrates/
```

Once all of those are copied over I'll create a local drupal 7 site to house them in and then transfer them to D8.

## Jan 17

Demographics jump links are broken. Here's a javascript fix that works if the page is loaded with the # added. I think it will work better if it is loaded before the page loads.
```
<script>
var shiftWindow = function() { scrollBy(0, -50) };
if (location.hash) shiftWindow();
window.addEventListener("hashchange", shiftWindow);
</script>
```

### Migration

Now I have to transfer out all of the Publications but that can wait a while. I'm at the clone D8 clone site and using the migrate tools transfer the content from d7 -> d8 format automatically.

### JSON API

I want to work on getting a working JSON API call in a test drupal site.
https://drupalize.me/tutorial/install-json-api?p=3003
https://ftp.drupal.org/files/projects/jsonapi-8.x-1.7.tar.gz

The JSON API lets you request drupal content in JSON format. For examples

```
http://uvacooper.dev-clone.dd:8083/jsonapi/node/cooper_center_units
http://uvacooper.dev-clone.dd:8083/jsonapi/node/cooper_center_units?page[limit]=2&page[offset]=3
http://uvacooper.dev-clone.dd:8083/jsonapi/node/cooper_center_units?sort=-created
```

We get all of the center units content type. Then we get 2 of them from offset 3. The last orders them by creation date with the newest first.


Possible use for this migrate from CSV tutorial.
https://www.drupal.org/docs/8/api/migrate-api/migrate-source-plugins/migrating-data-from-a-csv-source

Possible use for migration from previous SQL database.
https://www.drupal.org/docs/8/api/migrate-api/migrate-source-plugins/migrating-data-from-a-sql-source
