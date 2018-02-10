---
layout: default
---

# Transfer Drupal 7 content into Drupal 8

So I need to transfer the 2k+ pieces of content that the CEPS drupal 7 site contains. I am going to attempt to move it all on a fresh local copy of drupal 8.3.7 before I make the real move. So I'd like to transfer over the content without touching the way it's displayed. The migrate tools will be my first attempt.

To use the migration tools I need the database information. It's stored in the settings.php file of the site i want to copy. So I will SSH to the site using the bitnami key Mary Beth gave me.
```
chmod 600 key.pem
ssh -i key.pem ubuntu@vig.coopercenter.org
```

Using `find / -type d -name "sites" -print 2>/dev/null` I found the location of the sites. All the sites are stored at /var/www/html/sitename. I made a backup of the ceps database with the command `drush sql-dump > ceps.sql` executed in the ceps docroot. Now copy that file back.
`scp -i key.pem ubuntu@ceps.coopercenter.org:file_i_want.sql /local/directory`

### Can't connect to the database of the old sites.

I have tried copying the database directly from the live site using the   tool. I think the database only allows localhost access.

I tried downloading a sql-dump and loading that into phpmyadmin. It is too large of a sql dump file.

Now I am trying to use backup migrate like I do with the drupal 8 sites. It installed successfully but is stuck trying to make a Default Database download for me. The database backed up correctly. Now for the files. Then I can re-create the site locally and use that to feed into a local drupal 8 siteusing the migration tutorials.

Backup & Migrate also failed so now I am using the command line to attempt to install the mysql dump I got from the live server. Simply using the command `mysql database_target < dumpfile.sql`.

My next idea is to use the backup & migrate to transfer the site over piecemeal. One table of content at a time.

Just found out there is a cache clear button on the performance page...

mysql is located at /Applications/DevDesktop/mysql

you can uninstall modules with drushpm-uninstall name

After all of that I failed to get the content transfered to a drupal 8 site. I got the database imported into a drupal 7 site locally, I just can't get that site to connect to the drupal 8 site migrate. I keep getting some mysql socket error.

It may be that I am using a passwordless root access to the database.
It could be a mysql install error on my compupter.
It could be a problem with the migrate modules.

Tomorrow i will message the Drupalize.me people and watch a youtube video on the issue. That way I can see how it is supposed to go.

### Solved mysql socket issue

So Acquia sets up the mysql database but doesn't specify the default socket in the php.ini file. MySQL has been using the default socket but Acquia doesn't install MySQL in the default location. So PHP was looking in the wrong place for the socket to use too build the connection. Go into the Acquia Preferences > Config and then edit the php.ini for 7.0 (since that is the php version i'm using). Set the default socket name for mysql connects to `/Applications/DevDesktop/mysql/data/mysql.sock`. Now the migrate tools should be able to conect to the database of the local drupal 7 site.
```
; Default socket name for local MySQL connects.  If empty, uses the built-in
; MySQL defaults.
; http://php.net/pdo_mysql.default-socket
pdo_mysql.default_socket=/Applications/DevDesktop/mysql/data/mysql.sock
```

`drush migrate-upgrade --configure-only`

# [Migrate Walkthrough](https://drupalize.me/blog/201604/custom-drupal-drupal-migrations-migrate-tools)

[Video Of Example User Migration](https://www.youtube.com/watch?v=_z2FH0efd_g)

Copy this into D8 settings.php and change the database name/ credentials to the database of the D7 site.
```
// Database entry for `drush migrate-upgrade --configure-only`
$databases['upgrade']['default'] = array (
  'database' => 'd7_database',
  'username' => 'root',
  'password' => '',
  'prefix' => '',
  'host' => 'localhost',
  'port' => '3306',
  'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',
  'driver' => 'mysql',
);
```

Enable the migrate_tools migrate_plus migrate_upgrade modules.

```
drush en migrate_tools migrate_plus migrate_upgrade
```

Get the configuration files for the D7 site.
```
drush config-export --destination=/tmp/migrate
```

Before migration backup the database of the new site.
```
drush -v sql-dump --result-file=d8_fresh.sql
```

Restoring is as easy as
```
mysql database_target < d8_fresh.sql
```

# Cleaner Migration

The Default migration deleted a lot of the content on the D8 site. I want to update the ID's of the incoming data so that they migrate properly. Here's the roadmap as I understand it.

1. Copy the database and content of the D7 site to a local D7 site
2. Backup the database of that local D7 site so you can reload it after failed migrations
3. Create a D8 template site with all the Theme content I want
4. Install the needed plugins on the D8 site
5. Backup that D8 site database so I can restore it
6. Create a new migration plugin
7. Implement hook_migrate_prepare_row
8. Attempt to migrate and debug it
9. On failed migrations roll back the D8 database and try again

## Create a local d7 copy of the site

Because the permissions don't allow the ubuntu user to make files or directories, I had to make the drush sql backup in the ubuntu folder and copy it from there.
```
cd /Users/miles/Documents
ssh -i ssh_old_drupal_sites.pem ubuntu@certification.coopercenter.org
cd /var/www/html/
ls
cd certification.coopercenter.org/
drush -v sql-dump --result-file=/home/ubuntu/migrate/cert_d7.sql
```
Now copy the created content back to your local machine.
```
scp -i bitnamidrupal.pem ubuntu@ceps.coopercenter.org://home/ubuntu/migrate/cert_d7.sql .
scp -rp -i bitnamidrupal.pem ubuntu@ceps.coopercenter.org://var/www/html/certification.coopercenter.org/* cert/files/
```

Now I need a fresh Drupal 7 site to import my database and files into. Clone the fresh d7 site and make a new database with a short name. In this case it is cert7. `mysql cert7 < cert_d7.sql` For the files, copy over the sites/all/* contents and the sites/default/files/ folder contents. Don't copy over the settings.php file since that is what tells you what database to use. MAKE SURE THE TARGET SITE IS USING THE SAME PHP VERSION.

## Create a D8 template site.

I am going to use the SEI site since it worked so well last time. Pulled the site from Acquia and creating a SQL dump file using the Backup Migrate tool. Then I created a new multisite using DevDesktop and selected the sql file that Backup Migrate created. This could be done with drush as well but backup migrate is just as fast. Once the site is made, I copied the files from the sei site to the certification site's files folder. Before making a restore point for your backup, make sure that all of the migrate plugins are enabled on the extend page. Make the backup using Backup Migrate. To restore it simply run `mysql certification < pre_migration.sql` from the docroot directory where the migration backup is.

So I need to use backup migrate to make the site initially. Copy this into the install for extend
https://ftp.drupal.org/files/projects/backup_migrate-8.x-4.0-alpha2.tar.gz
/admin/config/development/backup_migrate

Restore the site from Backup Migrate. I started getting errors from the backup migrate saying that the entity reference revisions configuration was missing so I copied the modules, core, and themes folder from  my current copy of the production site.

I made a git repo locally to track file changes. I am also making a backup of the database so I can resore it.


## Create a custom Migration plugin

Copy this to settings.php . You may have to add write privileges to sites/default and settings.php
```
$databases['migrate']['default'] = array (
    'database' => 'cert7',
    'username' => 'root',
    'password' => '',
    'prefix' => '',
    'host' => 'localhost',
    'port' => '3306',
    'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',
    'driver' => 'mysql',
);
$databases['upgrade']['default'] = array (
    'database' => 'cert7',
    'username' => 'root',
    'password' => '',
    'prefix' => '',
    'host' => 'localhost',
    'port' => '3306',
    'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',
    'driver' => 'mysql',
);
$databases['drupal_7']['default'] = array (
    'database' => 'cert7',
    'username' => 'root',
    'password' => '',
    'prefix' => '',
    'host' => 'localhost',
    'port' => '3306',
    'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',
    'driver' => 'mysql',
);
```
I think this specifies my new database
```
$databases['default']['default'] = array (
    'database' => 'certification',
    'username' => 'root',
    'password' => '',
    'prefix' => '',
    'host' => 'localhost',
    'port' => '3306',
    'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',
    'driver' => 'mysql',
);
```

I also made sure the staging config directory exists. This is where the generated YAML files go for migrations.
`$config_directories['staging'] = 'sites/default/staging';`

Using this connection i will generate the migration template files for the drupal 8 site. [Instructions here](https://drupalize.me/tutorial/create-migrations-core-templates?p=2578)



To roll back the migration I have the sql backup made. `mysql d8 < pre_migration.sql`
Then  I created the migration files. `drush migrate-upgrade --configure-only`
Copy those migration files to where they are needed. `drush config-export --destination=~/Sites/migrate/cert2/`

`drush config-export --destination=~/Sites/devdesktop/8_5/sites/default/staging/`

Copy these configuration files to the staging configuration directory you declared in settings.php. You will delete all of the migration YAML files that you want to ignore. Following with the youtube example I will just migrate the migrate_drupal_7 and upgrade_d7_user files.

`drush config-import staging`

After running `drush ms` for migrate status I got a lot of errors and way too many migration files. I removed all of the database connections except for the drupal_7 one that we created from the key in migrate_drupal_7.YAML:
```
$databases['drupal_7']['default'] = array (
    'database' => 'cert7',
    'username' => 'root',
    'password' => '',
    'prefix' => '',
    'host' => 'localhost',
    'port' => '3306',
    'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',
    'driver' => 'mysql',
);
```

After editing the users migration file so that it didn't require user_roles as a dependency, I imported the the migration with `drush mi upgrade_d7_user`. This ran that single migration file. The result was all of the users were successfully migrated.

### Now How Do I run this migration for all of the nodes, content_types, and nodes?

I tried running a migration with a whole bunch of migration files and it failed to transfer a lot of the content. So I am going to roll the database back and try again with just the basic page nodes. The migration didn't work with `drush migrate-import --group=migrate_drupal_7` which attempted to do all of the migrations at once.

[This tutorial covers the process of creating nodes from a CSV file](https://evolvingweb.ca/blog/drupal-8-migration-migrating-basic-data-part-1) It will be useful for importing the LOST data.

I need to create a new module and add the hook_migrate_prepare_row override to correct the ID numbers for blocks and nodes.

## Template site creation

Create a fresh D8 site.
Enable backup migrate.
Transfer LEAD site database to it.
Transfer LEAD site files to it.
Make sure the migrate plugins are activated and installed.

BACKUP THE SITE with backup migrate, drush, and git.
The files will backup with git and the database with the sql dump

## Create configuration for migration

Edit the settings.php so you can generate migration YAML files.
Copy this video to transfer over users - https://www.youtube.com/watch?v=_z2FH0efd_g
Try to transfer over just the Users from D7 to D8
Users transferred successfully.

# New Migration Strategy

So the real problem is that I can't get content from the old sites to migrate into my template site. I can get the content to migrate into a regular version of Drupal 8 though. So let's make this a 5 step process to avoid losing nodes.

1. Create local D7 site that's a copy of the live D7 sites
2. Create a template D8 site with dummy content
3. Create a new fresh D8 site
4. Migrate the local D7 content into the fresh D8 site
5. Migrate the content from that fresh D8 site into the template D8 site

## Template site made

I also created a template fresh D8 site called clone that has all of the needed modules installed for the last 4 migrations. All the migrate tools and admin tools for easier UI access.

1. Clone the 'clone' site and make sure the needed plugins are activated

## Migrate the Fresh site

1. Got to http://cert8.dd:8083/upgrade the /upgrade page and run through the migration
2. Username - root
3. Password is blank
4. Database - cert7
5. Host - localhost
6. The public files directory - `/Users/miles/Sites/devdesktop/cert7`
7. Confirm you have the basic upgrade paths and run the upgrade

block
block_content
contact
dblog
field
file
filter
image
menu
menu_link_content
menu_ui
node
path
search
shortcut
file
system
taxonomy
text
update
user

## Transfer content Types over

So what content types do I need to move from the migrated site to the certification site?
1. tav_course_descriptions
2. Events
3. publications

### Failed Attempt
tav_course_descriptions have an entity reference in them that I am removing so the transferred content is just the essential content. These configurations got changed.
```
node.tav_course_descriptions.default
node.tav_course_descriptions.default
node.tav_course_descriptions.search_index
node.tav_course_descriptions.search_result
node.tav_course_descriptions.teaser
```

Tried transferring the configurations in the config table. I believe I am missing some configuration connected to actual nodes.
```
Update configure_status_field_widget

Failed: Drupal\Core\Field\FieldException: Attempt to create a field field_target_audience that does not exist on entity type node. in Drupal\field\Entity\FieldConfig->getFieldStorageDefinition() (line 293 of /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/modules/field/src/Entity/FieldConfig.php).
```

This failed horribly so I need to truncate and restore certification from a backup.
`mysql -Nse 'show tables' certification | while read table; do mysql -e "truncate table $table" certification; done`

### Successful Content Type Transfer

Use the Features module and export the Content Types you want individually. Then install them like a module on the real site. The Features module gives your some problems though.
```
Unable to install Publications Type due to unmet dependencies: core.entity_form_display.node.news_item.default (field.field.node.news_item.body, field.field.node.news_item.field_photo, node.type.news_item), field.field.node.news_item.field_publication (node.type.news_item), field.field.node.publications.field_publication_date (field.storage.node.field_publication_date)
```

## Transfer over the actual content

We have four fields to transfer over :
- body
- field_mandatory_elective
- field_prerequisites
- field_target_audience
