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


### IE CSS fixes

So the sites look awful in IE. No surprise there really. So I need to fix the css since 12% of our users are still using IE. I added this code to the html.html.twig file.

```
<!--[If IE]>
    <link rel="stylesheet" type="text/css" href="themes/coopercenter_units/css/ie.css">
<![endif]-->
```

SO to test my CSS fixes, I am going to install Windows 10 on a virtual machine hosted on this work computer.
1. Install VirtualBox

[Activating Windows](http://its.virginia.edu/software/mslicenses/activate.html)
```
Windows 7 and Server 2008 R2 Activation
Connect your computer to the UVA network (if on Grounds, via a wired or wireless connection to the UVA network; if remotely, via the UVA Anywhere VPN).
Verify your computer has the correct date, time, and time zone (Eastern).
Navigate to Start, then All Programs, then Accessories.
Right-click on the Command Prompt icon and click Run as administrator.
Click the Continue or Yes button on the dialog window that appears.
The path (e.g., C:\Windows\system32) should contain the word “Windows” and not “Users”. If it contains “Users”, close the window and repeat the two previous steps, being sure to open the Command Prompt as an administrator.
Copy and paste (or type) the command slmgr.vbs /skms skms.eservices.virginia.edu and press the Enter key.
Either “Key Management Service machine name set to skms.eservices.virginia.edu successfully” or an error message will be returned.
If not successful, ensure you typed the command correctly. There is a space between slmgr.vbs and /skms and between /skms and skms.eservices.virginia.edu
Copy and paste (or type) the command slmgr.vbs /ato and press the Enter key.
Either “Product activated successfully” or an error message will be returned. If you receive an error, contact the UVA Help Desk.
Exit the command prompt window by typing exit followed by pressing the Enter key.
Click the Start button.
Right-click on Computer and click Properties. Under Windows activation:
You should see “Windows is activated.” If you see “Product Activation Required” instead, contact the UVA Help Desk for assistance.
```

### Demographics Zoom Lense

https://demographics.coopercenter.org/node/7256

[Getting JQuery](https://stackoverflow.com/questions/7474354/include-jquery-in-the-javascript-console)
```
var jq = document.createElement('script');
jq.src = "https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js";
document.getElementsByTagName('head')[0].appendChild(jq);
// ... give time for script to load, then type (or see below for non wait option)
jQuery.noConflict();
```

### Getting Data into drupal from csv

So I want to get a couple sources of data directly into the Drupal database. I have to get LOST data in the CEPS site, Sorensen Alumni into the sorensen site, and Survey Research Data in to the CSR site.

[Here's the drupalize.me walkthrough for the Migrate API.](https://drupalize.me/topic/import-data-migrate-api)

Ultimaetly I'd like to import content from MySQL databases directly.

[From a mySQL database](https://drupalize.me/tutorial/set-migrate-demo-site-and-source-data?p=2578)

1. Define external database in settings.php
2. Create a source Plugin
3. Create Process plugin
4. Create destination plugin
5. Run the plugin with drush

[Source From CSV Plugin](https://drupal.org/project/migrate_source_csv)
[Example Use of CSV Plugin](https://www.mtech-llc.com/blog/lucas-hedding/migrating-using-csv)

#### Running the plugin with drush

 `drush ms` status of migration
 `drush mi <name>` import a site migration (which field is this?)
 `drush mr` rollback the migration


 ```
 drush --version
 Drush Version   :  8.1.10

PHP Fatal error:  Declaration of Drush\Command\DrushInputAdapter::hasParameterOption($values) must be compatible with Symfony\Component\Console\Input\InputInterface::hasParameterOption($values, $onlyParams = false) in /Applications/DevDesktop/tools/vendor/drush/drush/lib/Drush/Command/DrushInputAdapter.php on line 27
```



#### Actually creating the module for install

[tutorial for CSV module making](https://www.mtech-llc.com/blog/ada-hernandez/how-migrate-images-drupal-8-using-csv-source)

1. Create a module folder `lost_csv_import`
2. In that folder make a `lost_csv_import.info.yml`
```
name: My first migration
description: With this module I will migrate a csv file.
type: module
core: 8.x
package: Migration
dependencies:
  - migrate
  - migrate_plus
  - migrate_source_csv
  - migrate_tools
  - node
```
3. Create `config/install` and in that make `migrate_plus.migration.migration_lost_test.yml` (you use the id in the name of the file)
4. Fill that file with the actual migration plugin information
```
dependencies:
  module:
    - migrate_source_csv
id: migration_lost_test
migration_tags:
  - CSV
migration_group: null
label: Lost Migration
source:
  plugin: csv
  path: modules/custom/lost-test.csv
  header_row_count: 1
  keys:
    - locality
  column_names:
    -
      month: Month
    -
      year: Year
    -
      tax: Tax
    -
      locality: Locality
process:
  type:
    plugin: default_value
    default_value: lost
  title:
    plugin: concat
    source:
      - locality
      - month
      - year
    delimiter: ' '
  field_lost_month: month
  field_lost_year: year
  field_lost_tax: tax
  field_lost_locality:
    plugin: entity_generate
    source: locality
destination:
  plugin: 'entity:node'
migration_dependencies:
  required: {  }
  optional: {  }
```
4. Import and run the migration
```
drush mi migration_lost_test
```
My drush version isn't working so I'll try to update it to see if that will help.
```
 drush --version
 Drush Version   :  8.1.10

 composer require drush/drush:9.*
 drush --version
 Drush Commandline Tool 9.0.0

```

Now I get this error where mi isn't defined.
```
drush mi migration_lost_test

[Symfony\Component\Console\Exception\CommandNotFoundException]  
  Command "mi" is not defined.                                    
  Did you mean this?                                              
      pmi      
```
I'm going to try to enable all of the migrate modules to make sure I'm not missing them.
```
drush en migrate_tools
drush en migrate_plus
```
I ended up actually enabling them from the Admin UI because drush en wasn't working properly. mi is still not defined in Drush 9 so I'm going to use drush 8 to see if that helps. `drush list` didn't show any options for migration. It also didn't show any extra module commands.
```
composer require drush/drush:8.*
Drush Version   :  8.1.15
drush cache-clear drush
drush help
```
This shows the migrate commands I need to use.
```
drush help
All commands in migrate_tools: (migrate_tools)
 migrate-fields-sourc  List the fields available for mapping in a source.
 e (mfs)                                                                  
 migrate-import (mi)   Perform one or more migration processes.           
 migrate-messages      View any messages associated with a migration.     
 (mmsg)                                                                   
 migrate-reset-status  Reset a active migration's status to idle.         
 (mrs)                                                                    
 migrate-rollback      Rollback one or more migrations.                   
 (mr)                                                                     
 migrate-status (ms)   List all migrations with current status.           
 migrate-stop (mst)    Stop an active migration operation.
```

Now that I am in drush 8.1.15 instead of 8.1.10, the migrate import seems to be working.
```
drush mi migration_lost_test
No migrations Found
I renamed the migration.yml to the correct name and reinstalled the custom module.
```

Import the configuration
```
drush config-import --partial --source=modules/lost_csv_import/config/install/

```

Now I have the migration configuration imported but when I run migrate-status I get an error that the csv plugin doesn't exist. I fixed it by uninstalling the migrate_source_csv module, then updating composer, and then installing and re enabling the migrate_source_csv module.
```
composer update
drush en migrate_source_csv
drush cr
drush config-import --partial --source=modules/lost_csv_import2/config/install/
drush mi migration_lost_test2
```

Once the yaml config is imported, this can be run by cron at various times using System cron.

ATTEMPT TO RUN THE CUSTOM MIGRATION WITH THE EXAMPLE DATA!!!
