---
layout: default
---

# Transfer Drupal 7 content into Drupal 8

So I need to transfer the 2k+ pieces of content that the CEPS drupal 7 site contains. I am going to attempt to move it all on a fresh local copy of drupal 8.3.7 before I make the real move. So I'd like to transfer over the content without touching the way it's displayed. The migrate tools will be my first attempt.

To use the migration tools I need the database information. It's stored in the settings.php file of the site i want to copy. So I will SSH to the site using the bitnami key Mary Beth gave me.
```
chmod 600 key.pem
ssh -i key.pem upuntu@ceps.coopercenter.org
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
scp -i key.pem ubuntu@ceps.coopercenter.org://home/ubuntu/migrate/cert_d7.sql .
scp -rp -i key.pem ubuntu@ceps.coopercenter.org://var/www/html/certification.coopercenter.org/* cert/files/
```
Now I need a fresh Drupal 7 site to import my database and files into. Clone the fresh d7 site and make a new database with a short name. In this case it is cert7. `mysql cert7 < cert_d7.sql` For the files, copy over the sites/all/* contents and the sites/default/files/ folder contents. Don't copy over the settings.php file since that is what tells you what database to use.

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

# Plans for Tomorrow

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

## After sucessfully transfering over the Users I am getting this error when I run the other migrations
```
-172-25-19-187:8_4 miles$ drush migrate-rollback
You must specify --all, --group, --tag, or one or more migration names separated by commas                                                                                                                       [error]
d-172-25-19-187:8_4 miles$ drush migrate-rollback --all
Rolled back 0 items - done with 'upgrade_d7_taxonomy_term_vocabulary_13'                                                                                                                                         [status]
Rolled back 0 items - done with 'upgrade_d7_taxonomy_term_vocabulary_12'                                                                                                                                         [status]
Rolled back 0 items - done with 'upgrade_d7_taxonomy_term_tags'                                                                                                                                                  [status]
Rolled back 31 items - done with 'upgrade_d7_taxonomy_term_staff_authors'                                                                                                                                        [status]
Rolled back 9 items - done with 'upgrade_d7_taxonomy_term_publication_types'                                                                                                                                     [status]
Rolled back 5 items - done with 'upgrade_d7_taxonomy_term_publication_series'                                                                                                                                    [status]
Rolled back 23 items - done with 'upgrade_d7_taxonomy_term_class_types'                                                                                                                                          [status]
Rolled back 0 items - done with 'upgrade_d7_taxonomy_term_categorize_content'                                                                                                                                    [status]
Rolled back 9 items - done with 'upgrade_d7_node_title_label'                                                                                                                                                    [status]
Rolled back 20 items - done with 'upgrade_d7_node_tav_course_descriptions'                                                                                                                                       [status]
Rolled back 3 items - done with 'upgrade_d7_node_staff_member'                                                                                                                                                   [status]
Rolled back 56 items - done with 'upgrade_d7_node_publications'                                                                                                                                                  [status]
Rolled back 3 items - done with 'upgrade_d7_node_page'                                                                                                                                                           [status]
Rolled back 0 items - done with 'upgrade_d7_node_news_item'                                                                                                                                                      [status]
Rolled back 0 items - done with 'upgrade_d7_node_jobs'                                                                                                                                                           [status]
Rolled back 140 items - done with 'upgrade_d7_node_events'                                                                                                                                                       [status]
Rolled back 0 items - done with 'upgrade_d7_node_event'                                                                                                                                                          [status]
Rolled back 2 items - done with 'upgrade_d7_node_article'                                                                                                                                                        [status]
Rolled back 5 items - done with 'upgrade_d7_filter_format'                                                                                                                                                       [status]
Rolled back 68 items - done with 'upgrade_d7_field_instance_widget_settings'                                                                                                                                     [status]
Rolled back 272 items - done with 'upgrade_d7_field_formatter_settings'                                                                                                                                          [status]
Rolled back 12 items - done with 'upgrade_d7_view_modes'                                                                                                                                                         [status]
Rolled back 68 items - done with 'upgrade_d7_field_instance'                                                                                                                                                     [status]
Rolled back 1 item - done with 'upgrade_user_picture_entity_form_display'                                                                                                                                        [status]
Rolled back 1 item - done with 'upgrade_user_picture_entity_display'                                                                                                                                             [status]
Rolled back 8 items - done with 'upgrade_d7_taxonomy_vocabulary'                                                                                                                                                 [status]
Rolled back 1 item - done with 'upgrade_user_picture_field_instance'                                                                                                                                             [status]
Rolled back 9 items - done with 'upgrade_d7_node_type'                                                                                                                                                           [status]
Rolled back 1 item - done with 'upgrade_d7_contact_settings'                                                                                                                                                     [status]
Rolled back 1 item - done with 'upgrade_user_picture_field'                                                                                                                                                      [status]
Rolled back 53 items - done with 'upgrade_d7_field'                                                                                                                                                              [status]
Rolled back 1 item - done with 'upgrade_text_settings'                                                                                                                                                           [status]
Rolled back 1 item - done with 'upgrade_taxonomy_settings'                                                                                                                                                       [status]
Rolled back 301 items - done with 'upgrade_d7_url_alias'                                                                                                                                                         [status]
Rolled back 1 item - done with 'upgrade_d7_node_settings'                                                                                                                                                        [status]
Rolled back 1 item - done with 'upgrade_d7_image_styles'                                                                                                                                                         [status]
Rolled back 1 item - done with 'upgrade_d7_image_settings'                                                                                                                                                       [status]
Rolled back 1 item - done with 'upgrade_d7_filter_settings'                                                                                                                                                      [status]
Rolled back 0 items - done with 'upgrade_d7_file_private'                                                                                                                                                        [status]
Rolled back 61 items - done with 'upgrade_d7_file'                                                                                                                                                               [status]
Rolled back 1 item - done with 'upgrade_d7_dblog_settings'                                                                                                                                                       [status]
Rolled back 1 item - done with 'upgrade_contact_category'                                                                                                                                                        [status]
Rolled back 1 item - done with 'd6_upload_field'                                                                                                                                                                 [status]
Rolled back 1 item - done with 'user_picture_field'                                                                                                                                                              [status]
Rolled back 1 item - done with 'block_content_entity_form_display'                                                                                                                                               [status]
Rolled back 1 item - done with 'block_content_entity_display'                                                                                                                                                    [status]
Rolled back 1 item - done with 'block_content_body_field'                                                                                                                                                        [status]
Rolled back 1 item - done with 'block_content_type'                                                                                                                                                              [status]
d-172-25-19-187:8_4 miles$ ms
-bash: ms: command not found
d-172-25-19-187:8_4 miles$ drush ms
 Group: Import from Drupal 7 (migrate_drupal_7)  Status  Total  Imported  Unprocessed  Last imported       
 upgrade_contact_category                        Idle    1      0         1            2017-09-27 17:18:40
 upgrade_d7_dblog_settings                       Idle    0      0         0            2017-09-27 17:18:40
 upgrade_d7_file                                 Idle    61     0         61           2017-09-27 17:18:40
 upgrade_d7_file_private                         Idle    0      0         0            2017-09-27 17:18:40
 upgrade_d7_filter_settings                      Idle    1      0         1            2017-09-27 17:18:40
 upgrade_d7_image_settings                       Idle    0      0         0            2017-09-27 17:18:40
 upgrade_d7_image_styles                         Idle    1      0         1            2017-09-27 17:18:40
 upgrade_d7_node_settings                        Idle    1      0         1            2017-09-27 17:18:40
 upgrade_d7_url_alias                            Idle    301    0         301          2017-09-27 17:18:40
 upgrade_taxonomy_settings                       Idle    0      0         0            2017-09-27 17:18:41
 upgrade_text_settings                           Idle    0      0         0            2017-09-27 17:18:41
 upgrade_d7_field                                Idle    53     0         53           2017-09-27 17:18:41
 upgrade_user_picture_field                      Idle    1      0         1            2017-09-27 17:18:41
 upgrade_d7_contact_settings                     Idle    1      0         1            2017-09-27 17:18:41
 upgrade_d7_node_type                            Idle    9      0         9            2017-09-27 17:18:41
 upgrade_user_picture_field_instance             Idle    1      0         1            2017-09-27 17:18:41
 upgrade_d7_taxonomy_vocabulary                  Idle    8      0         8            2017-09-27 17:18:41
 upgrade_user_picture_entity_display             Idle    1      0         1            2017-09-27 17:18:41
 upgrade_user_picture_entity_form_display        Idle    1      0         1            2017-09-27 17:18:41
 upgrade_d7_field_instance                       Idle    68     0         68           2017-09-27 17:18:41
 upgrade_d7_view_modes                           Idle    14     0         14           2017-09-27 17:18:41
 upgrade_d7_field_formatter_settings             Idle    272    0         272          2017-09-27 17:18:41
 upgrade_d7_field_instance_widget_settings       Idle    68     0         68           2017-09-27 17:18:41
 upgrade_d7_filter_format                        Idle    5      0         5            2017-09-27 17:18:41
 upgrade_d7_node_article                         Idle    2      0         2            2017-09-27 17:18:41
 upgrade_d7_node_event                           Idle    0      0         0            2017-09-27 17:18:41
 upgrade_d7_node_events                          Idle    140    0         140          2017-09-27 17:18:42
 upgrade_d7_node_jobs                            Idle    0      0         0            2017-09-27 17:18:42
 upgrade_d7_node_news_item                       Idle    0      0         0            2017-09-27 17:18:42
 upgrade_d7_node_page                            Idle    3      0         3            2017-09-27 17:18:42
 upgrade_d7_node_publications                    Idle    56     0         56           2017-09-27 17:18:42
 upgrade_d7_node_staff_member                    Idle    3      0         3            2017-09-27 17:18:42
 upgrade_d7_node_tav_course_descriptions         Idle    20     0         20           2017-09-27 17:18:42
 upgrade_d7_node_title_label                     Idle    9      0         9            2017-09-27 17:18:42
 upgrade_d7_taxonomy_term_categorize_content     Idle    0      0         0            2017-09-27 17:18:42
 upgrade_d7_taxonomy_term_class_types            Idle    23     0         23           2017-09-27 17:18:42
 upgrade_d7_taxonomy_term_publication_series     Idle    5      0         5            2017-09-27 17:18:42
 upgrade_d7_taxonomy_term_publication_types      Idle    9      0         9            2017-09-27 17:18:42
 upgrade_d7_taxonomy_term_staff_authors          Idle    31     0         31           2017-09-27 17:18:42
 upgrade_d7_taxonomy_term_tags                   Idle    0      0         0            2017-09-27 17:18:42
 upgrade_d7_taxonomy_term_vocabulary_12          Idle    0      0         0            2017-09-27 17:18:42
 upgrade_d7_taxonomy_term_vocabulary_13          Idle    0      0         0            2017-09-27 17:18:42
 Group: default                                  Status  Total  Imported  Unprocessed  Last imported       
 block_content_type                              Idle    1      0         1            2017-09-27 17:18:42
 block_content_body_field                        Idle    1      0         1            2017-09-27 17:18:42
 block_content_entity_display                    Idle    1      0         1            2017-09-27 17:18:43
 block_content_entity_form_display               Idle    1      0         1            2017-09-27 17:18:43
 user_picture_field                              Idle    1      0         1            2017-09-27 17:18:43
 d6_upload_field                                 Idle    1      0         1            2017-09-27 17:18:43
d-172-25-19-187:8_4 miles$ drush migrate-import --group=migrate_drupal_7
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_contact_category'                                                                                                              [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_dblog_settings'                                                                                                             [status]
Processed 61 items (0 created, 0 updated, 61 failed, 0 ignored) - done with 'upgrade_d7_file'                                                                                                                    [status]
Processed 0 items (0 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_file_private'                                                                                                              [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_filter_settings'                                                                                                            [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_image_settings'                                                                                                             [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_image_styles'                                                                                                               [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_node_settings'                                                                                                              [status]
Processed 301 items (301 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_url_alias'                                                                                                             [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_taxonomy_settings'                                                                                                             [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_text_settings'                                                                                                                 [status]
The SQL storage cannot change the schema for an existing field (field_location in node entity) with data.                                                                                                        [error]
(/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorageSchema.php:1312)
Cannot change the field type for an existing field storage. (/Users/miles/Sites/devdesktop/8_4/core/modules/field/src/Entity/FieldStorageConfig.php:366)                                                         [error]
Cannot change the field type for an existing field storage. (/Users/miles/Sites/devdesktop/8_4/core/modules/field/src/Entity/FieldStorageConfig.php:366)                                                         [error]
Cannot change the field type for an existing field storage. (/Users/miles/Sites/devdesktop/8_4/core/modules/field/src/Entity/FieldStorageConfig.php:366)                                                         [error]
Cannot change the field type for an existing field storage. (/Users/miles/Sites/devdesktop/8_4/core/modules/field/src/Entity/FieldStorageConfig.php:366)                                                         [error]
Cannot change the field type for an existing field storage. (/Users/miles/Sites/devdesktop/8_4/core/modules/field/src/Entity/FieldStorageConfig.php:366)                                                         [error]
Processed 53 items (47 created, 0 updated, 6 failed, 0 ignored) - done with 'upgrade_d7_field'                                                                                                                   [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_user_picture_field'                                                                                                            [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_contact_settings'                                                                                                           [status]
Processed 9 items (9 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_node_type'                                                                                                                 [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_user_picture_field_instance'                                                                                                   [status]
Processed 8 items (8 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_taxonomy_vocabulary'                                                                                                       [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_user_picture_entity_display'                                                                                                   [status]
Processed 1 item (1 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_user_picture_entity_form_display'                                                                                              [status]
Missing bundle entity, entity type comment_type, entity id comment_node_page. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                                 [error]
Missing bundle entity, entity type comment_type, entity id comment_node_article. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                              [error]
Missing bundle entity, entity type comment_type, entity id comment_node_publications. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                         [error]
Missing bundle entity, entity type comment_type, entity id comment_node_tav_course_descriptions. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                              [error]
Missing bundle entity, entity type comment_type, entity id comment_node_events. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                               [error]
Missing bundle entity, entity type comment_type, entity id comment_node_staff_member. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                         [error]
Missing bundle entity, entity type comment_type, entity id comment_node_event. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                                [error]
Processed 68 items (61 created, 0 updated, 7 failed, 0 ignored) - done with 'upgrade_d7_field_instance'                                                                                                          [status]
Processed 14 items (14 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_view_modes'                                                                                                              [status]
Missing bundle entity, entity type comment_type, entity id comment_node_article. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                              [error]
Missing bundle entity, entity type comment_type, entity id comment_node_event. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                                [error]
Missing bundle entity, entity type comment_type, entity id comment_node_events. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                               [error]
Missing bundle entity, entity type comment_type, entity id comment_node_page. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                                 [error]
Missing bundle entity, entity type comment_type, entity id comment_node_publications. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                         [error]
Missing bundle entity, entity type comment_type, entity id comment_node_staff_member. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                         [error]
Missing bundle entity, entity type comment_type, entity id comment_node_tav_course_descriptions. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                              [error]
The "taxonomy_term_reference_plain" plugin does not exist. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Component/Plugin/Discovery/DiscoveryTrait.php:52)                                                  [error]
The "taxonomy_term_reference_plain" plugin does not exist. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Component/Plugin/Discovery/DiscoveryTrait.php:52)                                                  [error]
The "taxonomy_term_reference_plain" plugin does not exist. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Component/Plugin/Discovery/DiscoveryTrait.php:52)                                                  [error]
The "taxonomy_term_reference_plain" plugin does not exist. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Component/Plugin/Discovery/DiscoveryTrait.php:52)                                                  [error]
The "link_url" plugin does not exist. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Component/Plugin/Discovery/DiscoveryTrait.php:52)                                                                       [error]
The "file_download_link" plugin does not exist. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Component/Plugin/Discovery/DiscoveryTrait.php:52)                                                             [error]
Processed 272 items (157 created, 0 updated, 13 failed, 102 ignored) - done with 'upgrade_d7_field_formatter_settings'                                                                                           [status]
Missing bundle entity, entity type comment_type, entity id comment_node_page. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                                 [error]
Missing bundle entity, entity type comment_type, entity id comment_node_article. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                              [error]
Missing bundle entity, entity type comment_type, entity id comment_node_publications. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                         [error]
Missing bundle entity, entity type comment_type, entity id comment_node_tav_course_descriptions. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                              [error]
Missing bundle entity, entity type comment_type, entity id comment_node_events. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                               [error]
Missing bundle entity, entity type comment_type, entity id comment_node_staff_member. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                         [error]
Missing bundle entity, entity type comment_type, entity id comment_node_event. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/EntityType.php:882)                                                [error]
Processed 68 items (55 created, 0 updated, 7 failed, 6 ignored) - done with 'upgrade_d7_field_instance_widget_settings'                                                                                          [status]
Missing filter plugin: filter_null.                                                                                                                                                                              [error]
Missing filter plugin: filter_null.                                                                                                                                                                              [error]
Missing filter plugin: filter_null.                                                                                                                                                                              [error]
Missing filter plugin: filter_null.                                                                                                                                                                              [error]
Processed 5 items (5 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_filter_format'                                                                                                             [status]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '331' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 331
    [:db_insert_placeholder_1] => 331
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1496679186
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '331' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 331
    [:db_insert_placeholder_1] => 331
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1496679186
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Processed 2 items (1 created, 0 updated, 1 failed, 0 ignored) - done with 'upgrade_d7_node_article'                                                                                                              [status]
Processed 0 items (0 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_node_event'                                                                                                                [status]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '68-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}           [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 68
    [:db_insert_placeholder_1] => 68
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-10-26 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '68-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                     [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 68
    [:db_insert_placeholder_1] => 68
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-10-26 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '69-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}           [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 69
    [:db_insert_placeholder_1] => 69
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-11-05 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '69-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                     [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 69
    [:db_insert_placeholder_1] => 69
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-11-05 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '70-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}           [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 70
    [:db_insert_placeholder_1] => 70
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-11-09 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '70-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                     [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 70
    [:db_insert_placeholder_1] => 70
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-11-09 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '72-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}           [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 72
    [:db_insert_placeholder_1] => 72
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-10-29 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '72-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                     [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 72
    [:db_insert_placeholder_1] => 72
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-10-29 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '73-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}           [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 73
    [:db_insert_placeholder_1] => 73
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-10-30 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '73-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                     [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 73
    [:db_insert_placeholder_1] => 73
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-10-30 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '143-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 143
    [:db_insert_placeholder_1] => 143
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-12-09 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '143-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 143
    [:db_insert_placeholder_1] => 143
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-12-09 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '194-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 194
    [:db_insert_placeholder_1] => 194
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-11-10 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '194-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 194
    [:db_insert_placeholder_1] => 194
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-11-10 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '278-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 278
    [:db_insert_placeholder_1] => 278
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 63
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '278-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 278
    [:db_insert_placeholder_1] => 278
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 63
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '279-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 279
    [:db_insert_placeholder_1] => 279
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '279-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 279
    [:db_insert_placeholder_1] => 279
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '280-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 280
    [:db_insert_placeholder_1] => 280
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-04-14 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '280-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 280
    [:db_insert_placeholder_1] => 280
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-04-14 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '281' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 281
    [:db_insert_placeholder_1] => 281
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449587417
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '281' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 281
    [:db_insert_placeholder_1] => 281
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449587417
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '282-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 282
    [:db_insert_placeholder_1] => 282
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-04-22 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '282-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 282
    [:db_insert_placeholder_1] => 282
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-04-22 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '283-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 283
    [:db_insert_placeholder_1] => 283
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-04-24 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '283-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 283
    [:db_insert_placeholder_1] => 283
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-04-24 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '284-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 284
    [:db_insert_placeholder_1] => 284
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-05-08 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '284-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 284
    [:db_insert_placeholder_1] => 284
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-05-08 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '285-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 285
    [:db_insert_placeholder_1] => 285
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 52
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '285-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 285
    [:db_insert_placeholder_1] => 285
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 52
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '286' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 286
    [:db_insert_placeholder_1] => 286
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449587667
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '286' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 286
    [:db_insert_placeholder_1] => 286
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449587667
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '287-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 287
    [:db_insert_placeholder_1] => 287
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-08-12 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '287-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 287
    [:db_insert_placeholder_1] => 287
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-08-12 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '289-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 289
    [:db_insert_placeholder_1] => 289
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '289-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 289
    [:db_insert_placeholder_1] => 289
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '290-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 290
    [:db_insert_placeholder_1] => 290
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 55
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '290-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 290
    [:db_insert_placeholder_1] => 290
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 55
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '291' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 291
    [:db_insert_placeholder_1] => 291
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449588368
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '291' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 291
    [:db_insert_placeholder_1] => 291
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449588368
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '294-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 294
    [:db_insert_placeholder_1] => 294
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 292
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '294-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 294
    [:db_insert_placeholder_1] => 294
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 292
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '295-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 295
    [:db_insert_placeholder_1] => 295
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 56
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '295-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 295
    [:db_insert_placeholder_1] => 295
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 56
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '296' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 296
    [:db_insert_placeholder_1] => 296
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449597303
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '296' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 296
    [:db_insert_placeholder_1] => 296
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449597303
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '297-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 297
    [:db_insert_placeholder_1] => 297
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '297-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 297
    [:db_insert_placeholder_1] => 297
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '298-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 298
    [:db_insert_placeholder_1] => 298
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '298-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 298
    [:db_insert_placeholder_1] => 298
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '299-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 299
    [:db_insert_placeholder_1] => 299
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-11-05 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '299-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 299
    [:db_insert_placeholder_1] => 299
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-11-05 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '300-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 300
    [:db_insert_placeholder_1] => 300
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-11-06 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '300-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 300
    [:db_insert_placeholder_1] => 300
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-11-06 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '301' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 301
    [:db_insert_placeholder_1] => 301
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449597280
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '301' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 301
    [:db_insert_placeholder_1] => 301
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449597280
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '302-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 302
    [:db_insert_placeholder_1] => 302
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-11-13 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '302-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 302
    [:db_insert_placeholder_1] => 302
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2014-11-13 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '303-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 303
    [:db_insert_placeholder_1] => 303
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-01-26 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '303-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 303
    [:db_insert_placeholder_1] => 303
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-01-26 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '304-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 304
    [:db_insert_placeholder_1] => 304
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '304-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 304
    [:db_insert_placeholder_1] => 304
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '305-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 305
    [:db_insert_placeholder_1] => 305
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '305-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 305
    [:db_insert_placeholder_1] => 305
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '306' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 306
    [:db_insert_placeholder_1] => 306
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449597480
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '306' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 306
    [:db_insert_placeholder_1] => 306
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449597480
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '307-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 307
    [:db_insert_placeholder_1] => 307
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 52
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '307-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 307
    [:db_insert_placeholder_1] => 307
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 52
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '308-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 308
    [:db_insert_placeholder_1] => 308
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '308-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 308
    [:db_insert_placeholder_1] => 308
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '309-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 309
    [:db_insert_placeholder_1] => 309
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-03-24 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '309-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 309
    [:db_insert_placeholder_1] => 309
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-03-24 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '310-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 310
    [:db_insert_placeholder_1] => 310
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-03-25 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '310-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 310
    [:db_insert_placeholder_1] => 310
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-03-25 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '311' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 311
    [:db_insert_placeholder_1] => 311
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449597262
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '311' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 311
    [:db_insert_placeholder_1] => 311
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1449597262
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '312-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 312
    [:db_insert_placeholder_1] => 312
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-04-02 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '312-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 312
    [:db_insert_placeholder_1] => 312
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-04-02 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '313-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 313
    [:db_insert_placeholder_1] => 313
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 52
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '313-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 313
    [:db_insert_placeholder_1] => 313
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 52
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '314-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 314
    [:db_insert_placeholder_1] => 314
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 64
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '314-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 314
    [:db_insert_placeholder_1] => 314
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 64
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '315-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 315
    [:db_insert_placeholder_1] => 315
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '315-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 315
    [:db_insert_placeholder_1] => 315
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '316' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 316
    [:db_insert_placeholder_1] => 316
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455038790
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '316' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 316
    [:db_insert_placeholder_1] => 316
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455038790
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '317-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 317
    [:db_insert_placeholder_1] => 317
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-08-10 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '317-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 317
    [:db_insert_placeholder_1] => 317
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-08-10 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '318-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 318
    [:db_insert_placeholder_1] => 318
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '318-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 318
    [:db_insert_placeholder_1] => 318
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '319-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 319
    [:db_insert_placeholder_1] => 319
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '319-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 319
    [:db_insert_placeholder_1] => 319
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '320-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 320
    [:db_insert_placeholder_1] => 320
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-11-12 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '320-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 320
    [:db_insert_placeholder_1] => 320
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2015-11-12 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '324-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 324
    [:db_insert_placeholder_1] => 324
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-01-24 03:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '324-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 324
    [:db_insert_placeholder_1] => 324
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-01-24 03:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '333-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 333
    [:db_insert_placeholder_1] => 333
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 334
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '333-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 333
    [:db_insert_placeholder_1] => 333
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 334
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '335-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 335
    [:db_insert_placeholder_1] => 335
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 334
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '335-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 335
    [:db_insert_placeholder_1] => 335
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 334
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '340-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 340
    [:db_insert_placeholder_1] => 340
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '340-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 340
    [:db_insert_placeholder_1] => 340
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '342-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 342
    [:db_insert_placeholder_1] => 342
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-04-13 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '342-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 342
    [:db_insert_placeholder_1] => 342
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-04-13 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '343-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 343
    [:db_insert_placeholder_1] => 343
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-04-14 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '343-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 343
    [:db_insert_placeholder_1] => 343
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-04-14 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '344-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 344
    [:db_insert_placeholder_1] => 344
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-04-19 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '344-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 344
    [:db_insert_placeholder_1] => 344
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-04-19 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '345-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 345
    [:db_insert_placeholder_1] => 345
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-04-20 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '345-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 345
    [:db_insert_placeholder_1] => 345
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-04-20 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '346' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 346
    [:db_insert_placeholder_1] => 346
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1463574780
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '346' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 346
    [:db_insert_placeholder_1] => 346
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1463574780
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '347-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 347
    [:db_insert_placeholder_1] => 347
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-07-14 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '347-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 347
    [:db_insert_placeholder_1] => 347
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-07-14 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '348-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 348
    [:db_insert_placeholder_1] => 348
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-08-01 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '348-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 348
    [:db_insert_placeholder_1] => 348
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-08-01 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '349-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 349
    [:db_insert_placeholder_1] => 349
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-08-09 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '349-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 349
    [:db_insert_placeholder_1] => 349
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-08-09 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '350-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 350
    [:db_insert_placeholder_1] => 350
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-03-30 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '350-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 350
    [:db_insert_placeholder_1] => 350
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-03-30 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '353-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 353
    [:db_insert_placeholder_1] => 353
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '353-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 353
    [:db_insert_placeholder_1] => 353
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '354-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 354
    [:db_insert_placeholder_1] => 354
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 52
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '354-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 354
    [:db_insert_placeholder_1] => 354
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 52
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '355-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 355
    [:db_insert_placeholder_1] => 355
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-05-03 08:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '355-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 355
    [:db_insert_placeholder_1] => 355
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-05-03 08:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '356' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 356
    [:db_insert_placeholder_1] => 356
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455110817
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '356' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 356
    [:db_insert_placeholder_1] => 356
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455110817
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '359-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 359
    [:db_insert_placeholder_1] => 359
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '359-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 359
    [:db_insert_placeholder_1] => 359
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '360-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 360
    [:db_insert_placeholder_1] => 360
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 65
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '360-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 360
    [:db_insert_placeholder_1] => 360
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 65
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '361' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 361
    [:db_insert_placeholder_1] => 361
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1467059979
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '361' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 361
    [:db_insert_placeholder_1] => 361
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1467059979
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '362-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 362
    [:db_insert_placeholder_1] => 362
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-08-07 15:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '362-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 362
    [:db_insert_placeholder_1] => 362
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-08-07 15:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '363-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 363
    [:db_insert_placeholder_1] => 363
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-06-19 15:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '363-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 363
    [:db_insert_placeholder_1] => 363
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-06-19 15:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '365-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 365
    [:db_insert_placeholder_1] => 365
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 55
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '365-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 365
    [:db_insert_placeholder_1] => 365
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 55
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '367-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 367
    [:db_insert_placeholder_1] => 367
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 64
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '367-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 367
    [:db_insert_placeholder_1] => 367
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 64
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '368-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 368
    [:db_insert_placeholder_1] => 368
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-04-26 12:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '368-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 368
    [:db_insert_placeholder_1] => 368
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-04-26 12:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '369-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 369
    [:db_insert_placeholder_1] => 369
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-03-11 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '369-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 369
    [:db_insert_placeholder_1] => 369
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-03-11 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '372-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 372
    [:db_insert_placeholder_1] => 372
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 292
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '372-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 372
    [:db_insert_placeholder_1] => 372
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 292
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '373-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 373
    [:db_insert_placeholder_1] => 373
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 56
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '373-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 373
    [:db_insert_placeholder_1] => 373
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 56
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '374-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 374
    [:db_insert_placeholder_1] => 374
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-08-09 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '374-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 374
    [:db_insert_placeholder_1] => 374
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-08-09 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '376' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 376
    [:db_insert_placeholder_1] => 376
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1458747686
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '376' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 376
    [:db_insert_placeholder_1] => 376
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1458747686
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '379-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 379
    [:db_insert_placeholder_1] => 379
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-09-20 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '379-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 379
    [:db_insert_placeholder_1] => 379
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-09-20 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '380-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 380
    [:db_insert_placeholder_1] => 380
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-10-20 09:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '380-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 380
    [:db_insert_placeholder_1] => 380
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-10-20 09:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '381' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 381
    [:db_insert_placeholder_1] => 381
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1471978514
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '381' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 381
    [:db_insert_placeholder_1] => 381
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1471978514
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '384-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 384
    [:db_insert_placeholder_1] => 384
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-08-09 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '384-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 384
    [:db_insert_placeholder_1] => 384
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-08-09 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '388-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 388
    [:db_insert_placeholder_1] => 388
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-10-05 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '388-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 388
    [:db_insert_placeholder_1] => 388
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-10-05 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '389-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 389
    [:db_insert_placeholder_1] => 389
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-10-06 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '389-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 389
    [:db_insert_placeholder_1] => 389
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-10-06 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '390-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 390
    [:db_insert_placeholder_1] => 390
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-10-12 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '390-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 390
    [:db_insert_placeholder_1] => 390
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-10-12 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '391' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 391
    [:db_insert_placeholder_1] => 391
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1475522164
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '391' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 391
    [:db_insert_placeholder_1] => 391
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1475522164
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '393-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 393
    [:db_insert_placeholder_1] => 393
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-10-28 10:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '393-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 393
    [:db_insert_placeholder_1] => 393
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-10-28 10:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '394-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 394
    [:db_insert_placeholder_1] => 394
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-11-14 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '394-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 394
    [:db_insert_placeholder_1] => 394
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-11-14 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '395-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 395
    [:db_insert_placeholder_1] => 395
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-11-16 09:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '395-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 395
    [:db_insert_placeholder_1] => 395
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2016-11-16 09:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '396' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 396
    [:db_insert_placeholder_1] => 396
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1475512476
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '396' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 396
    [:db_insert_placeholder_1] => 396
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1475512476
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '401' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 401
    [:db_insert_placeholder_1] => 401
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1480605532
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '401' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 401
    [:db_insert_placeholder_1] => 401
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1480605532
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '403-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 403
    [:db_insert_placeholder_1] => 403
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-01-23 08:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '403-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 403
    [:db_insert_placeholder_1] => 403
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-01-23 08:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '404-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 404
    [:db_insert_placeholder_1] => 404
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-06 09:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '404-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 404
    [:db_insert_placeholder_1] => 404
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-06 09:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '405-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 405
    [:db_insert_placeholder_1] => 405
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-20 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '405-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 405
    [:db_insert_placeholder_1] => 405
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-20 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '406' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 406
    [:db_insert_placeholder_1] => 406
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1489596228
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '406' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 406
    [:db_insert_placeholder_1] => 406
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1489596228
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '407-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 407
    [:db_insert_placeholder_1] => 407
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-04-06 08:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '407-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 407
    [:db_insert_placeholder_1] => 407
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-04-06 08:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '408-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 408
    [:db_insert_placeholder_1] => 408
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-05-16 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '408-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 408
    [:db_insert_placeholder_1] => 408
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-05-16 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '409-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 409
    [:db_insert_placeholder_1] => 409
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-07-11 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '409-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 409
    [:db_insert_placeholder_1] => 409
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-07-11 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '410-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 410
    [:db_insert_placeholder_1] => 410
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-08 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '410-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 410
    [:db_insert_placeholder_1] => 410
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-08 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '411' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 411
    [:db_insert_placeholder_1] => 411
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502122204
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '411' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 411
    [:db_insert_placeholder_1] => 411
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502122204
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '412-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 412
    [:db_insert_placeholder_1] => 412
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-08 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '412-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 412
    [:db_insert_placeholder_1] => 412
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-08 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '413-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 413
    [:db_insert_placeholder_1] => 413
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-08 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '413-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 413
    [:db_insert_placeholder_1] => 413
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-08 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '414-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 414
    [:db_insert_placeholder_1] => 414
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-06-11 12:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '414-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 414
    [:db_insert_placeholder_1] => 414
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-06-11 12:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '415-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 415
    [:db_insert_placeholder_1] => 415
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-04-13 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '415-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 415
    [:db_insert_placeholder_1] => 415
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-04-13 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '416' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 416
    [:db_insert_placeholder_1] => 416
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502122283
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '416' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 416
    [:db_insert_placeholder_1] => 416
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502122283
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '417-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 417
    [:db_insert_placeholder_1] => 417
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-01-22 15:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '417-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 417
    [:db_insert_placeholder_1] => 417
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-01-22 15:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '418-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 418
    [:db_insert_placeholder_1] => 418
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-06 15:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '418-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 418
    [:db_insert_placeholder_1] => 418
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-06 15:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '419-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 419
    [:db_insert_placeholder_1] => 419
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-07 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '419-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 419
    [:db_insert_placeholder_1] => 419
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-07 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '420-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 420
    [:db_insert_placeholder_1] => 420
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-27 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '420-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 420
    [:db_insert_placeholder_1] => 420
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-27 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '422-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 422
    [:db_insert_placeholder_1] => 422
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-05-03 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '422-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 422
    [:db_insert_placeholder_1] => 422
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-05-03 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '423-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 423
    [:db_insert_placeholder_1] => 423
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-04-26 10:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '423-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 423
    [:db_insert_placeholder_1] => 423
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-04-26 10:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '424-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 424
    [:db_insert_placeholder_1] => 424
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-10-04 10:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '424-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 424
    [:db_insert_placeholder_1] => 424
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-10-04 10:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '431' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 431
    [:db_insert_placeholder_1] => 431
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1486751652
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '431' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 431
    [:db_insert_placeholder_1] => 431
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1486751652
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '432-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 432
    [:db_insert_placeholder_1] => 432
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-09-11 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '432-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 432
    [:db_insert_placeholder_1] => 432
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-09-11 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '434-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 434
    [:db_insert_placeholder_1] => 434
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-09-25 09:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '434-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 434
    [:db_insert_placeholder_1] => 434
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-09-25 09:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '435-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 435
    [:db_insert_placeholder_1] => 435
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-09-12 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '435-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 435
    [:db_insert_placeholder_1] => 435
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-09-12 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '436' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 436
    [:db_insert_placeholder_1] => 436
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502481182
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '436' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 436
    [:db_insert_placeholder_1] => 436
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502481182
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '437-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 437
    [:db_insert_placeholder_1] => 437
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-09-14 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '437-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 437
    [:db_insert_placeholder_1] => 437
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-09-14 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '438-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 438
    [:db_insert_placeholder_1] => 438
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 288
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '438-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 438
    [:db_insert_placeholder_1] => 438
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 288
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '439-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 439
    [:db_insert_placeholder_1] => 439
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 63
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '439-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 439
    [:db_insert_placeholder_1] => 439
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 63
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '440-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 440
    [:db_insert_placeholder_1] => 440
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-23 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '440-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 440
    [:db_insert_placeholder_1] => 440
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-23 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '441' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 441
    [:db_insert_placeholder_1] => 441
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1489179015
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '441' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 441
    [:db_insert_placeholder_1] => 441
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1489179015
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '442-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 442
    [:db_insert_placeholder_1] => 442
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-29 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '442-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 442
    [:db_insert_placeholder_1] => 442
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-29 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '443-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 443
    [:db_insert_placeholder_1] => 443
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-30 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '443-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 443
    [:db_insert_placeholder_1] => 443
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-03-30 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '445-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 445
    [:db_insert_placeholder_1] => 445
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-04-18 09:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '445-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 445
    [:db_insert_placeholder_1] => 445
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-04-18 09:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '453-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 453
    [:db_insert_placeholder_1] => 453
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '453-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 453
    [:db_insert_placeholder_1] => 453
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 54
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '460-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information}  [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 460
    [:db_insert_placeholder_1] => 460
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '460-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_information} (entity_id, revision_id, bundle, delta, langcode,            [error]
field_course_information_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 460
    [:db_insert_placeholder_1] => 460
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 53
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '461' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 461
    [:db_insert_placeholder_1] => 461
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502985454
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '461' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 461
    [:db_insert_placeholder_1] => 461
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502985454
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '463-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 463
    [:db_insert_placeholder_1] => 463
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-12-13 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '463-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 463
    [:db_insert_placeholder_1] => 463
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-12-13 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '465-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 465
    [:db_insert_placeholder_1] => 465
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-10-03 10:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '465-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 465
    [:db_insert_placeholder_1] => 465
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-10-03 10:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '466' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 466
    [:db_insert_placeholder_1] => 466
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1504131285
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '466' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 466
    [:db_insert_placeholder_1] => 466
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1504131285
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '467-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 467
    [:db_insert_placeholder_1] => 467
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-10-17 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '467-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 467
    [:db_insert_placeholder_1] => 467
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-10-17 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '468-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 468
    [:db_insert_placeholder_1] => 468
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-10-19 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '468-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 468
    [:db_insert_placeholder_1] => 468
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-10-19 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '469-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 469
    [:db_insert_placeholder_1] => 469
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-10-18 08:30:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '469-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 469
    [:db_insert_placeholder_1] => 469
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-10-18 08:30:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '470-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date}          [error]
(entity_id, revision_id, bundle, delta, langcode, field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 470
    [:db_insert_placeholder_1] => 470
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-09-21 10:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '470-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_event_date} (entity_id, revision_id, bundle, delta, langcode,                    [error]
field_event_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 470
    [:db_insert_placeholder_1] => 470
    [:db_insert_placeholder_2] => events
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-09-21 10:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Processed 140 items (0 created, 0 updated, 140 failed, 0 ignored) - done with 'upgrade_d7_node_events'                                                                                                           [status]
Processed 0 items (0 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_node_jobs'                                                                                                                 [status]
Processed 0 items (0 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_node_news_item'                                                                                                            [status]
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '326' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 326
    [:db_insert_placeholder_1] => 326
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502121920
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '326' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 326
    [:db_insert_placeholder_1] => 326
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502121920
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Processed 3 items (0 created, 0 updated, 3 failed, 0 ignored) - done with 'upgrade_d7_node_page'                                                                                                                 [status]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '248-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 248
    [:db_insert_placeholder_1] => 248
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 185
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '248-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 248
    [:db_insert_placeholder_1] => 248
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 185
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '252-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 252
    [:db_insert_placeholder_1] => 252
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 155
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '252-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 252
    [:db_insert_placeholder_1] => 252
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 155
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '260-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 260
    [:db_insert_placeholder_1] => 260
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 163
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '260-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 260
    [:db_insert_placeholder_1] => 260
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 163
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '262-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 262
    [:db_insert_placeholder_1] => 262
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 165
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '262-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 262
    [:db_insert_placeholder_1] => 262
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 165
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '263-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 263
    [:db_insert_placeholder_1] => 263
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 166
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '263-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 263
    [:db_insert_placeholder_1] => 263
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 166
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '267-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 267
    [:db_insert_placeholder_1] => 267
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 170
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '267-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 267
    [:db_insert_placeholder_1] => 267
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 170
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '268-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 268
    [:db_insert_placeholder_1] => 268
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 171
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '268-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 268
    [:db_insert_placeholder_1] => 268
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 171
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '270-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 270
    [:db_insert_placeholder_1] => 270
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 238
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '270-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 270
    [:db_insert_placeholder_1] => 270
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 238
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '323-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 323
    [:db_insert_placeholder_1] => 323
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 181
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '323-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 323
    [:db_insert_placeholder_1] => 323
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 181
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '337-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 337
    [:db_insert_placeholder_1] => 337
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 186
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '337-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 337
    [:db_insert_placeholder_1] => 337
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 186
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '338-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 338
    [:db_insert_placeholder_1] => 338
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 187
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '338-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 338
    [:db_insert_placeholder_1] => 338
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 187
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '339-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 339
    [:db_insert_placeholder_1] => 339
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 188
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '339-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 339
    [:db_insert_placeholder_1] => 339
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 188
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '351' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 351
    [:db_insert_placeholder_1] => 351
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1484664269
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '351' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 351
    [:db_insert_placeholder_1] => 351
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1484664269
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '352-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 352
    [:db_insert_placeholder_1] => 352
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 190
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '352-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 352
    [:db_insert_placeholder_1] => 352
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 190
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '357-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 357
    [:db_insert_placeholder_1] => 357
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 191
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '357-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 357
    [:db_insert_placeholder_1] => 357
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 191
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '358-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 358
    [:db_insert_placeholder_1] => 358
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 192
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '358-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 358
    [:db_insert_placeholder_1] => 358
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 192
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '364-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 364
    [:db_insert_placeholder_1] => 364
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 193
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '364-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 364
    [:db_insert_placeholder_1] => 364
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 193
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '366' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 366
    [:db_insert_placeholder_1] => 366
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1484664401
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '366' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 366
    [:db_insert_placeholder_1] => 366
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1484664401
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '370-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 370
    [:db_insert_placeholder_1] => 370
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 195
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '370-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 370
    [:db_insert_placeholder_1] => 370
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 195
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '371' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 371
    [:db_insert_placeholder_1] => 371
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1484664477
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '371' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 371
    [:db_insert_placeholder_1] => 371
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1484664477
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '375-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 375
    [:db_insert_placeholder_1] => 375
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 198
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '375-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 375
    [:db_insert_placeholder_1] => 375
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 198
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '377-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 377
    [:db_insert_placeholder_1] => 377
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 200
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '377-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 377
    [:db_insert_placeholder_1] => 377
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 200
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '378-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 378
    [:db_insert_placeholder_1] => 378
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 202
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '378-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 378
    [:db_insert_placeholder_1] => 378
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 202
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '382-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 382
    [:db_insert_placeholder_1] => 382
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 203
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '382-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 382
    [:db_insert_placeholder_1] => 382
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 203
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '383-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 383
    [:db_insert_placeholder_1] => 383
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 205
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '383-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 383
    [:db_insert_placeholder_1] => 383
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 205
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '385-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 385
    [:db_insert_placeholder_1] => 385
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 206
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '385-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 385
    [:db_insert_placeholder_1] => 385
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 206
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '386' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 386
    [:db_insert_placeholder_1] => 386
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1484663999
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '386' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 386
    [:db_insert_placeholder_1] => 386
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1484663999
    [:db_insert_placeholder_4] => 1
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '387-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 387
    [:db_insert_placeholder_1] => 387
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 208
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '387-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 387
    [:db_insert_placeholder_1] => 387
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 208
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '392-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 392
    [:db_insert_placeholder_1] => 392
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 209
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '392-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 392
    [:db_insert_placeholder_1] => 392
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 209
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '397-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 397
    [:db_insert_placeholder_1] => 397
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 210
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '397-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 397
    [:db_insert_placeholder_1] => 397
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 210
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '398-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 398
    [:db_insert_placeholder_1] => 398
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 211
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '398-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 398
    [:db_insert_placeholder_1] => 398
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 211
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '399-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 399
    [:db_insert_placeholder_1] => 399
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 212
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '399-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 399
    [:db_insert_placeholder_1] => 399
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 212
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '400-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 400
    [:db_insert_placeholder_1] => 400
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 214
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '400-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 400
    [:db_insert_placeholder_1] => 400
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 214
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '402-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 402
    [:db_insert_placeholder_1] => 402
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 216
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '402-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 402
    [:db_insert_placeholder_1] => 402
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 216
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '425-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 425
    [:db_insert_placeholder_1] => 425
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 217
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '425-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 425
    [:db_insert_placeholder_1] => 425
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 217
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '426' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 426
    [:db_insert_placeholder_1] => 426
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1486585640
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '426' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 426
    [:db_insert_placeholder_1] => 426
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1486585640
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '427-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 427
    [:db_insert_placeholder_1] => 427
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 219
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '427-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 427
    [:db_insert_placeholder_1] => 427
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 219
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '428-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 428
    [:db_insert_placeholder_1] => 428
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 220
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '428-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 428
    [:db_insert_placeholder_1] => 428
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 220
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '429-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 429
    [:db_insert_placeholder_1] => 429
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 221
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '429-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 429
    [:db_insert_placeholder_1] => 429
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 221
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '430-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 430
    [:db_insert_placeholder_1] => 430
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 222
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '430-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 430
    [:db_insert_placeholder_1] => 430
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 222
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '446' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 446
    [:db_insert_placeholder_1] => 446
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1488986902
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '446' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 446
    [:db_insert_placeholder_1] => 446
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1488986902
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '447-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 447
    [:db_insert_placeholder_1] => 447
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 225
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '447-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 447
    [:db_insert_placeholder_1] => 447
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 225
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '448-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 448
    [:db_insert_placeholder_1] => 448
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 226
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '448-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 448
    [:db_insert_placeholder_1] => 448
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 226
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '449-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 449
    [:db_insert_placeholder_1] => 449
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 227
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '449-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 449
    [:db_insert_placeholder_1] => 449
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 227
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '450-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_non_staff_authors}   [error]
(entity_id, revision_id, bundle, delta, langcode, field_non_staff_authors_value, field_non_staff_authors_format) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2,
:db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6); Array
(
    [:db_insert_placeholder_0] => 450
    [:db_insert_placeholder_1] => 450
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => Tara L. Thomas
    [:db_insert_placeholder_6] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '450-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_non_staff_authors} (entity_id, revision_id, bundle, delta, langcode,             [error]
field_non_staff_authors_value, field_non_staff_authors_format) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5, :db_insert_placeholder_6); Array
(
    [:db_insert_placeholder_0] => 450
    [:db_insert_placeholder_1] => 450
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => Tara L. Thomas
    [:db_insert_placeholder_6] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '451' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 451
    [:db_insert_placeholder_1] => 451
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1496679245
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '451' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 451
    [:db_insert_placeholder_1] => 451
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1496679245
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '452-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 452
    [:db_insert_placeholder_1] => 452
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 230
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '452-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 452
    [:db_insert_placeholder_1] => 452
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 230
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '454-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 454
    [:db_insert_placeholder_1] => 454
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 231
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '454-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 454
    [:db_insert_placeholder_1] => 454
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 231
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '455-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 455
    [:db_insert_placeholder_1] => 455
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 232
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '455-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 455
    [:db_insert_placeholder_1] => 455
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 232
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '456' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 456
    [:db_insert_placeholder_1] => 456
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502473936
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '456' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 456
    [:db_insert_placeholder_1] => 456
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1502473936
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '457-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 457
    [:db_insert_placeholder_1] => 457
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 234
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '457-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 457
    [:db_insert_placeholder_1] => 457
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 234
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '458-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 458
    [:db_insert_placeholder_1] => 458
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 235
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '458-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 458
    [:db_insert_placeholder_1] => 458
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 235
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '459-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication_date}    [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 459
    [:db_insert_placeholder_1] => 459
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-11 00:00:00
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '459-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication_date} (entity_id, revision_id, bundle, delta, langcode,              [error]
field_publication_date_value) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 459
    [:db_insert_placeholder_1] => 459
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 2017-08-11 00:00:00
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '462-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 462
    [:db_insert_placeholder_1] => 462
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 239
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '462-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 462
    [:db_insert_placeholder_1] => 462
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 239
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '464-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1,
:db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 464
    [:db_insert_placeholder_1] => 464
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 240
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '464-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_publication} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_publication_target_id, field_publication_display, field_publication_description) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6, :db_insert_placeholder_7); Array
(
    [:db_insert_placeholder_0] => 464
    [:db_insert_placeholder_1] => 464
    [:db_insert_placeholder_2] => publications
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 240
    [:db_insert_placeholder_6] => 1
    [:db_insert_placeholder_7] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '471' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 471
    [:db_insert_placeholder_1] => 471
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1504131147
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '471' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 471
    [:db_insert_placeholder_1] => 471
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1504131147
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Processed 56 items (0 created, 0 updated, 56 failed, 0 ignored) - done with 'upgrade_d7_node_publications'                                                                                                       [status]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '328-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_address} (entity_id, [error]
revision_id, bundle, delta, langcode, field_address_value, field_address_format) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6); Array
(
    [:db_insert_placeholder_0] => 328
    [:db_insert_placeholder_1] => 328
    [:db_insert_placeholder_2] => staff_member
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => <p>2400 Old Ivy Road<br />Room 220<br />Charlottesville, VA 22903-4827</p>
    [:db_insert_placeholder_6] => full_html
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '328-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_address} (entity_id, revision_id, bundle, delta, langcode, field_address_value,  [error]
field_address_format) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5,
:db_insert_placeholder_6); Array
(
    [:db_insert_placeholder_0] => 328
    [:db_insert_placeholder_1] => 328
    [:db_insert_placeholder_2] => staff_member
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => <p>2400 Old Ivy Road<br />Room 220<br />Charlottesville, VA 22903-4827</p>
    [:db_insert_placeholder_6] => full_html
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '329-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_address} (entity_id, [error]
revision_id, bundle, delta, langcode, field_address_value, field_address_format) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6); Array
(
    [:db_insert_placeholder_0] => 329
    [:db_insert_placeholder_1] => 329
    [:db_insert_placeholder_2] => staff_member
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => <p>2400 Old Ivy Road<br />Room 220<br />Charlottesville, VA 22903-4827</p>
    [:db_insert_placeholder_6] => full_html
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '329-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_address} (entity_id, revision_id, bundle, delta, langcode, field_address_value,  [error]
field_address_format) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5,
:db_insert_placeholder_6); Array
(
    [:db_insert_placeholder_0] => 329
    [:db_insert_placeholder_1] => 329
    [:db_insert_placeholder_2] => staff_member
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => <p>2400 Old Ivy Road<br />Room 220<br />Charlottesville, VA 22903-4827</p>
    [:db_insert_placeholder_6] => full_html
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '330-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_address} (entity_id, [error]
revision_id, bundle, delta, langcode, field_address_value, field_address_format) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5, :db_insert_placeholder_6); Array
(
    [:db_insert_placeholder_0] => 330
    [:db_insert_placeholder_1] => 330
    [:db_insert_placeholder_2] => staff_member
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => <p>2400 Old Ivy Road<br />Rm 220<br />Charlottesville, VA 22903<br />&nbsp;</p>
    [:db_insert_placeholder_6] => full_html
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '330-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_address} (entity_id, revision_id, bundle, delta, langcode, field_address_value,  [error]
field_address_format) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5,
:db_insert_placeholder_6); Array
(
    [:db_insert_placeholder_0] => 330
    [:db_insert_placeholder_1] => 330
    [:db_insert_placeholder_2] => staff_member
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => <p>2400 Old Ivy Road<br />Rm 220<br />Charlottesville, VA 22903<br />&nbsp;</p>
    [:db_insert_placeholder_6] => full_html
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Processed 3 items (0 created, 0 updated, 3 failed, 0 ignored) - done with 'upgrade_d7_node_staff_member'                                                                                                         [status]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '52' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 52
    [:db_insert_placeholder_1] => 52
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455117180
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '52' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 52
    [:db_insert_placeholder_1] => 52
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455117180
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '53' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 53
    [:db_insert_placeholder_1] => 53
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045462
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '53' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 53
    [:db_insert_placeholder_1] => 53
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045462
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '54' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 54
    [:db_insert_placeholder_1] => 54
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455046167
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '54' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 54
    [:db_insert_placeholder_1] => 54
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455046167
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '55' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 55
    [:db_insert_placeholder_1] => 55
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455046467
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '55' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 55
    [:db_insert_placeholder_1] => 55
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455046467
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '58' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 58
    [:db_insert_placeholder_1] => 58
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045596
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '58' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 58
    [:db_insert_placeholder_1] => 58
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045596
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '59' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 59
    [:db_insert_placeholder_1] => 59
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045615
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '59' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 59
    [:db_insert_placeholder_1] => 59
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045615
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '60' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 60
    [:db_insert_placeholder_1] => 60
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045634
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '60' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 60
    [:db_insert_placeholder_1] => 60
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045634
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '62' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 62
    [:db_insert_placeholder_1] => 62
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045692
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '62' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 62
    [:db_insert_placeholder_1] => 62
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045692
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '63' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 63
    [:db_insert_placeholder_1] => 63
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045709
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '63' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 63
    [:db_insert_placeholder_1] => 63
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045709
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '64' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 64
    [:db_insert_placeholder_1] => 64
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045729
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '64' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 64
    [:db_insert_placeholder_1] => 64
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045729
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '65' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,       [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 65
    [:db_insert_placeholder_1] => 65
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455046262
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '65' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES            [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 65
    [:db_insert_placeholder_1] => 65
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455046262
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Entity\EntityStorageException: Update existing 'node' entity revision while changing the revision ID is not supported. in Drupal\Core\Entity\ContentEntityStorageBase->doPreSave() (line 309 of      [error]
/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/ContentEntityStorageBase.php).
Update existing 'node' entity revision while changing the revision ID is not supported. (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)                      [error]
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '245-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_type}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_type_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 245
    [:db_insert_placeholder_1] => 245
    [:db_insert_placeholder_2] => tav_course_descriptions
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 13
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '245-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_type} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_course_type_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 245
    [:db_insert_placeholder_1] => 245
    [:db_insert_placeholder_2] => tav_course_descriptions
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 13
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '288-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_type}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_type_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 288
    [:db_insert_placeholder_1] => 288
    [:db_insert_placeholder_2] => tav_course_descriptions
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 17
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '288-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_type} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_course_type_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 288
    [:db_insert_placeholder_1] => 288
    [:db_insert_placeholder_2] => tav_course_descriptions
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 17
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '292-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_type}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_type_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 292
    [:db_insert_placeholder_1] => 292
    [:db_insert_placeholder_2] => tav_course_descriptions
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 18
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '292-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_type} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_course_type_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 292
    [:db_insert_placeholder_1] => 292
    [:db_insert_placeholder_2] => tav_course_descriptions
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 18
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '293-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_type}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_type_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 293
    [:db_insert_placeholder_1] => 293
    [:db_insert_placeholder_2] => tav_course_descriptions
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 19
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '293-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_type} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_course_type_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 293
    [:db_insert_placeholder_1] => 293
    [:db_insert_placeholder_2] => tav_course_descriptions
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 19
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '334-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_type}         [error]
(entity_id, revision_id, bundle, delta, langcode, field_course_type_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3,
:db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 334
    [:db_insert_placeholder_1] => 334
    [:db_insert_placeholder_2] => tav_course_descriptions
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 20
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '334-0-0-und' for key 'PRIMARY': INSERT INTO {node__field_course_type} (entity_id, revision_id, bundle, delta, langcode,                   [error]
field_course_type_target_id) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 334
    [:db_insert_placeholder_1] => 334
    [:db_insert_placeholder_2] => tav_course_descriptions
    [:db_insert_placeholder_3] => 0
    [:db_insert_placeholder_4] => und
    [:db_insert_placeholder_5] => 20
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Drupal\Core\Database\IntegrityConstraintViolationException: SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '336' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode,      [error]
revision_timestamp, revision_uid, revision_log) VALUES (:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4,
:db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 336
    [:db_insert_placeholder_1] => 336
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045413
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 in Drupal\Core\Database\Connection->handleQueryException() (line 682 of /Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Database/Connection.php).
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '336' for key 'PRIMARY': INSERT INTO {node_revision} (nid, vid, langcode, revision_timestamp, revision_uid, revision_log) VALUES           [error]
(:db_insert_placeholder_0, :db_insert_placeholder_1, :db_insert_placeholder_2, :db_insert_placeholder_3, :db_insert_placeholder_4, :db_insert_placeholder_5); Array
(
    [:db_insert_placeholder_0] => 336
    [:db_insert_placeholder_1] => 336
    [:db_insert_placeholder_2] => und
    [:db_insert_placeholder_3] => 1455045413
    [:db_insert_placeholder_4] => 21
    [:db_insert_placeholder_5] =>
)
 (/Users/miles/Sites/devdesktop/8_4/core/lib/Drupal/Core/Entity/Sql/SqlContentEntityStorage.php:777)
Processed 20 items (0 created, 0 updated, 20 failed, 0 ignored) - done with 'upgrade_d7_node_tav_course_descriptions'                                                                                            [status]
Processed 9 items (9 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_node_title_label'                                                                                                          [status]
Processed 0 items (0 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_taxonomy_term_categorize_content'                                                                                          [status]
Processed 23 items (23 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_taxonomy_term_class_types'                                                                                               [status]
Processed 5 items (5 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_taxonomy_term_publication_series'                                                                                          [status]
Processed 9 items (9 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_taxonomy_term_publication_types'                                                                                           [status]
Processed 31 items (31 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_taxonomy_term_staff_authors'                                                                                             [status]
Processed 0 items (0 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_taxonomy_term_tags'                                                                                                        [status]
Processed 0 items (0 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_taxonomy_term_vocabulary_12'                                                                                               [status]
Processed 0 items (0 created, 0 updated, 0 failed, 0 ignored) - done with 'upgrade_d7_taxonomy_term_vocabulary_13'                                                                                               [status]
```
