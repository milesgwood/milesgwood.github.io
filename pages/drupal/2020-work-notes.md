---
layout: default
---

# Creating News Update Block

First I need to create a news update content type with a title, and picture.

Created the image field which links to the media.

I still need to figure out how I'm going to actually display the articles before I style them. Create a new section for the theme and add this block to that section of the theme.

Their images are
width 900
height 600

Make sure to use the m-0 and p-0 classes to get the images to display actual full width.


Their actual height varies between 320 and 420.

In the `theme.info.yml` file I added a new section `content_full_width: 'Full Width Content'`

Update `page--node.html.twig` to display the new region. I made the mistake of trying to add it to page.html.twig and that file was not outputting anything because page--node overrides it. The block examples are provided using hte page.html.twig file. The rest of the pages use the page--node.html.twig file.

```
{% if page.content_full_width %}
    {% block content_full_width %}
        {{ page.content_full_width}}
    {% endblock %}
{% endif %}
```

Now I can add blocks to that content section. I created a view that created a new block for that section.

```
block.block.views_block__news_updates_block_1
views.view.news_updates
core.entity_view_display.node.news_update.teaser
```

I want to make this block using twig and the grid of all blocks using react.

Working on custom text output for the view.

```
<a href="{{ view_node }}"><div class="grid-news-img-wrapper"><figure>{{ field_news_update_image }}</figure></div><div class="grid-news-content">{{ title }}</div></a>
```

Styling the view within the views module admin interface caused issues. Doesn't seem you can layer elements since they refer to each other. I can't put the image and title inside the link to content field.

Attempt 2 - Display the view using the teaser display of the News Update content type. Then customize the teaser twig for that specific file.

Copy the `node.html.twig` template from the bootstrap templates folder. Name it `node--news-update--teaser.html.twig`

## Retrieve the image field url

[Helpful](https://gbyte.co/blog/get-image-url-from-media-field-twig)

The only peice you need to change is the `field_news_update_image` part. The second `field_media_image` comes from the image being uploaded as a Image media type.


```
<img src="{{ file_url(node.field_news_update_image.entity.field_media_image.entity.fileuri) }}"/>
```

# CSS fucked up on PC browser - bootstrap not loading from CDN

Changed CDN provider to CDNJS from jsDeliver. That seems to have solved the local issue..

# Playing hero video on safari

Needed to add the `playsinline` attribute on `page--node.html.twig` I WAS LOOKING AT THE WRONG TEMPLATE FILE AGAIN

# Composer Updates Core 882-884

Prod is on 20200303-modules

Attempting to update everything except simplesaml and external_auth.

```
composer update --dry-run

- Updating psr/log (1.1.2) to psr/log (1.1.3)
- Updating doctrine/reflection (v1.1.0) to doctrine/reflection (1.2.0)
- Updating doctrine/persistence (1.3.6) to doctrine/persistence (1.3.7)
- Updating drupal/core (8.8.2) to drupal/core (8.8.4)
- Updating drupal/admin_toolbar (2.0.0) to drupal/admin_toolbar (2.2.0)
- Updating drupal/entity_reference_revisions (1.7.0) to drupal/entity_reference_revisions (1.8.0)
- Updating drupal/webform (5.8.0) to drupal/webform (5.9.0)
- Updating drupal/webform_ui (5.8.0) to drupal/webform_ui (5.9.0)
- Updating drupal/webform_templates (5.8.0) to drupal/webform_templates (5.9.0)
- Updating drupal/webform_node (5.8.0) to drupal/webform_node (5.9.0)
- Updating drupal/webform_devel (5.8.0) to drupal/webform_devel (5.9.0)
- Updating drupal/webform_bootstrap (5.8.0) to drupal/webform_bootstrap (5.9.0)
- Updating webmozart/assert (1.7.0) to webmozart/assert (1.5.0)
- Updating simplesamlphp/simplesamlphp (v1.18.4) to simplesamlphp/simplesamlphp (v1.18.5)
- Updating simplesamlphp/simplesamlphp-module-discopower (v0.9.1) to simplesamlphp/simplesamlphp-module-discopower (v0.9.3)
- Updating simplesamlphp/simplesamlphp-module-authorize (v0.9.1) to simplesamlphp/simplesamlphp-module-authorize (v0.9.2)
- Updating simplesamlphp/simplesamlphp-module-authfacebook (v0.9.2) to simplesamlphp/simplesamlphp-module-authfacebook (v0.9.3)
- Updating simplesamlphp/saml2 (v4.1.4) to simplesamlphp/saml2 (v4.1.7)
- Updating phpmailer/phpmailer (v6.1.4) to phpmailer/phpmailer (v6.1.5)
- Updating psy/psysh (v0.9.12) to psy/psysh (v0.10.2)
- Updating phpspec/prophecy (v1.10.2) to phpspec/prophecy (v1.10.3)

composer update
```

Copied the simplesaml 4 directories

Ran DB updates

# Config Workflow

[OST Training Paragraphs Tutorial](https://www.ostraining.com/blog/drupal/paragraphs-module/)

To make config work for you, you need to be focused on improving one specific site element at a time. You create a new paragraph to display flex grid cards. Then you export the config and take note of which files were changed. Then you know what to copy and sync into the other sites. You transfer it into another site and make sure that it is now working.

## Creating a new paragraph and transferring config

1. [Create New Paragraph Type](https://mediadev1.coopercenter.org/admin/structure/paragraphs_type/add)
2. Make all the fields unique with a prefix common to them all
3. [Enable the paragraph type on the Basic Page Additional Content - content type. ](https://mediadev1.coopercenter.org/admin/structure/types/manage/page/fields/node.page.field_paragraphs)
4. Test the new paragraph
5. Figure out what template you need to over ride
6. Customize the twig output
7. Style the twig output
8. Enable permissions for the new paragraph
9. Add the paragraph to any additonal Entity Reference sections like columns.
10. Run `drush config-export vcs` on the source site
11. Copy all of the config files listed that are exported into Atom
12. Create a new folder for this set of config imports
13. Copy the files you need into that new folder - `prepare_cofig_fileset_for_import.sh`
14. Modify the `import-set-of-config-files.sh` with the target site and the name of the folder you're importing
15. Import and test

# Drupal Config

`webform.webform.lead.application` - all webforms
`imce.settings`
`view.view.upcoming_classes` - all views but not the underlying content types are stored in these view config files
`field.field.node.page.field_paragraphs` - what additional paragraph types are allowed and viewable in the editor
`user.role.anonymous`- Permissions

HTML Editor

```
filter.format.full_html
editor.editor.full_html
filter.format.basic_html
editor.editor.basic_html
```

# VDOT Composer and Drush work

Global Composer install
```
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
export PATH="$HOME/.composer/vendor/bin:$PATH"
source ~/.bash_profile
composer global require drush/drush:dev-master
composer global update
drush --version
```

PHP memory limit

```
php -i | grep "memory_limit"
memory_limit => 128M => 128M
```

Temporarily increase memory limit
```
php -d memory_limit=512M /usr/local/bin/composer require drush/drush:~9
```

The symphont/filesystem package is causing problems so I want to remove that requirement I made and simply include dependencies in the update/require

On cloud9 I ran

```
composer self-update

Updating to version 1.9.2 (stable channel).
   Downloading (100%)         
Use composer self-update --rollback to return to version 1.8.0

composer remove symfony/filesystem --update-with-dependencies

php -d memory_limit=-1 /home/uvacooper/.c9/node/bin/composer remove symfony/filesystem --update-with-dependencies

php -d memory_limit=-1 /home/uvacooper/.c9/node/bin/composer require drush/drush:9.7.1 --update-with-dependencies

drush config-import -y --partial --source=modules/custom/vdot_user_csv_migration/config/install
```

Then use the gui to actually run the migration.

# phpStorm Setup

### 1
 [Follow Acquia Tutorial on PhPStorm Setup](https://docs.acquia.com/dev-desktop/sites/phpstorm/)

In your current php.ini 7.2 make sure that this line has the semicolon at the beginning removed

`zend_extension="W:\acquia\stack\php7_2_x64\ext\php_xdebug.dll"`

Then we can check for xdebug by visiting this page `/admin/reports/status/php`

I see xdebug version 2.6.0 but I do not see a IDE key. I also see that xdebug.remote_enable is turned off as well. We need to remedy that by adding the following to php.ini

`xdebug.remote_enable=1`

Then restart and check the php info page again. Now the `xdebug.remote_enable` is set to On

### 2

I let phpstorm configure windows defender to exclude my project directories from real time scanning.

### 3

Check the Event Log which shows you issues at the bottom of the screen.

I clicked enable drupal support. It asks for the drupal root directory. In this case that is the learn dir, which has modules and sites inside of it.

Fix
I set drupal style formatting.

Fix
.test, .install, .engine, .profile, .theme files are not associated with PHP file type.

Fix
.info files are not associated with Ini file type.

### Step 4

- Debugging with Dev Desktop

Enable PHPStorm to debug Acquia Dev desktop

Settings > Languages and Frameworks > PHP > Debug

Enable Listening for PHP Debug Connections

This makes teh phone appear in the top right of the menu. You want the debug to be green and have the 3 lines coming out of the phone.

Can Accept External Connections
Debug port to 9000

- Setup PHPStrom with debugger

Run> Edit Configurations

New PHP Remote Debug Configuration

Add a Name that means something

Add a New Server

Host: http://learn.dd
Port: 8083
Debugger: Xdebug

Apply

Just for a test I am setting the debug to Break at first line in PHP script. Settings > Lang > PHP >Debug

So I need to have the chrome debugger tool installed. Then I just make sure that PHPStorm is listening and do something on the website while the chrome debug helper is live.

Set the PHP level to 7.2 which matches current DevDesk.

Alt+Ctrl+S + Languages and Frameworks > PHP Set PHP Language Level dropdown

The .idea folder tracks all of your project settings. You should track that in version control.

To improve performance you can tell phpstorm what directories to index and what directories to ignore. You go to settings ctrl+alt+s and in the directories tab setup the Sources folder.
