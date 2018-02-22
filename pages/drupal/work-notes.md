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
drush config-import --partial --source=modules/custom/lost/config/install/
drush mi migration_lost_test2
```

Once the yaml config is imported, this can be run by cron at various times using System cron.

ATTEMPT TO RUN THE CUSTOM MIGRATION WITH THE EXAMPLE DATA!!!

https://www.mtech-llc.com/blog/lucas-hedding/migrating-using-csv
https://www.mtech-llc.com/blog/ada-hernandez/how-migrate-images-drupal-8-using-csv-source

### Running Example Custom MIGRATION

1. Install Drupal site new Drupal 8.4
2. Install Migrate, Migrate Source CSV, Migrate Plus, Migrate Tools
```
drush en -y  migrate_plus migrate_tools migrate_source_csv
drush en -y admin_toolbar
```
3. Make sure drush is installed
```
drush --version
Drush Version   :  8.1.10

WE NEED SOMETHING ELSE
composer require drush/drush:8.*
drush --version
Drush Version   :  8.1.15
```
4. Create your content type for Profile type as described
First Name - Text(plain)
Last Name - Text(plain)
Email - Email
Language - Taxonomy Term
5. Create a custom module in the custom module folder
  - create the cuustom_migrate.info.yml that hadles the installation of the module
  - Create the migrate_plus.migration.profile.yml file that describes the migration for our Profile type
6. Enable the custom migrate module in drush `drush en custom_migrate`
7. Create the CSV file in excel and make sure you save it in WINDOWS CSV FORMAT
8. Run `drush cex` and `drush ms`
```
Group: Default (default)  Status  Total  Imported  Unprocessed  Last imported
profile                   Idle    1      0         1
```
8. Run drush mim profile
```
drush mim profile
```
9. If it fails then make sure that you roll it back and import the fixed configuration
```
drush mr profile
drush config-import --partial --source=modules/custom_migrate/config/install
drusm migrate-import profile
```

## Attempt 2 at getting LOST migrations

```
drush config-import --partial --source=modules/custom/lost/config/install/

```

## Sorensen Alumni Directory

So we have some seperate users who can see seperate things.
Alumni Profile
1. Name (First Middle Last Suffix Preferred)
2. Image
3. Program (Program and Year multiple) `ELP 2016`
4. DOB
5. Gender
6. Political Party
7. Race
8. Region
9. Mobile Phone
10. Home Phone
11. Work Phone
12. Preferred email
13. Alt Email
14. Title
15. Organization (Organization and Department)

I created the basic migration with all of the CSV fields now I want to enable and run the migration. Enable all of the needed migration modules before importing the migration configuration.
```
drush --version
Drush Version   :  8.1.16

drush en sorensen_alum -y
drush config-import --partial --source=modules/custom/sorensen_alum/config/install/
drush ms
 Group: sorensen (sorensen)         Status    Total  Imported  Unprocessed  Last imported       
 alum_2                             Idle      124    0         124                       

drush migrate-import alum_2
 Processed 124 items (124 created, 0 updated, 0 failed, 0 ignored) - done with 'alum_2'
```

To run this migration on a specific site, make sure you are in the site directory so drush runs into your settings.php file.

List of the process plugins I'll be using.
https://www.drupal.org/docs/8/api/migrate-api/migrate-process-plugins
https://www.drupal.org/docs/8/api/migrate-api/migrate-process-plugins/list-of-core-process-plugins

If you use more than one plugin then you need to use an associative array to show the order of the plugins.

Rather than stress about getting the terms into the correct list during the initial migration, I'll just merge the separate fields with a module later.

[Example of updating nodes with a module](https://docs.acquia.com/tutorials/fast-track-drupal-8-coding/attach-terms-another-entity-programmatically)

```
D8 Code
Place the following in lotus.module

<?php
use Drupal\node\Entity\Node;

/**
 * Before attaching a term(s) to a term reference field,
 * Must know:
 *   - field_example_name: the full name of the term reference field
 *   - tid: the term ID(s) to attach
 *
 * Keep in mind that this example uses Node::load()
 * but you can use any Entity::load()
 * e.g. User::load(), Term::load(), etc.
 */


// Example 1: attaching a single term
$node = \Drupal\node\Entity\Node::load($nid);

// Attach only one term
$tid = 1; // The ID of the term to attach.
$node->set('field_example_name', $tid);
$node->save();
// End of Example 1 />

// Example 2: attaching multiple terms
$node2 = \Drupal\node\Entity\Node::load($nid2);

// To attach multiple terms, the term IDs must be in an array.
$multiple_tids = array(1, 2, 3); // Each is Term ID of an existing term.
$node2->set('field_example_name', $multiple_tids);  // Note that field_example_name must allow multiple terms.
$node2->save();
// End of Example 2 />
```

## Migrate the Users

https://agencychief.com/blog/drupal-8-csv-migration

You can define the source database connection in setting php and then specify which database connection to use as source in your source plugin. The default key is the migrate key so `$databases[migrate][default]`

https://www.drupal.org/docs/8/api/migrate-api/migrate-source-plugins/migrating-data-from-a-sql-source

## Migrate Headshots

https://www.mtech-llc.com/blog/ada-hernandez/how-migrate-images-drupal-8-using-csv-source

Create another migration and use the name of that migration as the plugin for your photo field.

So the photos migration is not actually assigning the image to the Alumni Profile. It is creating the file entity in the database though. I will create a custom plugin to manually attach that file entity to the field.

In the migrate_map_photo field, we get the destination ID of the photo. For my example it is 67199. I want to attach that ID to my Alumni Profiles. The filename is generated from the name of the client so it shouldn't be hard to get the value of the FID by searching the file_managed table with SQL.

I started by setting the image to a default value like this. The default is a File I know exists in the database.
```
field_image:
  plugin: default_value
  default_value: 67199
```

So I want to make my own process plugin and use the name from the CSV file to find the file. I'll need to concat the name and then pass that value to my process plugin. Use Bethal Abraham for the name of the file.

So first you need to export all of the images from filemaker. Then you import all of them into the database using the ICME file browser. It automatically creates all of the images.

I'm using the same /update-alumni url to cause the alumni object fixes.

Ms. Bethal  Abraham
Ms. Bethal Abraham.jpg

Here is the php code that attaches the image to the alumni profile. 

```
function attachHeadshotToAlumniProfile($node)
{
    $title = $node->getTitle();
    $explode = explode(' ', $title);
    $title_normalized = '';
    foreach($explode as $word)
    {
        if($word != ''){
            $title_normalized .= $word . ' ';
        }
    }
    $title_normalized = trim($title_normalized);
    $jpg = $title_normalized . ".jpg";
    $png = $title_normalized . ".png";
    $jpgfile = \Drupal::entityQuery('file')->condition('filename', $jpg)->execute();
    $pngfile = \Drupal::entityQuery('file')->condition('filename', $png)->execute();
    if($pngfile)
    {
        $node->set('field_image', $pngfile);
        $node->save();
        drupal_set_message( "Node with nid " . $node->id() . " got a headshot! ". $png . "\n");
    }
    if($jpgfile)
    {
        $node->set('field_image', $jpgfile);
        $node->save();
        drupal_set_message( "Node with nid " . $node->id() . " got a headshot! ". $jpg . "\n");
    }
    return;
}
```


## Install xDebug for Drupal [https://docs.acquia.com/dev-desktop/sites/phpstorm](Guide)

I've reached a point where I need to be able to step through code and see a fall stack to really understand what is going on. I want to get a debugging tool for php. I know this will be painful to install but I have to try. I had to switch to PHP 5.6.29 to get the xdebug utility built into Acquia Dev Desktop.

Uncomment this line by removing the semi colon in the right php.ini
```
zend_extension="/Applications/DevDesktop/php5_6/ext/xdebug.so"

Add this line too
xdebug.remote_enable=1
```

#### Fix the xdebug issue of it breaking on the first line no matter what.

To get it to stop I did this (on OS X):
Go to Preferences > Languages & Frameworks > PHP > Debug
Uncheck both of the 'force break at the first line...' options
Apply and close
In the Run menu, uncheck 'Break at the first line in PHP scripts'

## Install Drupal Console

These two tutorials failed to work. DEAD END.

[Install overview](https://drupalize.me/tutorial/drupal-console?p=2766)

[How to install](https://drupalconsole.com/articles/how-to-install-drupal-console)

## Manually create a module and use it to update all of the Alumni profiles

First I need to read up on Drupalize.me to find out how to make a module. Then I need to learn how to invoke it and test it with a debugger.

git clone https://github.com/sidharrell/D8HWexample.git

[Drupal Docs for creating modules.](https://www.drupal.org/docs/8/creating-custom-modules) Make sure you enable the module with drush and also install it through the Extend screen.

So using xdebug on this basic request for a specific node, I was able to find the core class that is responsible for getting my Node entity.
```
$node = \Drupal\node\Entity\Node::load(119167);

core/lib/Drupal/Core/Entity/Entity.php
```

There is a load multiple option that would allow me to load a lot of them if I could get ahold of the ids for all of the Alumni Profile content. So how do I get ahold of all of those node IDs?

```
$nids = \Drupal::entityQuery('node')->condition('type','my_custom_type')->execute();
$nodes =  \Drupal\node\Entity\Node::loadMultiple($nids);

$tid = $node->get('field_class')->target_id;
$term_id = \Drupal\taxonomy\Entity\Term::load($tid)->get('tid')->value;
$term_name = \Drupal\taxonomy\Entity\Term::load($tid)->get('name')->value;
```

So I kept getting these Objects that had lists and arrays in them. I couldn't get what I wanted so I used the get method to go all the way to the data.


Updated the Alumni after checking for admin role.
```
if (\Drupal\user\Entity\User::load(\Drupal::currentUser()->id())->hasRole('administrator'))
```

## Extract the photos from filemaker

That export field contents can be done from a script that loops through the records of your found set to export all the images to a specified location all in one go.

This will export the images to your desktop. Variations of it would export to other locations:

Perform after you have found your records
```
Go To Record [First]
Loop
   Set Variable [$Path ; value: Get ( DesktopPath ) & YourTable::ImageName & ".jpg"]
   Export Field Contents [YourTable::YourcontainerField ; $Path ]
   Go To Record [ next ; exit after last ]
End Loop
```
This script assumes that you have one image per record, that each record also has a field that can be used to unique name the file and that all of the images are JPEGs.

## Create Users in Druapl

[Example Usre Migration from CSV](http://valuebound.com/resources/blog/how-to-migrate-users-from-a-csv-file-drupal-8)

```
drush config-import -y --partial --source=modules/custom/sorensen_alum/config/install/
drush ms
drush migrate-import alumni_users
```

Now that I have the users, I need to connect them to the actual Alumni Profiles as the author. I need to make a [custom process plugin.](https://drupalize.me/tutorial/write-custom-process-plugin?p=2578)

There may be an easier way. There is a MigratioLookup plugin that can look up the uid of our recently migrated Users. the alumni_users migrateion which has to happen before this data migration created 4 users with uids. So in process I need to add the following.
```
process:
  uid:
    plugin: migration_lookup
    migration: alumni_users
    source: sid
```

This looks at the key for the user migration and finds the user that was created with that key.

## Rough friday - migration for LOST content

```
drush en -y migrate_tools
drush en -y lost
drush config-import -y --partial --source=modules/custom/lost/config/install/
