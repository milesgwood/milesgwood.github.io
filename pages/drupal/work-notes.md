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

To make sure it is running properly, start your site locally, then click the start debugger scriptlet in the browser. You should be able to turn on the red phone icon with the PHP Remote Debug configuration named Drupal Debug. NOTE: You may need to change the server each time you want to debug a different local site.


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

[Example User Migration from CSV](http://valuebound.com/resources/blog/how-to-migrate-users-from-a-csv-file-drupal-8)

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
```


## Add click to enlarge to all colorboxes
```
<script>
window.onload = function clickbox(e) {
    jQuery('.colorbox').append("<div>Click to Enlarge</div>");
}
</script>
```

## Fresh run of the migration on a unfucked datatype set

1. Create the Alumni Profile Content Type
2. Create the Alumni Directory Page Content Type
3. Create the Alumni User Type
4. Transfer all of the photos to the correct directory
5. Enable Migration modules
6. Enable Custom Modules
7. Run the migration
8. Run the update that follows migration  /update-alumni
9. Style the Alumni Content


I get failure when I try to install the alumni_profile module. I don't really need it so hopefully the problem will stop. This error seems to have come from bad indent on alumni.content. I FUCKED UP ONE SINGLE INDENT!!!!
```
exception 'Symfony\Component\Yaml\Exception\ParseException' with message 'Indentation problem at line 3 (near "  defaults:").' in /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/symfony/yaml/Parser.php:492                                                                   [error]
Stack trace:
#0 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/symfony/yaml/Parser.php(276): Symfony\Component\Yaml\Parser->getNextEmbedBlock()
#1 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/symfony/yaml/Parser.php(103): Symfony\Component\Yaml\Parser->doParse('alumni.content:...', 2)
#2 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Component/Serialization/YamlSymfony.php(37): Symfony\Component\Yaml\Parser->parse('alumni.content:...', 2)
#3 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Component/Serialization/Yaml.php(35): Drupal\Component\Serialization\YamlSymfony::decode('alumni.content:...')
#4 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Core/Discovery/YamlDiscovery.php(19): Drupal\Component\Serialization\Yaml::decode('alumni.content:...')
#5 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Component/Discovery/YamlDiscovery.php(64): Drupal\Core\Discovery\YamlDiscovery->decode('/Users/miles/Si...')
#6 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Core/Routing/RouteBuilder.php(230): Drupal\Component\Discovery\YamlDiscovery->findAll()
#7 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Core/Routing/RouteBuilder.php(135): Drupal\Core\Routing\RouteBuilder->getRouteDefinitions()
#8 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Core/ProxyClass/Routing/RouteBuilder.php(83): Drupal\Core\Routing\RouteBuilder->rebuild()
#9 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/includes/common.inc(1157): Drupal\Core\ProxyClass\Routing\RouteBuilder->rebuild()
#10 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/includes/utility.inc(52): drupal_flush_all_caches()
#11 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/commands/core/cache.drush.inc(302): drupal_rebuild(Object(Composer\Autoload\ClassLoader), Object(Symfony\Component\HttpFoundation\Request))
#12 [internal function]: drush_cache_rebuild()
#13 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/includes/command.inc(422): call_user_func_array('drush_cache_reb...', Array)
#14 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/includes/command.inc(231): _drush_invoke_hooks(Array, Array)
#15 [internal function]: drush_command()
#16 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/includes/command.inc(199): call_user_func_array('drush_command', Array)
#17 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/lib/Drush/Boot/BaseBoot.php(67): drush_dispatch(Array)
#18 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/includes/preflight.inc(66): Drush\Boot\BaseBoot->bootstrap_and_dispatch()
#19 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/drush.php(12): drush_main()
#20 {main}

Next exception 'Drupal\Component\Serialization\Exception\InvalidDataTypeException' with message 'Indentation problem at line 3 (near "  defaults:").' in /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Component/Serialization/YamlSymfony.php:40
Stack trace:
#0 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Component/Serialization/Yaml.php(35): Drupal\Component\Serialization\YamlSymfony::decode('alumni.content:...')
#1 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Core/Discovery/YamlDiscovery.php(19): Drupal\Component\Serialization\Yaml::decode('alumni.content:...')
#2 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Component/Discovery/YamlDiscovery.php(64): Drupal\Core\Discovery\YamlDiscovery->decode('/Users/miles/Si...')
#3 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Core/Routing/RouteBuilder.php(230): Drupal\Component\Discovery\YamlDiscovery->findAll()
#4 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Core/Routing/RouteBuilder.php(135): Drupal\Core\Routing\RouteBuilder->getRouteDefinitions()
#5 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Core/ProxyClass/Routing/RouteBuilder.php(83): Drupal\Core\Routing\RouteBuilder->rebuild()
#6 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/includes/common.inc(1157): Drupal\Core\ProxyClass\Routing\RouteBuilder->rebuild()
#7 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/includes/utility.inc(52): drupal_flush_all_caches()
#8 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/commands/core/cache.drush.inc(302): drupal_rebuild(Object(Composer\Autoload\ClassLoader), Object(Symfony\Component\HttpFoundation\Request))
#9 [internal function]: drush_cache_rebuild()
#10 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/includes/command.inc(422): call_user_func_array('drush_cache_reb...', Array)
#11 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/includes/command.inc(231): _drush_invoke_hooks(Array, Array)
#12 [internal function]: drush_command()
#13 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/includes/command.inc(199): call_user_func_array('drush_command', Array)
#14 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/lib/Drush/Boot/BaseBoot.php(67): drush_dispatch(Array)
#15 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/includes/preflight.inc(66): Drush\Boot\BaseBoot->bootstrap_and_dispatch()
#16 /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/vendor/drush/drush/drush.php(12): drush_main()
#17 {main}
```

Since I wasted a bunch of time with trying to restore when it was just a simple indent, now my drush version is fucked up too.
```
Performed from docroot

composer require drush/drush:8.1.15

Failed

Problem 1
  - Installation request for drush/drush 8.1.15 -> satisfiable by drush/drush[8.1.15].
  - Conclusion: remove phpdocumentor/reflection-docblock 3.3.2
  - Conclusion: don't install phpdocumentor/reflection-docblock 3.3.2
  - drush/drush 8.1.15 requires phpdocumentor/reflection-docblock ^2.0 -> satisfiable by phpdocumentor/reflection-docblock[2.0.0, 2.0.0a1, 2.0.0a2, 2.0.0a3, 2.0.1, 2.0.2, 2.0.3, 2.0.4, 2.0.5].
  - Can only install one of: phpdocumentor/reflection-docblock[2.0.0, 3.3.2].
  - Can only install one of: phpdocumentor/reflection-docblock[2.0.0a1, 3.3.2].
  - Can only install one of: phpdocumentor/reflection-docblock[2.0.0a2, 3.3.2].
  - Can only install one of: phpdocumentor/reflection-docblock[2.0.0a3, 3.3.2].
  - Can only install one of: phpdocumentor/reflection-docblock[2.0.1, 3.3.2].
  - Can only install one of: phpdocumentor/reflection-docblock[2.0.2, 3.3.2].
  - Can only install one of: phpdocumentor/reflection-docblock[2.0.3, 3.3.2].
  - Can only install one of: phpdocumentor/reflection-docblock[2.0.4, 3.3.2].
  - Can only install one of: phpdocumentor/reflection-docblock[2.0.5, 3.3.2].
  - Installation request for phpdocumentor/reflection-docblock (locked at 3.3.2) -> satisfiable by phpdocumentor/reflection-docblock[3.3.2].

composer require phpdocumentor/reflection-docblock:2.*
composer require drush/drush:8.1.15

drush --version
 Drush Version   :  8.1.15
```

Backed up the database and made a commit with all the drush vendor crap. Getting rid of commas changed the number of rows i mmigrated to fewer. I know I'm definitley still missing some rows too.

I am getting messages saying that the csv line endings are all wrong. That is why i am not getting as many rows as I would expect.

Before I publish I need to restrict permissions possibly using this Group Module.
[Instructions](https://drupal.stackexchange.com/questions/249393/how-to-restrict-access-to-specific-content-types-by-role)




## CSR migrations

```
drush en -y csr_projects_refresh
drush config-import -y --partial --source=modules/custom/csr_projects_refresh/config/install/
drush ms
drush migrate-import csr_projects_refresh
```

```
field_external_principal_investi‎:
  plugin: entity_generate
  entity_type: taxonomy_term
  source: outside_principal_investigator

NO CONFIG FOR THE TRANSFERRED TAXONOMY TERMS
```

After making it live I have some issues to correct. Mainly the problem is the CSRData field which means Surveys and Data Collection vs. Consulting services. For some reason the field did not map properly and is now in error.

Fatal error again
`Fatal error: Call to a member function getConfig() on null in /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/modules/migrate_plus/src/Plugin/migrate/process/EntityLookup.php on line 191`

```
field_project_type‎:
  plugin: entity_generate
  entity_type: taxonomy_term
  source: project_type
```

After typing that same information in, I got the migration to success. THEY AREN'T THE SAME! In the top one there is a U+200E mark before the colon. That is a Left to Right mark or cairage return! WHAT THE FUCK
```
field_project_type:
  plugin: entity_generate
  entity_type: taxonomy_term
  source: project_type
```

## Support Site for Cooper Center

I have a bunch of projects that are all over the place. Next big one is the support.cooperceter site with a trello ticketing system. I'll build one for myself and then create one for everybody else. Smaller projects if I get bored...

1. Get LOST data out of the database in CSV format and then use migration to import it back into the site
2. Import data from CSV on the web side
3. LEAD/SEI landing page
4. Google SEO

So this SUPPORT site needs SSO access, a ticketing system, and training materials. This project could take all the way until september to make for real. First step is to make the blank site. I'll use the current Sorensen site as a template because I want to be able to use Groups.

1. Add `support.dev1.coopercenter.org` to the domains on Acquia Cloud. You can add the other ones too for Stage and Prod.
2. Use Backup Migrate to copy the Sorensen Site
3. Launch the site to Dev to make sure it works.
4. Make a decent looking homepage with far less content
5. Delete all content programmatically
6. Delete all the content types too


### Trying to delete all content types

Run arbitrary php in the drupal devel interface. It says Execute PHP.
```
$nids = \Drupal::entityQuery('node')->condition('type','person')->execute();
$nodes =  \Drupal\node\Entity\Node::loadMultiple($nids);
foreach ($nodes as $node){
  $node->delete();
}
````

## Trello Webform Integration

I want to build a plugin/powerup that allows for a Drupal Webform to add cards to my Trello Baords for the website work. Ideally people would add the card directly to the board but people aren't always willing to use a new tool.

I'm playing around with the developer sandbox.
https://developers.trello.com/page/sandbox/

Here is the javascript that posts a new card to my Incoming Request Board.
```
// Set the destination list for the new card
var destinationList = "5ab160ed2e906a4f06871e9b";

var success = function(successMsg) {
  asyncOutput(successMsg);
};

var error = function(errorMsg) {
  asyncOutput(errorMsg);
};

var newCard =
  {name: "I just created a new card!",
  desc: "Using the Trello API is fun and easy!",
  pos: "top",
  due: null,
  idList: destinationList
  };

Trello.post('/cards/', newCard, success, error);
```

Getting the label ID's using the api.

https://api.trello.com/1/boards/vmMUiJkb/?labels=all&label_fields=all&fields=id
```
{
"id": "5ab15d365cf1b99537d2c0a3",
"labels": [
{
"id": "5ab1692e11eda5e4dd4f6c23",
"idBoard": "5ab15d365cf1b99537d2c0a3",
"name": "Support Site",
"color": null,
"uses": 2
},
{
"id": "5ab15d36841642c2a8da3f5c",
"idBoard": "5ab15d365cf1b99537d2c0a3",
"name": "CEPS Site",
"color": "orange",
"uses": 1
},
{
"id": "5ab15d36841642c2a8da3f5d",
"idBoard": "5ab15d365cf1b99537d2c0a3",
"name": "Main Cooper Center Site",
"color": "green",
"uses": 1
},
{
"id": "5ab15d36841642c2a8da3f5e",
"idBoard": "5ab15d365cf1b99537d2c0a3",
"name": "SEI/LEAD Sites",
"color": "yellow",
"uses": 1
},
{
"id": "5ab15d36841642c2a8da3f65",
"idBoard": "5ab15d365cf1b99537d2c0a3",
"name": "Certification Site",
"color": "purple",
"uses": 1
},
{
"id": "5ab15d36841642c2a8da3f66",
"idBoard": "5ab15d365cf1b99537d2c0a3",
"name": "Demographics Site",
"color": "blue",
"uses": 1
},
{
"id": "5ab15eaa2808419cc7edd0e9",
"idBoard": "5ab15d365cf1b99537d2c0a3",
"name": "VIG Site",
"color": "sky",
"uses": 1
},
{
"id": "5ab15ec14b8e8a87d266d7dd",
"idBoard": "5ab15d365cf1b99537d2c0a3",
"name": "Sorensen Site",
"color": "lime",
"uses": 1
},
{
"id": "5ab15ed1dce18a4276d200c3",
"idBoard": "5ab15d365cf1b99537d2c0a3",
"name": "VDOT Site",
"color": "pink",
"uses": 1
},
{
"id": "5ab15d36841642c2a8da3f62",
"idBoard": "5ab15d365cf1b99537d2c0a3",
"name": "CSR Site",
"color": "red",
"uses": 0
}
]
}
```

Creating the Card with a list specified. Use the above ids to specify which site labels to use.
```
// Set the destination list for the new card
var destinationList = "5ab160ed2e906a4f06871e9b";
var labels = "5ab1692e11eda5e4dd4f6c23";

var success = function(successMsg) {
  asyncOutput(successMsg);
};

var error = function(errorMsg) {
  asyncOutput(errorMsg);
};

var newCard =
  {name: "I just created a new card!",
  desc: "Using the Trello API is fun and easy!",
  pos: "top",
  due: null,
  idList: destinationList,
  idLabels: labels
  };

Trello.post('/cards/', newCard, success, error);
```


## Making a flexbox grid of website cards

I need to make a flexbox grid of website cards. I want them to display the name of the site above an image of something related to the site.


## Interactive maps Stephen

What python version are you running to get your simple server up. python3 didn't like it.

```
<link href="/sites/demographics/files/va_maps_minimal_test/css/interactive-map.css" rel="stylesheet" title="Interactive Maps Stylesheet">
<script src="/sites/demographics/files/va_maps_minimal_test/js/d3.min.js"></script>
<script src="/sites/demographics/files/va_maps_minimal_test/js/topojson.min.js"></script>
<script src="/sites/demographics/files/va_maps_minimal_test/js/wcc.maps.js"></script>


<div id="map-01" class="interactive-map-target"></div>

<script>
usMapParams = {
  target: "map-01",
  area: "US",
  topography: "states",
  title: "United States Population",
  subtitle: "Estimates & Projections",
  data: {
    file: "2016-11-13-us-estimates-projections.csv",
    geo: {
      idColumn: "fips",
      nameColumn: "name"
    },
    variables: [{
        column: "pop2010",
        label: "2010 Estimate"
      },
      {
        column: "pop2020",
        label: "2020 Projection"
      },
      {
        column: "pop2030",
        label: "2030 Projection"
      },
      {
        column: "pop2040",
        label: "2040 Projection"
      }
    ],
    legend: {
      title: "Population",
      limits: [0, 10000000],
      colors: [{
          red: 255,
          green: 255,
          blue: 255
        },
        {
          red: 229,
          green: 114,
          blue: 0
        }
      ],
      category: "quantitative"
    }
  }
}

interactiveMap(usMapParams);
</script>
```

[Link to the current progress](http://demographics.dd:8083/node/7451)

We should maybe make the overflow visible so the map continuese to show up.

.interactive-map-box svg
overflow: visible;

## Getting Shonel iframes to display properly

```
<style>.embed-container {position: relative; padding-bottom: 67%; height: 0; max-width: 100%;} .embed-container iframe, .embed-container object, .embed-container iframe{position: absolute; top: 0; left: 0; width: 100%; height: 100%;} small{position: absolute; z-index: 40; bottom: 0; margin-bottom: -15px;}</style><div class="embed-container"><small><a href="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=d3b3eadb06214567a6a7bce83d12c26f&amp;extent=-81.6122,35.9981,-77.2289,39.6756&home=true&zoom=true&scale=true&disable_scroll=true&theme=light" style="color:#0000FF;text-align:left" target="_blank">View larger map</a></small><br><iframe width="300" height="200" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="Breast_Website" src="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=d3b3eadb06214567a6a7bce83d12c26f&amp;extent=-81.6122,35.9981,-80.2289,39.6756&home=true&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light"></iframe></div>


&extent=-81.6122,35.9981,-76.2289,39.6756

extent=-81.6122,35.9981,-77.2289,39.6756
gives me the 60 mile on the argis site and 100 on the embed

extent=-81.6122,35.9981,-80.2289,39.6756
gives me 20mi on the arcgis site

------


<style>.embed-container {position: relative; padding-bottom: 67%; height: 0; max-width: 100%;} .embed-container iframe, .embed-container object, .embed-container iframe{position: absolute; top: 0; left: 0; width: 100%; height: 100%;} small{position: absolute; z-index: 40; bottom: 0; margin-bottom: -15px;}</style><div class="embed-container"><small><a href="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=65bc1890f1b740419372cb39d9a872d1&amp;extent=-84.9493,33.9731,-74.1827,41.3377&home=true&zoom=true&scale=true&disable_scroll=true&theme=light" style="color:#0000FF;text-align:left" target="_blank">View larger map</a></small><br><iframe width="300" height="200" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="Lung_Website" src="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=65bc1890f1b740419372cb39d9a872d1&amp;extent=-84.9493,33.9731,-74.1827,41.3377&home=true&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light"></iframe></div>


<style>.embed-container {position: relative; padding-bottom: 67%; height: 0; max-width: 100%;} .embed-container iframe, .embed-container object, .embed-container iframe{position: absolute; top: 0; left: 0; width: 100%; height: 100%;} small{position: absolute; z-index: 40; bottom: 0; margin-bottom: -15px;}</style><div class="embed-container"><small><a href="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=003b1aea35514a55bfc855e4b311e182&amp;extent=-85.0153,33.8956,-74.2486,41.2676&home=true&zoom=true&scale=true&disable_scroll=true&theme=light" style="color:#0000FF;text-align:left" target="_blank">View larger map</a></small><br><iframe width="300" height="200" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="Prostate_Website" src="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=003b1aea35514a55bfc855e4b311e182&amp;extent=-85.0153,33.8956,-74.2486,41.2676&home=true&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light"></iframe></div>


<style>.embed-container {position: relative; padding-bottom: 67%; height: 0; max-width: 100%;} .embed-container iframe, .embed-container object, .embed-container iframe{position: absolute; top: 0; left: 0; width: 100%; height: 100%;} small{position: absolute; z-index: 40; bottom: 0; margin-bottom: -15px;}</style><div class="embed-container"><small><a href="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=3b9a86a66cc44156a3cd3df1c53f4b46&amp;extent=-84.9521,33.9184,-74.1854,41.2882&home=true&zoom=true&scale=true&disable_scroll=true&theme=light" style="color:#0000FF;text-align:left" target="_blank">View larger map</a></small><br><iframe width="300" height="200" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" title="All Sites_Website"

<a href="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=3b9a86a66cc44156a3cd3df1c53f4b46&amp;extent=-84.9521,33.9184,-74.1854,41.2882&home=true&zoom=true&scale=true&disable_scroll=true&theme=light" style="color:#0000FF;text-align:left" target="_blank">View larger map</a> src="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=3b9a86a66cc44156a3cd3df1c53f4b46&amp;extent=-84.9521,33.9184,-74.1854,41.2882&home=true&zoom=true&previewImage=false&scale=true&disable_scroll=true&theme=light"></iframe></div>
```

There is the embed code. I want to test it all out and make sure it works on mobile screens correctly. So I really just want the links to the argis maps. I don't need to edit the current iframes because I'm going to hide them on mobile.

extent=-81.6122,35.9981,-77.2289,39.6756

Here are the working links for what to show on mobile screens. It would be nice for them to also have pictures of the maps above them.
```
<img class="show-only-under-500" src="/sites/demographics/files/breast-cancer.png" href="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=d3b3eadb06214567a6a7bce83d12c26f&amp;extent=-81.6122,35.9981,-77.2289,39.6756&home=true&zoom=true&scale=true&disable_scroll=true&theme=light">
<span class="bbb show-only-under-500"><a href="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=d3b3eadb06214567a6a7bce83d12c26f&amp;extent=-81.6122,35.9981,-77.2289,39.6756&home=true&zoom=true&scale=true&disable_scroll=true&theme=light">View Breast Cancer map</a></span>
<span class="bbb show-only-under-500"><a href="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=65bc1890f1b740419372cb39d9a872d1&amp;extent=-81.6122,35.9981,-77.2289,39.6756&home=true&zoom=true&scale=true&disable_scroll=true&theme=light">View Lung Cancer map</a></span>
<span class="bbb show-only-under-500"><a href="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=003b1aea35514a55bfc855e4b311e182&amp;extent=-81.6122,35.9981,-77.2289,39.6756&home=true&zoom=true&scale=true&disable_scroll=true&theme=light">View Prostate Cancer map</a></span>
<span class="bbb show-only-under-500"><a href="//uvalibrary.maps.arcgis.com/apps/Embed/index.html?webmap=3b9a86a66cc44156a3cd3df1c53f4b46&amp;extent=-81.6122,35.9981,-77.2289,39.6756&home=true&zoom=true&scale=true&disable_scroll=true&theme=light">View map of All Cancer</a></span>
```

## Exporting to CSV file

So I want to export all of the CEPS LOST data to a csv file so that I can possibly re-import it later and get rid of all of the extra content types that are attached to it. There are 30,686 nodes. That's over 30000 data points to deal with. I can't get all of that data into one CSV file. This is not possible in one go. I was figuring it was a lot fewer data-points than that.

## Importing CSV to site

The export is not as useful so I'm going to work on importing a single month worth through an admin interface instead. The first piece I needed was the routing for this module. Instead of creating a new module, I am using the lost_to_csv module and just adding an additional [route to the .routing.yml file](https://www.drupal.org/docs/8/api/routing-system/structure-of-routes). The other really important piece is the return type of the controller I specified in routing. The controller returns a reder array which is a Drupal representation of the HTML that will display to the user. I want a form to display with a single Upload CSV file form element.

```
use \Drupal\node\Entity\Node;
$month = 3;
$year = 857;
$locality = 'Loudoun County';
$tax = 857;
$node = Node::create([
    'type'        => 'lost',
    'title'       => 'LOST-' . $month . '-' . $year,
    'field_lost_locality' => 857,
    'field_lost_month' => $month,
    'field_lost_tax' => $tax,
    'field_lost_year' => $year,
]);
$node->save();
```

You have to specify the exact term id for locality since it is an entity reference. So use the string to get the tid.

```
$term_name = 'Loudoun County';
$term = \Drupal::entityTypeManager()
      ->getStorage('taxonomy_term')
      ->loadByProperties(['name' => $term_name,
                          'vid' => 'local_option_sales_tax_localitie']);
$keys = array_keys($term);
var_dump( $keys);
echo 'Here is the tid ' . $keys[0];
```

This test code now works.
```
create_new_lost_node(55, 56, 'Loudoun County', 66.66);
```

So now I need to pass a csv file through a form and process it for the values this create_new_lost_node function needs. [Here is a good tutorial on how to abstract this taxonomy term fetching function so you can use it with any vocabulary.](https://www.btmash.com/article/2016-04-26/saving-and-retrieving-taxonomy-terms-programmatically-drupal-8)

I want to take a short cut and just process the data as a regular text entry. This way I don't have to deal with the uploading of a csv file yet.
I've been looking forever for a list of example code snippets. Finally found them through Drupalize.me. [Code tutorials](https://www.drupal.org/project/examples/releases/8.x-1.x-dev)

Sanitizing inputs with a regular expression seems like an easy option. It's more restrictive than checking for html or mysql.

```
([0-9]){1,2},([0-9])*.([0-9.])*,([A-Za-z ])+
```

https://regexr.com/

Now I just need to figure out how to filter Regex with php on the form validation step. [The preg_match seems to be a good option.](http://php.net/manual/en/function.preg-match.php)


## Python distraction

So I wanted a simple way to get all of the image paths so I output them using python.I've gone down the rabbit hole of new tools and python integration.

Tool name - autocomplete-python
Kite is a tool for autocomplete of text.
https://kite.com/blog/faq-autocomplete-python?source=autocomplete-python

There is a how to tool for the Kite plugin. https://help.kite.com/category/43-atom-integration

It looks like Kite costs money eventually so I may need to turn it off in 30 days.

Tool name atom-python-run
Use F5 or F6 to just run the python on your screen. No more terminal needing to be open.

Tool name python-tools
It allows refactoring and goto definition.

I'm looking for a syntax checker.

Tool name python-indent
Handles the indentation automatically

There is a full ide that has a syntax checker but it requires some actual installation of Python Language Server. No more tools.
https://atom.io/packages/ide-python

## VA Politics page

So here are a bunch of images for the politics page.

```
<div id="politics-wrapper">

<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/538-logo-fivethirtyeight.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/bloomberg.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/cnn.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/cookpoliticalreport.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/cooper-center.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/crystal-ball.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/dem-caucus.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/demographics-CED.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/fox.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/fredricksburg.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/Governors-Office.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/insidenova.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/london-times-mirror.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/msnbc-logo-card-twitter.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/news-advance.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/news-bristol.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/news-daily-press.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/news-daily-record.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/news-progress.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/NewYorkTimes.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/NSNClogo.jpg'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/Politico.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/PollingReport.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/RealClearPolitics.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/republican-party-of-va-2.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/richmond-free-press.jpeg'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/richmond-sunlight.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/richmond-times-dispatch-logo-feat.jpg'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/thehill-logo-big.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/va-democrats.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/va-repub-caucus.jpg'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/va-young-democrats.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/VA21.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/Virginia-department-of-elections.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/virginia-pilot.jpg'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/virginiageneralassembly.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/WashingtonPost.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/wason-center.png'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/wsj.jpeg'/></a>
<a class='politics-link' href='/' ><img class='grow' src='sites/sorensen/files/va_politics_page/young-republican-federation-of-va.png'/></a>


</div>
```

<<<<<<< HEAD

# Using Pug / Jade

Use phpStorm and create a new project. [Tutorial](https://www.jetbrains.com/help/phpstorm/pug-jade-template-engine.html)

Node.js.Express project type
Create a Pug file > File > New > Jade file
Create a file watcher

Pug Jade File Watcher Setup on WINDOWS
[Tutoriall](https://intellij-support.jetbrains.com/hc/en-us/community/posts/115000131524-File-Watcher-transpiler-for-pugJs)

npm install pug-cli -g
Make Pug Filewatcher with program set to `%YOUR_HOME%\AppData\Roaming\npm\pug.cmd`

## Smooth Scroll Anchor links

https://codepen.io/jooleearr/pen/gpooKj

```javascript
/*
	Smooth scroll functionality for anchor links (animates the scroll
	rather than a sudden jump in the page)
*/
$('.js-anchor-link').click(function(e){
  e.preventDefault();
  var target = $($(this).attr('href'));
  if(target.length){
    var scrollTo = target.offset().top;
    $('body, html').animate({scrollTop: scrollTo+'px'}, 800);
  }
});
```

```html
<ul id="nav">
  <li><a href="#section-1" class="js-anchor-link">Section 1</a></li>
  <li><a href="#section-2" class="js-anchor-link">Section 2</a></li>
  <li><a href="#section-3" class="js-anchor-link">Section 3</a></li>
</ul>

<div id="section-1" class="section">
  <h1>Section 1</h1>
  <a href="#section-2" class="js-anchor-link">Go to section 2</a>
</div>
```
=======
State Government
```
<div class="politics-wrapper">
<a class='politics-link' href='https://governor.virginia.gov/' ><img class='grow' src='sites/sorensen/files/va_politics_page/Governors-Office.png'/></a>
<a class='politics-link' href='https://virginiageneralassembly.gov/' ><img class='grow' src='sites/sorensen/files/va_politics_page/virginiageneralassembly.png'/></a>
<a class='politics-link' href='https://www.elections.virginia.gov/' ><img class='grow' src='sites/sorensen/files/va_politics_page/Virginia-department-of-elections.png'/></a>
</div>
```

Party Sites
```
<div class="politics-wrapper">
<a class='politics-link' href='http://virginia.gop/' ><img class='grow' src='sites/sorensen/files/va_politics_page/republican-party-of-va-2.png'/></a>
<a class='politics-link' href='https://vademocrats.org/' ><img class='grow' src='sites/sorensen/files/va_politics_page/va-democrats.png'/></a>
<a class='politics-link' href='https://www.dems.gov/' ><img class='grow' src='sites/sorensen/files/va_politics_page/dem-caucus.png'/></a>
<a class='politics-link' href='https://www.senators4va.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/va-repub-caucus.jpg'/></a>
</div>

```

Organizations for Young People
```
<div class="politics-wrapper">
<a class='politics-link' href='http://www.vayd.org/' ><img class='grow' src='sites/sorensen/files/va_politics_page/va-young-democrats.png'/></a>
<a class='politics-link' href='https://www.virginia21.org/' ><img class='grow' src='sites/sorensen/files/va_politics_page/VA21.png'/></a>
<a class='politics-link' href='https://yrfv.gop/' ><img class='grow' src='sites/sorensen/files/va_politics_page/young-republican-federation-of-va.png'/></a>
</div>
```


State & Local News
```
<div class="politics-wrapper">
<a class='politics-link' href='https://www.loudountimes.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/london-times-mirror.png'/></a>
<a class='politics-link' href='http://www.newsadvance.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/news-advance.png'/></a>
<a class='politics-link' href='http://www.dailypress.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/news-daily-press.png'/></a>
<a class='politics-link' href='http://www.fredericksburg.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/fredricksburg.png'/></a>
<a class='politics-link' href='http://www.insidenova.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/insidenova.png'/></a>
<a class='politics-link' href='http://www.heraldcourier.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/news-bristol.png'/></a>
<a class='politics-link' href='http://www.dnronline.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/news-daily-record.png'/></a>
<a class='politics-link' href='http://www.dailyprogress.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/news-progress.png'/></a>
<a class='politics-link' href='https://www.richmondsunlight.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/richmond-sunlight.png'/></a>
<a class='politics-link' href='http://www.richmond.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/richmond-times-dispatch-logo-feat.jpg'/></a>
<a class='politics-link' href='http://richmondfreepress.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/richmond-free-press.jpeg'/></a>
<a class='politics-link' href='https://pilotonline.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/virginia-pilot.jpg'/></a>
</div>
```


National news

```
<div class="politics-wrapper">
<a class='politics-link' href='https://www.nytimes.com/section/politics' ><img class='grow' src='sites/sorensen/files/va_politics_page/NewYorkTimes.png'/></a>
<a class='politics-link' href='http://www.columnists.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/NSNClogo.jpg'/></a>
<a class='politics-link' href='https://www.wsj.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/wsj.jpeg'/></a>
<a class='politics-link' href='https://fivethirtyeight.com/politics/' ><img class='grow' src='sites/sorensen/files/va_politics_page/538-logo-fivethirtyeight.png'/></a>
<a class='politics-link' href='https://cookpolitical.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/cookpoliticalreport.png'/></a>
<a class='politics-link' href='https://www.bloomberg.com/politics' ><img class='grow' src='sites/sorensen/files/va_politics_page/bloomberg.png'/></a>
<a class='politics-link' href='https://www.realclearpolitics.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/RealClearPolitics.png'/></a>
<a class='politics-link' href='http://www.msnbc.com/place-for-politics' ><img class='grow' src='sites/sorensen/files/va_politics_page/msnbc-logo-card-twitter.png'/></a>
<a class='politics-link' href='https://www.washingtonpost.com/politics' ><img class='grow' src='sites/sorensen/files/va_politics_page/WashingtonPost.png'/></a>
<a class='politics-link' href='https://www.cnn.com/politics' ><img class='grow' src='sites/sorensen/files/va_politics_page/cnn.png'/></a>
<a class='politics-link' href='https://www.politico.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/Politico.png'/></a>
<a class='politics-link' href='http://www.foxnews.com/politics.html' ><img class='grow' src='sites/sorensen/files/va_politics_page/fox.png'/></a>
<a class='politics-link' href='http://thehill.com/' ><img class='grow' src='sites/sorensen/files/va_politics_page/thehill-logo-big.png'/></a>



</div>
```


Research & Demographics
```
<div class="politics-wrapper">
<a class='politics-link' href='http://www.pollingreport.com/index.html' ><img class='grow' src='sites/sorensen/files/va_politics_page/PollingReport.png'/></a>
<a class='politics-link' href='http://wasoncenter.cnu.edu/' ><img class='grow' src='sites/sorensen/files/va_politics_page/wason-center.png'/></a>
<a class='politics-link' href='http://www.centerforpolitics.org/crystalball/' ><img class='grow' src='sites/sorensen/files/va_politics_page/crystal-ball.png'/></a>
<a class='politics-link' href='http://ced.uab.es/en/' ><img class='grow' src='sites/sorensen/files/va_politics_page/demographics-CED.png'/></a>
<a class='politics-link' href='https://cooperceter.org' ><img class='grow' src='sites/sorensen/files/va_politics_page/cooper-center.png'/></a>
<a class='politics-link' href='https://csr.cooperceter.org' ><img class='grow' src='sites/sorensen/files/va_politics_page/cooper-center.png'/></a>
<a class='politics-link' href='http://statchatva.org/' ><img class='grow' src='sites/sorensen/files/va_politics_page/cooper-center.png'/></a>
</div>
```

So I have two last goals for this politics page. I need to edit the Governors' images so they are unique and I need to make the jump links.

[Codepen with great example](https://codepen.io/jooleearr/pen/gpooKj)
```
<ul id="jump-nav">
  <li><a href="#section-1" class="js-anchor-link">Research & Demographics</a></li>
  <li><a href="#section-2" class="js-anchor-link">State & Local News</a></li>
  <li><a href="#section-3" class="js-anchor-link">National News</a></li>
  <li><a href="#section-4" class="js-anchor-link">Organizations for Young People</a></li>
  <li><a href="#section-5" class="js-anchor-link">Party Sites</a></li>
  <li><a href="#section-6" class="js-anchor-link">State Government</a></li>
</ul>
```

## Test out how you add a custom field to a card in trello

I want to create two custom fields fields for my trello cards. A date created and a date completed field. I also need to create a email field that is autopopulated by the Drupal account email.

I'm realizing that creating this application as a client side app will make this board vulnerable.

key - KEY
token - TOKEN
board id - 5ad7d8b0af86ba9895891ab7
New Requests List Id - 5ad7da0dab91022ea25796da

Here is the script that adds a global Trello object to make calls on.
<script src="https://api.trello.com/1/client.js?key=6617bebb8d1e9ddd8ab682977cf8d6a2"></script>

```
var data = null;

var xhr = new XMLHttpRequest();

xhr.addEventListener("readystatechange", function () {
  if (this.readyState === this.DONE) {
    console.log(this.responseText);
  }
});

xhr.open("POST", "https://api.trello.com/1/cards?name=New%20Card&desc=Please%20Fix%20My%20Computer&pos=top&idList=5ad7da0dab91022ea25796da&urlSource=https%3A%2F%2Fsupport.coopercenter.org%2Ftickets&keepFromSource=all&key={YOUR-API-KEY}&token={AN-OAUTH-TOKEN}");

xhr.send(data);
```

https://api.trello.com/1/cards?name=New%20Card&desc=Please%20Fix%20My%20Computer&pos=top&idList=5ad7da0dab91022ea25796da&urlSource=https%3A%2F%2Fsupport.coopercenter.org%2Ftickets&keepFromSource=all&key=KEY&token=TOKEN

So the issue I am running into is that making this a client side app leaves the trello boards vulnerable to attack since the API ket and token would be exposed. If I make the HTTP Requests from the server through PHP then the API key is protected. Unfortunatley that means I'd need to use PHP to send the data to Trello and I am not nearly as clear on how to do that.

It looks like the httpClient() method is my solution to sending values through cURL - https://www.drupal.org/project/filefield_sources/issues/2840594

```
$client = \Drupal::httpClient();
try {
  $request = $client->get($url);
  $status = $request->getStatusCode();
  $file_contents = $request->getBody()->getContents();
}
catch (RequestException $e) {
  //An error happened.
}
```

This PHP code works to submit a new card!!!!!!!
```
  $client = \Drupal::httpClient();
  $request = $client->post('https://api.trello.com/1/cards?name=New%20Card&desc=Please%20Fix%20My%20Computer&pos=top&idList=5ad7da0dab91022ea25796da&urlSource=https%3A%2F%2Fsupport.coopercenter.org%2Ftickets&keepFromSource=all&key=KEY&token=TOKEN');
  $response = json_decode($request->getBody());
```

My Key - KEY
Token - TOKEN


Here is the response
```
object(stdClass)[588]
  public 'id' => string '5ada2198a08f24cf053e4d4e' (length=24)
  public 'badges' =>
    object(stdClass)[586]
      public 'votes' => int 0
      public 'attachmentsByType' =>
        object(stdClass)[559]
          public 'trello' =>
            object(stdClass)[582]
              ...
      public 'viewingMemberVoted' => boolean false
      public 'subscribed' => boolean false
      public 'fogbugz' => string '' (length=0)
      public 'checkItems' => int 0
      public 'checkItemsChecked' => int 0
      public 'comments' => int 0
      public 'attachments' => int 1
      public 'description' => boolean true
      public 'due' => null
      public 'dueComplete' => boolean false
  public 'checkItemStates' =>
    array (size=0)
      empty
  public 'closed' => boolean false
  public 'dueComplete' => boolean false
  public 'dateLastActivity' => string '2018-04-20T17:21:28.841Z' (length=24)
  public 'desc' => string 'Please Fix My Computer' (length=22)
  public 'descData' =>
    object(stdClass)[561]
      public 'emoji' =>
        object(stdClass)[560]
  public 'due' => null
  public 'email' => null
  public 'idBoard' => string '5ad7d8b0af86ba9895891ab7' (length=24)
  public 'idChecklists' =>
    array (size=0)
      empty
  public 'idList' => string '5ad7da0dab91022ea25796da' (length=24)
  public 'idMembers' =>
    array (size=0)
      empty
  public 'idMembersVoted' =>
    array (size=0)
      empty
  public 'idShort' => int 9
  public 'idAttachmentCover' => null
  public 'labels' =>
    array (size=0)
      empty
  public 'idLabels' =>
    array (size=0)
      empty
  public 'manualCoverAttachment' => boolean false
  public 'name' => string 'New CardComp' (length=12)
  public 'pos' => int 2048
  public 'shortLink' => string 'NOCZSZGr' (length=8)
  public 'shortUrl' => string 'https://trello.com/c/NOCZSZGr' (length=29)
  public 'subscribed' => boolean false
  public 'stickers' =>
    array (size=0)
      empty
  public 'url' => string 'https://trello.com/c/NOCZSZGr/9-new-cardcomp' (length=44)
  public 'limits' =>
    object(stdClass)[288]
  ```

  Getting the custom fields and their definitions for our board.
  Board ID - 5ad7d8b0af86ba9895891ab7
  https://api.trello.com/1/board/5ad7d8b0af86ba9895891ab7?key=KEY&token=TOKEN
  Card ID - 5ada2198a08f24cf053e4d4e

  My Key - KEY
  Token - TOKEN
  https://api.trello.com/1/board/5ad7d8b0af86ba9895891ab7/customFields?key=KEY&token=TOKEN



Using this kind of a request I am able to get all of the board data I need.
https://api.trello.com/1/boards/5ad7d8b0af86ba9895891ab7/?fields=name&cards=visible&card_fields=name&customFields=true&card_customFieldItems=true&key=KEY&token=TOKEN

5ada31dade941ce827bd1305 - Customer Email
5ada31cc8cc9574fa096bce8 - Customer Name
5ad7da91b2aeb0f0ceebe691 - Date Created
5ad7da9e1ded184355867d28 - Date Completed



https://api.trello.com/1/board/5ad7d8b0af86ba9895891ab7/customFields?key=KEY&token=TOKEN

  ```
  $request_data = 'https://api.trello.com/1/boards/5ad7d8b0af86ba9895891ab7/customFields&key=KEY&token=TOKEN';
$client = \Drupal::httpClient();
$request = $client->get($request_data);
$response = json_decode($request->getBody());
var_dump($response);
```


```
[
{
"id": "5ad7da91b2aeb0f0ceebe691",
"idModel": "5ad7d8b0af86ba9895891ab7",
"modelType": "board",
"fieldGroup": "4cbcd5f64f44c20674adfd97f4bf4bce5abbbec2b323d5ed9820010f3f7c55ec",
"name": "Date Created",
"pos": 16384,
"type": "date"
},
{
"id": "5ad7da9e1ded184355867d28",
"idModel": "5ad7d8b0af86ba9895891ab7",
"modelType": "board",
"fieldGroup": "f6065514bd878639c3b7073703f9fc2373c2b2b2b43c1f43a56d9c71b16fe8f4",
"name": "Date Completed",
"pos": 32768,
"type": "date"
},
{
"id": "5ada31cc8cc9574fa096bce8",
"idModel": "5ad7d8b0af86ba9895891ab7",
"modelType": "board",
"fieldGroup": "c5aa7ca545628b7ae6afe628eead70fa5f284e6e8cfeddd8ddb6bc076af5ae71",
"name": "Customer Name",
"pos": 49152,
"type": "text"
},
{
"id": "5ada31dade941ce827bd1305",
"idModel": "5ad7d8b0af86ba9895891ab7",
"modelType": "board",
"fieldGroup": "3bcbc0b9543931242a567fa85d9b00b16840469be8c7e8eaa80131f66fa7c14a",
"name": "Customer Email",
"pos": 65536,
"type": "text"
}
]
```

Drupalize Me Example of how to add data to a request
```
$client = \Drupal::httpClient();
$request = $client->get('https://api.github.com/user', [
  'auth' => ['username','password']
]);
$response = $request->getBody();
```


```
$client = \Drupal::httpClient();
$request = $client->put('https://api.trello.com/1/card/5adf9669d4bdf0a0d1adfaeb/customField/5ada31dade941ce827bd1305/item', 'json' => [
  "key" => 'KEY',
  "token" => 'TOKEN',
  "value" => ["text", "Hello, world!"]
]);
$response = $request->getBody();
```

https://api.trello.com/1/card/{card ID}/customField/{Custom Field ID}/item



"idValue": "5a6a23abf958725e1ac86c22",
"key": "",
"token": ""

{
  "value" => ["text": "Hello, world!"]
}

https://api.trello.com/1/card/5ad7d8b0af86ba9895891ab7/customField/%7BCustom%20Field%20ID%7D/item

https://api.trello.com/1/card/5ad7d8b0af86ba9895891ab7?customFieldItems=true&key={APIKey}&token={APIToken}

https://api.trello.com/1/boards/5ad7d8b0af86ba9895891ab7?fields=name&customFieldItems=true&key={APIKey}&token={APIToken}
https://api.trello.com/1/boards/5ad7d8b0af86ba9895891ab7/cards/?fields=name&customFieldItems=true&key={APIKey}&token={APIToken}




## Getting my Hyper sudo passwords to match

https://askubuntu.com/questions/772050/reset-the-password-in-linux-bash-in-windows

I have forgotten my bash on windows password and needed to reset it. The second answer solved the problem.

## Javascript ESLint

[Tutorial](https://www.jetbrains.com/help/webstorm/eslint.html) Linting is running a program to check for possible errors. I need to set up linting on my work computer. It is installed here `/usr/local/bin/eslint -> /usr/local/lib/node_modules/eslint/bin/eslint.js`.

I'm also installing the JavaScript Standard style. I set the version of JS I'm using to Javascript 1.8.5

## Convert SASS to SCSS
```
sass-convert -F scss -T sass style.scss style.sass
```


## Making a Satisfaction Survey page

\Drupal\trello_support_form\TicketAnalyzer::run_survey_generator();

\Drupal\trello_support_form\TicketAnalyzer::get_all_ticket_nodes_by_current_user();

\Drupal\trello_support_form\SurveyResults::get_all_survey_nodes();

## Headshot updates

https://coopercenter.org/sites/cooper/files/larry_head.png
https://www.linkedin.com/in/larry-terry-0bb24529/

Larry Terry Slide goes at the topic

```HTML
<div class="ms-slide"><img alt="lorem ipsum dolor sit" data-src="https://coopercenter.org/sites/cooper/files/larry_head.png" src="/masterslider/style/blank.gif" />
<div class="ms-info">
<h3>Larry D. Terry II</h3>

<h4>Executive Director</h4>

<p class="email">E-Mail: <a href="mailto:larry.terry@virginia.edu">larry.terry@virginia.edu</a></p>

<p>Larry Terry comes to the Cooper Center in 2018 from Texas, where he worked to improve the lives of citizens in the Dallas region and beyond, creating practical partnerships with elected officials, public servants and community leaders to address poverty and other community issues, including launching the Community Leadership Academy, the nation’s first peer-based citizen police officer leadership training program. His passion is research-based, outcome-driven programs and services that advance the priorities of the University of Virginia in serving the Commonwealth, forming lasting partnerships with citizens, and building vibrant, connected communities. Terry’s research, publications, teaching, and educational achievements focus on leading and managing public organizations, housing reform, and community engagement and public trust. Prior to his position at UNT Dallas, Terry served as an assistant professor of Public Administration at both Long Island University-Brooklyn and Arizona State University.</p>

<ul class="ms-socials ">
	<li class="ms-ico-fb link"><a href="https://www.linkedin.com/in/larry-terry-0bb24529/">linkedin</a></li>
	<!-- <li class='ms-ico-tw gs'><a href='https://scholar.google.com/citations?user=09W80zgAAAAJ&hl=en&oi=sra'>google</a></li> -->
</ul>
</div>
</div>
```


## PHPUnit Tests

I found some examples for the phpunit tests. I have to run the tests from the core directory. There is a phpunit.xml.dist file that has the settings needed to make the tests work.
```
cd /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core
../vendor/bin/phpunit --group phpunit_example
```
The tests take forever to run but this configuration in the phpunit.xml.dist file seems to work out.
```xml
<?xml version="1.0" encoding="UTF-8"?>

<!-- TODO set checkForUnintentionallyCoveredCode="true" once https://www.drupal.org/node/2626832 is resolved. -->
<!-- PHPUnit expects functional tests to be run with either a privileged user
 or your current system user. See core/tests/README.md and
 https://www.drupal.org/node/2116263 for details.
-->
<phpunit bootstrap="tests/bootstrap.php" colors="true"
         beStrictAboutTestsThatDoNotTestAnything="true"
         beStrictAboutOutputDuringTests="true"
         beStrictAboutChangesToGlobalState="true">
<!-- TODO set printerClass="\Drupal\Tests\Listeners\HtmlOutputPrinter" once
 https://youtrack.jetbrains.com/issue/WI-24808 is resolved. Drupal provides a
 result printer that links to the html output results for functional tests.
 Unfortunately, this breaks the output of PHPStorm's PHPUnit runner. However, if
 using the command line you can add
 - -printer="\Drupal\Tests\Listeners\HtmlOutputPrinter" to use it (note there
 should be no spaces between the hyphens).
-->
  <php>
    <!-- Set error reporting to E_ALL. -->
    <ini name="error_reporting" value="32767"/>
    <!-- Do not limit the amount of memory tests take to run. -->
    <ini name="memory_limit" value="-1"/>
    <!-- Example SIMPLETEST_BASE_URL value: http://localhost -->
    <env name="SIMPLETEST_BASE_URL" value="http://support.dd:8083"/>
    <!-- Example SIMPLETEST_DB value: mysql://username:password@localhost/databasename#table_prefix -->
    <!-- <env name="SIMPLETEST_DB" value="mysql://root@localhost:8083/test"/> -->
    <env name="SIMPLETEST_DB" value="mysql://root@localhost:33067/test"/>
    <!-- 127.0.0.1:33067  -->
    <!-- Example BROWSERTEST_OUTPUT_DIRECTORY value: /path/to/webroot/sites/simpletest/browser_output -->
    <env name="BROWSERTEST_OUTPUT_DIRECTORY" value="/Users/miles/Sites/devdesktop/uvacooper-dev/tests"/>
    <!-- To disable deprecation testing uncomment the next line. -->
    <env name="SYMFONY_DEPRECATIONS_HELPER" value="weak_vendors"/>
    <!-- Example for changing the driver class for mink tests MINK_DRIVER_CLASS value: 'Drupal\FunctionalJavascriptTests\DrupalSelenium2Driver' -->
    <!-- Example for changing the driver args to mink tests MINK_DRIVER_ARGS value: '["http://127.0.0.1:8510"]' -->
    <!-- Example for changing the driver args to phantomjs tests MINK_DRIVER_ARGS_PHANTOMJS value: '["http://127.0.0.1:8510"]' -->
    <!-- Example for changing the driver args to webdriver tests MINK_DRIVER_ARGS_WEBDRIVER value: '["firefox", null, "http://localhost:4444/wd/hub"]' -->
  </php>
  <testsuites>
    <testsuite name="unit">
      <file>./tests/TestSuites/UnitTestSuite.php</file>
    </testsuite>
    <testsuite name="kernel">
      <file>./tests/TestSuites/KernelTestSuite.php</file>
    </testsuite>
    <testsuite name="functional">
      <file>./tests/TestSuites/FunctionalTestSuite.php</file>
    </testsuite>
    <testsuite name="functional-javascript">
      <file>./tests/TestSuites/FunctionalJavascriptTestSuite.php</file>
    </testsuite>
  </testsuites>
  <listeners>
    <listener class="\Drupal\Tests\Listeners\DrupalListener">
    </listener>
    <!-- The Symfony deprecation listener has to come after the Drupal listener -->
    <listener class="Symfony\Bridge\PhpUnit\SymfonyTestsListener">
    </listener>
  </listeners>
  <!-- Filter for coverage reports. -->
  <filter>
    <whitelist>
      <directory>./includes</directory>
      <directory>./lib</directory>
      <directory>./modules</directory>
      <directory>../modules</directory>
      <directory>../sites</directory>
      <!-- By definition test classes have no tests. -->
      <exclude>
        <directory suffix="Test.php">./</directory>
        <directory suffix="TestBase.php">./</directory>
      </exclude>
     </whitelist>
  </filter>
</phpunit>
```

The unit tests take a really long time to run but they do work. With 6 tests it takes 1.31 minutes. Here is my group of tests I am using.

```
../vendor/bin/phpunit --group trello_test
```


## Creating Butler so we don't have to pay for Trello

Churning Board ID - 5967774e86ea1554e62fa8f1

Asynchronous javascript using the .then notation
```js
function markCardComplete(t){
  var card_id = t.getContext()['card'];
  t.board('all').then(function (board){
      return get_completed_field_id_from_baord(board);
  })
  .then(function (field_id){
      return setEndDateToCurrentDate(card_id, field_id);
  });
}

doSomething()
.then(result => doSomethingElse(result))
.then(newResult => doThirdThing(newResult))
.then(finalResult => {
  console.log(`Got the final result: ${finalResult}`);
})
.catch(failureCallback);
```
Now rewritten in the cleaner style:
```js
function markCardComplete(t){
  var card_id = t.getContext()['card'];
  t.board('all')
  .then(resulting_board => get_completed_field_id_from_baord(resulting_board))
  .then(field_id => set_end_date_to_current_date(card_id, field_id));
}
```

ID of the list - 5b0704c53424605a40397a8a
Card ID - "5b075186b9029fa7b2244b55"

The working url
https://api.trello.com/1/boards/5ad7d8b0af86ba9895891ab7/?fields=name&list&cards=visible&card_fields=name&customFields=true&card_customFieldItems=true&key=ebc310e38e2e0fe0d33cc0eba8eeb024&token=bcb740e1385d254f27f4c99346788dc13536c86da93a946cf6ecb6234a258608

https://glitch.com/edit/#!/perpetual-polish?path=public/js/client.js:491:47

Working Code with Durations and Date Completed marking
```js
/* global TrelloPowerUp */

var Promise = TrelloPowerUp.Promise;

//                              Completed Button on Cards
////////////////////////////////////////////////////////////////////////////////////////

function mark_card_completed(t){
  var card_id = t.getContext()['card'];
  t.board('all')
    .then(resulting_board => get_completed_field_id_from_baord(resulting_board))
    .then(field_id => set_end_date_to_current_date(card_id, field_id));
}

function get_completed_field_id_from_baord(board){
  for(var i = 0 ; i < board["customFields"].length; i++){
      if(board["customFields"][i].name == "Date Completed"){
        var date_completed_field_id = board["customFields"][i].id;
      }   
    }
  return date_completed_field_id;
}

function set_end_date_to_current_date(card_id, custom_field){
  let cur_date = new Date();
  var url = "https://api.trello.com/1/cards/"+card_id+"/customField/"+custom_field+"/item?";
  url = addAuthToken(url);
  var data = {value: { date: cur_date }};
  fetch(url, { body: JSON.stringify(data), method: 'PUT', headers: {'content-type': 'application/json'}})
  .then((resp) => resp.json())
  // .then((data) => console.log(JSON.stringify(data, null, 2)))
  .catch((err) => console.log(JSON.stringify(err, null, 2)))
}

function addAuthToken(str){
  return str + "&key=ebc310e38e2e0fe0d33cc0eba8eeb024&token=bcb740e1385d254f27f4c99346788dc13536c86da93a946cf6ecb6234a258608";
}
//                              Setting Badge Durations
////////////////////////////////////////////////////////////////////////////////////////////

//Here we set the duration badge and update card end dates using the last 50 actions
var getBadges = function(t){
  return t.card('customFieldItems')
  .then((fields) => find_duration(fields))
  .then(function(duration){
    // console.log('We just loaded the duration: ', duration);
    check_cards_in_done_list_for_end_times(t);
    return [{
      // dynamic badges can have their function rerun after a set number
      // of seconds defined by refresh. Minimum of 10 seconds.
      dynamic: function(){
        // we could also return a Promise that resolves to this as well if we needed to do something async first
        return {
          title: 'Duration', // for detail badges only
          text: duration.str,
          color: get_time_color(duration.number),
          refresh: 10 // in seconds
        };
      }
    }];
  });
};

function find_duration(fields){
 let dates = [];
 for(let i = 0 ; i < fields.customFieldItems.length ; i++){
   if(fields.customFieldItems[i].value.date != undefined){
     dates.push(fields.customFieldItems[i].value.date);
   }
 }
 let d2 = new Date();
 let d1 = new Date();

 if(dates.length > 0){
   d1 = new Date(dates[0]);
   if(dates.length > 1){
     d2 = new Date(dates[1]);  
   }
 }
  let duration = Math.abs(d2 - d1);
  return formatted_duration(duration);
}

function formatted_duration(duration){
  let min = 60000;
  let hour = 3600000;
  let day = 86400000;
  let week = 604800000;

  if(duration < min){
    return {"str" : ms_to_seconds(duration).toFixed(2) + " sec",
            "number" : duration};
  }
  else if(duration < 2*hour){
    return {"str" : ms_to_minutes(duration).toFixed(2) + " min" , "number" : duration};
  }
  else if(duration < 2* day){
    return {"str" : ms_to_hours(duration).toFixed(2) + " hours" , "number" : duration};
  }
  else if(duration < 2* week){
    return {"str" : ms_to_days(duration).toFixed(2) + " days" , "number" : duration};
  }
  else if(duration >= 2* week){
    return {"str" : ms_to_week(duration).toFixed(2) + " weeks" , "number" : duration};
  }
  else{
    return {"str" : "No Duration" , "number" : duration};
  }
}


function ms_to_seconds(duration){
  return duration / 1000;
}

function ms_to_minutes(duration){
  return duration / 1000 / 60;
}

function ms_to_hours(duration){
  return duration / 1000 / 60 / 60;
}

function ms_to_days(duration){
  return duration /1000 /60 / 60 / 24;
}

function ms_to_week(duration){
  return duration /1000 /60 / 60 / 24 / 7;
}

function get_time_color(duration){
  let min = 60000;
  let hour = 3600000;
  let day = 86400000;
  let week = 604800000;

  if(duration < min){
    return "green";
  }
  else if(duration < 2*hour){
    return "yellow";
  }
  else if(duration < 2* day){
    return "orange";
  }
  else if(duration < 2* week){
    return "red";
  }
  else if(duration >= 2* week){
    return "dark_red";
  }
  else{
    return "none";
  }
}

//                              Update Cards Based on Actions
////////////////////////////////////////////////////////////////////////////////////////////

var global_board_id;
var actions_json;
var completed_id = -1;
var complete_board_info = -1;

function check_cards_in_done_list_for_end_times(t){
  // console.log("Here is the t: ", t, t.getContext());
  // debugger;
  let board_id = t.getContext().board;
  if(global_board_id != board_id){
    console.log("Board Id Changed : ",  board_id);
    global_board_id = board_id;
    return scan_actions(board_id) //this gets called a single time since we only need the actions set once.
      .then((actions_json) => update_cards_moved_to_the_done_list(actions_json));
  }
}

function scan_actions(board_id){
  let url = "https://api.trello.com/1/boards/"
    + board_id + "/actions?key=ebc310e38e2e0fe0d33cc0eba8eeb024&token=bcb740e1385d254f27f4c99346788dc13536c86da93a946cf6ecb6234a258608&filter=updateCard:idList"
  return fetch(url, {method: 'GET', headers: {'content-type': 'application/json'}})
    .then((response) => response.json());
}

function update_cards_moved_to_the_done_list(actions_json){
  console.log("actions: ", actions_json);
  for(var i = 0 ; i < actions_json.length ; i++){ //since this is a asynchronous loop, it needs to have a private copy of the action it is operating on. If this doesn't work I'll try a primitive
    let local_func_exe = (function() {
      let local_scope_action_index  = i; // A copy of i only available to the scope of the inner function
      return function() {
        if(moved_to_done(actions_json[local_scope_action_index])){
        set_end_date(actions_json[local_scope_action_index]);
      }
    }
  })();
  local_func_exe(); //Execute the local scope function you created
  }//end loop
}//end outer

function moved_to_done(action){
  // console.log("Checking if action moved it to done: ", action.data.card.idShort);
  return (action.data.listAfter.name == "Done");
}

function set_end_date(action){
  let date = action.date;
  let card_id = action.data.card.id;

  if(complete_board_info > 0 && completed_id > 0){
    return set_custom_field(completed_id, card_id, date)
  }
  else{
    let url = "https://api.trello.com/1/boards/" +
      action.data.board.id + "/?list&cards=visible&card_fields=name&customFields=true&card_customFieldItems=true";
    url = addAuthToken(url);
    return fetch(url, {method: 'GET', headers: {'content-type': 'application/json'}})
    .then((response) => response.json())
    .then((board_data) => set_global_response(board_data))
    .then((customFieldTypes) => find_date_completed_field_id(customFieldTypes))
    .then((field_id) => set_custom_field(field_id, card_id, date));
  }  
}

function set_global_response(board_data){
  complete_board_info = board_data;
  return board_data.customFields;
}

function set_custom_field(custom_field, card_id, date){
  var url = "https://api.trello.com/1/cards/"+card_id+"/customField/"+custom_field+"/item?";
  url = addAuthToken(url);
  var data = {value: { date: date }};
  return fetch(url, { body: JSON.stringify(data), method: 'PUT', headers: {'content-type': 'application/json'}})
  .then((resp) => resp.json())
  .then(function(updated){
    // console.log("End Date Updated: ", updated);
    return updated.value.date; //return the date completed field so we can set the duration badge
  })
  .catch((err) => console.log(JSON.stringify(err, null, 2)));
}

function find_date_completed_field_id(custom_fields){
  try{
    // console.log("Custom Fields", custom_fields);
    for(let field of custom_fields){
        if(field.name == "Date Completed"){
          completed_id = field.id;
          return field.id;
        }
      }
  }
  catch(e){
    console.log("Error - Here be the customs fields", e, custom_fields);
  }
}

TrelloPowerUp.initialize({
  'card-badges': function(t, options){
    return getBadges(t);
  },
  'card-buttons': function(t, options){
    return [{
      icon: 'https://cdn.glitch.com/1b42d7fe-bda8-4af8-a6c8-eff0cea9e08a%2Frocket-ship.png?1494946700421',
      text: 'Mark Completed',
      callback: mark_card_completed,
    }];
  },
  'card-detail-badges': function(t, options) {
    return getBadges(t);
  },
});
```

## Finishing up the Support site

### Forms

I need to create all of the forms and make sure that they are submitting data properly.

Remember in atom that the alt-q keybinding expands the selection to the quotes. That would be even more useful for dreamweaver.

Computer is really sluggish so I am clearing out some ram and changing some finder settings.

1. Alt-rt click finder icon and relaunch
2. [Set default finder open to Downloads and keep that clear so it opens fast](https://paradite.com/2017/01/31/reduce-macos-finder-memory-usage/)
3. [Reduce the usage of mds_stores](https://www.neilturner.me.uk/2013/02/08/fixing-high-memory-usage-caused-by-mds.html) Continue with this if Finder is still slow or mds_stores uses up more memory.
4. PhPStorm File > Invalidate Caches and Restart
5. Reduce the indexed files in PHPStorm - Preferences > Directories > Rt.Click and Exclude so it turns orange
6. [Disabled spotlight to make things faster](https://forums.macrumors.com/threads/disabling-spotlight-in-sierra.2075261/)

Cleaning up the github repo. I haven't been merging anything since it's just me on the repository.
```
git branch --merged
git branch -d branch_name
```

## Add Kara Fitzgibbon to slider

Kara Fitzgibbon

Senior Project Coordinator

Kara earned her M.A. and Ph.D. in Sociology at the University of Virginia. While completing her graduate degree, she worked part-time at CSR as a Graduate Research Analyst. Beyond survey and social research methodology, her areas of specialty are race, ethnicity, immigration, and religion.

ksf5fe@virginia.edu

https://twitter.com/ksfitzgibbon

## CSS selectors of children

1. descendant selector (space) : .outer h2: All descendants
2. child selector (>) : .outer > h2 : Immediate Child
3. adjacent sibling selector (+) : .outer + h2 : Immediate Sibling from same parent
4. general sibling selector (~) : .outer ~ h2 : All Sibling from same parent

Attempt to run js updates of css classes

```js
jQuery(window).load(function(){
debugger;
jQuery('.views-row').each(function(i){
  setTimeout(function(){
    jQuery('.item').eq(i).addClass('is-visible');
  }, 100 * i);
});
});
```

Added the access analytics to theme files in html.html.twig

```html
<script src="https://cdn.levelaccess.net/accessjs/YW1wX3V2YTExMDA/access.js" type="text/javascript"></script>
```

```html
<script type="text/javascript">var access_analytics={base_url:"https://analytics.ssbbartgroup.com/api/",instance_id:"AA-58bdcc11cee35"};(function(a,b,c){var d=a.createElement(b);a=a.getElementsByTagName(b)[0];d.src=c.base_url+"access.js?o="+c.instance_id+"&v=2";a.parentNode.insertBefore(d,a)})(document,"script",access_analytics);</script>
```



# Simplesaml and Filemaker Pro Web Publishing

[Filemaker 16 guide with web server info](https://fmhelp.filemaker.com/docs/16/en/fms16_cwp_guide.pdf)

So we want to make sure that users are logged into Netbadge in order for them to look at specific databases in Filemaker on the web. They already have their permissions set through Active directory accounts. We just need to make sure that they are logged into netbadge to access the web-app at all.

So while building every page, we want to check if the user has a valid cookie that relates to a valid session stored at login.

The Cooopercenter.org site will handle the authentication and send the session data to the Filemaker server.

On all of the sensitive Filemaker pages, we'll add some php code to check for a valid session.
[Example](https://stackoverflow.com/questions/42022837/require-user-to-login-for-certain-pages)

```
<?php
if(isset( $_SESSION['SESS_MEMBER_ID']) && !empty($_SESSION['SESS_MEMBER_ID'])):?>
    Do your html and other code
<?php
    else:
        header("location:page.php"); // take them to page
     //or echo "You not allowed to view this page <a href=\"login.php\">Please login</a>";
    endif;
    ?>
```

So I need to find the php files or the PHP code that interacts with the FM API  and add some restrictive code.

## Failed attempts to get simplesaml on filemaker server

[Changing the filemakerhomepage](https://community.filemaker.com/thread/143388)
fmwebd_home.html

[fmsadmin settings edits](https://community.filemaker.com/thread/186328)

```
sudo fmsadmin set cwpconfig enablephp=true
sudo fmsadmin set cwpconfig UseFMPHP=false

Start & Stop FileMaker Server processes
sudo launchctl stop com.filemaker.fms
sudo launchctl start com.filemaker.fms
```

## Using the filemaker API to create webpages

Here is the location of the Filemaker API

For Apache (macOS): /Library/FileMaker Server/Documentation/PHP API
Documentation/index.html


# Acquia SSH Keys and Dev Desktop setup

- Remove all local sites from Dev Desktop. Preferences > remove local site.
- Create new SSH key in dev desktop and move it to your ssh folder. ex. `/Users/miles/.ssh`

```bash
ssh-keygen -t rsa -b 4096
```

- Upload that key to Acquia
- Clone the sites to Dev Desktop
- Make sure you clone the correct name so it matches


# Context Filters for Views

[How to add a Entity Reference View Type](https://drupal.stackexchange.com/questions/42034/how-to-create-a-view-type-of-entity-reference-display)

[Filtering by Current User logged in](https://drupal.stackexchange.com/questions/22427/filtering-on-node-whose-user-id-is-equal-to-the-current-user)

# Twig Theme Edits

[Overview of TWIG](https://www.drupal.org/docs/8/theming/twig)

[Enable Twig Debugging](https://www.youtube.com/watch?v=cLMxMf-DVIs)

1. Create services.yml from the default and put it in the site I want to edit (sorensen)
2. Changed twig cofing debug to true from false
3. Set auto reload to true from null
4. Turned off aggregate css and js in admin dashboard - Home>Admin>Configuration>Development

```
Double curly braces for simple prints {{ site_logo }} vs. {% if site_logo %}
```

## XDeBug and PHP

First I want to make sure my phpStorm setup is correct. [Acquia Setup for phpStorm and XDeBug](https://docs.acquia.com/dev-desktop/sites/phpstorm/)

Edit the php.ini file and specify the correct xdebug dll file. Dev Desktopo Preferences > config > php.ini edit

```
zend_extension=opcache.so
zend_extension=xdebug.so
xdebug.remote_enable=1
xdebug.remote_port="9000"
xdebug.profiler_enable=1
```

If you run into errors run `php -m` to get the modules php is running. If there is an error at the top of the output, fix that error and then try again. Often the full path to the extension will cause issues since php starts its search inside that ext directory that xdebug.so resides in.

![xdebug](../../images/Screen Shot 2018-08-07 at 3.06.27 PM.png)

Visit your phpinfo() output page `/admin/reports/status/php` to make sure that xdebug is in fact running. If it isn't you may need to restart apache.

![phpinfo](../../images/Screen Shot 2018-08-07 at 3.31.27 PM.png)

### Setting up the proper PHP for phpStorm

[Walkthrough](http://redcrackle.com/blog/drupal-8/phpstorm)

You need to specify the php version and an interpreter for PHPStorm to use. So go to `Preferences > Languages & Framewords > PHP` and set the path to the php file you are using with dev desktop.

![php setup](../../images/Screen Shot 2018-08-07 at 3.49.04 PM.png)

Now search for Drupal in preferences and set the Drupal Installation Path - this is the docroot that has sites modules and core folders in it.

![docroot drupal](../../images/Screen Shot 2018-08-07 at 3.51.44 PM.png)

## Hooks

So I'm running drupal 8.5.5 and trying to implement the hook [hook_menu_local_tasks_alter](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/function/hook_menu_local_tasks_alter/8.5.x). [Here's an explanation of how these hooks are defined and invoked.](https://x-team.com/blog/drupal-8-hooks/) It seems I need to use an OO approach to define my hook and implement it.

I found the hook I need but had to implement it in the module and then clear the cache so the module realized it was there.
