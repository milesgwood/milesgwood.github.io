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

# Play Button on Hero Video

[tutorial](https://blog.teamtreehouse.com/building-custom-controls-for-html5-videos)

Edit `page--node.html.twig` to add in the video controls.

```
<div class="hero-container">
    <div class="hero_overlay"></div>
    <video id="hero-video" autoplay loop muted playsinline class="hero-bg">
        <source src="{{ node.field_hero_video_direct_link.value }}" type="video/mp4" alt="HTML5 background video">
    </video>
    <div id="hero-controls">
        <a title="Pause/Unpause Video" aria-label="Pause/Unpause Video" class="btn btn-link">
            <span class="glyphicon glyphicon-play-circle"></span>
            <span class="glyphicon glyphicon-pause"></span>
        </a>
    </div>
</div>
```

[Convert tabs to spaces when sass compile breaks](https://tabstospaces.com/)

# Demographics Sync Config

Group altered config into a folder.

```
"block.block.views_block__news_updates_block_1"
"block.block.views_block__news_updates_full_grid_block_1"
"core.entity_form_display.node.news_update.default"
"core.entity_form_display.paragraph.flex_grid.default"
"core.entity_form_display.paragraph.flex_grid_1_4.default"
"core.entity_form_display.paragraph.flex_grid_child.default"
"core.entity_form_display.paragraph.remote_video.default"
"core.entity_form_display.paragraph.spotlight.default"
"core.entity_view_display.node.news_update.default"
"core.entity_view_display.node.news_update.teaser"
"core.entity_view_display.paragraph.flex_grid.default"
"core.entity_view_display.paragraph.flex_grid_1_4.default"
"core.entity_view_display.paragraph.flex_grid_child.default"
"core.entity_view_display.paragraph.remote_video.default"
"core.entity_view_display.paragraph.spotlight.default"
"editor.editor.basic_html"
"editor.editor.full_html"
"field.field.media.audio.field_media_audio_file"
"field.field.media.file.field_media_file"
"field.field.media.image.field_media_image"
"field.field.media.video.field_media_video_file"
"field.field.node.news_update.body"
"field.field.node.news_update.field_news_update_additional_con"
"field.field.node.news_update.field_news_update_image"
"field.field.node.page.field_paragraphs"
"field.field.paragraph.bp_columns.bp_column_content"
"field.field.paragraph.bp_columns_two_uneven.bp_column_content_2"
"field.field.paragraph.flex_grid.field_flex_grid_child"
"field.field.paragraph.flex_grid_1_4.field_flex_grid_child"
"field.field.paragraph.flex_grid_child.field_flex_body"
"field.field.paragraph.flex_grid_child.field_flex_body"
"field.field.paragraph.flex_grid_child.field_flex_child"
"field.field.paragraph.flex_grid_child.field_flex_image"
"field.field.paragraph.flex_grid_child.field_flex_link"
"field.field.paragraph.remote_video.field_youtube_video"
"field.field.paragraph.spotlight.field_spotlight_background_color"
"field.field.paragraph.spotlight.field_spotlight_body"
"field.field.paragraph.spotlight.field_spotlight_image"
"field.field.paragraph.spotlight.field_spotlight_link"
"field.field.paragraph.spotlight.field_spotlight_section_title"
"field.storage.media.field_media_audio_file"
"field.storage.media.field_media_file"
"field.storage.media.field_media_image  "
"field.storage.media.field_media_video_file"
"field.storage.node.field_news_update_additional_con"
"field.storage.node.field_news_update_image"
"field.storage.paragraph.bp_column_content"
"field.storage.paragraph.bp_column_content_2"
"field.storage.paragraph.field_flex_body"
"field.storage.paragraph.field_flex_child"
"field.storage.paragraph.field_flex_grid_child"
"field.storage.paragraph.field_flex_image"
"field.storage.paragraph.field_flex_link"
"field.storage.paragraph.field_spotlight_background_color"
"field.storage.paragraph.field_spotlight_body"
"field.storage.paragraph.field_spotlight_image"
"field.storage.paragraph.field_spotlight_link"
"field.storage.paragraph.field_spotlight_section_title"
"field.storage.paragraph.field_youtube_video"
"filter.format.basic_html"
"filter.format.full_html"
"node.type.news_update"
"paragraphs.paragraphs_type.flex_grid"
"paragraphs.paragraphs_type.flex_grid_1_4"
"paragraphs.paragraphs_type.flex_grid_child"
"paragraphs.paragraphs_type.remote_video"
"paragraphs.paragraphs_type.spotlight"
"views.view.news_updates"
"views.view.news_updates_full_grid"
"views.view.pages_with_advanced_html"
```

Move your cloud9 to tab 1 so you can use `ctrl 1` to get to it quickest.

Export current Demographics Site config

drush config-export vcs -y

Copy over the config you wish to change and commit changes to git.

Fix all of the pages that have FULL HTML sections `/advanced-pages`

Fix all the /advanced-sections that need updating.

# Demographics Testing Site Element Creation

```
drush export vcs -y
branch 20200407
```

[Login](https://demographicsdev1.coopercenter.org/user/login)
Username is test

Search `create basic page`

Enter Dummy Text

[Publish Page](https://demographicsdev1.coopercenter.org/editor/test)

Add a custom small banner of dimensions 1600x300 with custom class as `banner--top-replace`


### Permission Changes

1. Prune extra text formats - search `text formats`


# Substitute Top Banner - Tutorial needed

You add the banner to Additional content with custom class `banner--top-replace`

The banner needs to be 1600x300

This works on demographics site because of this javascript

```
  function replace_large_banner(e) {
        var url = $(".banner--top-replace").css("background-image");
        $(".main-container .page-title-wrapper").css("background-image", url);
    }
```

You can not do this on the homepage!

Examples
https://demographics.coopercenter.org/maps
https://media.coopercenter.org/web/top-banner

# Report Website Problem Link

[Add Link to Admin Menu](https://demographicsdev1.coopercenter.org/admin/structure/menu/manage/admin/add?destination=/admin/structure/menu/manage/admin)

Settings

Report Website Problem
https://support.coopercenter.org/saml_login
Check Enabled and Expanded
Help improve our sites by reporting a website problem
--Administration
Weight 11

# Hero Tagline Edge fix

width: fit-content on chrome and firefox is solved by `display: table` on edge.

# Discard local modifications in git for one file

`git checkout -- filename`

# Remote Link News Update

Created new field `field_news_update_external_link`

Edit `node--news-update--teaser.html.twig`

[Get twig values](https://blog.usejournal.com/getting-drupal-8-field-values-in-twig-22b80cb609bd)

The check to see if the field is empty occurs on the **node** variable but while accessing the external link URL I use the **content** variable. Why?

The node is the render array element.

```
{% if node.field_news_update_external_link is not empty%}
  <a class="news-update-container external bounce-on-hover" href="{{ content.field_news_update_external_link.0['#url'] }}"  rel="bookmark">
    <div class="news-update-img-wrapper">
      <figure><img src="{{ file_url(node.field_news_update_image.entity.field_media_image.entity.fileuri) }}"/></figure>
    </div>
    <div class="news-update-content"><h2>{{ label }}</h2></div>
  </a>
{% else %}
  <a class="news-update-container bounce-on-hover" href="{{ url }}" rel="bookmark">
    <div class="news-update-img-wrapper">
      <figure><img src="{{ file_url(node.field_news_update_image.entity.field_media_image.entity.fileuri) }}"/></figure>
    </div>
    <div class="news-update-content"><h2>{{ label }}</h2></div>
  </a>
{% endif %}
```

# Employee Specific News Updates

On Demographcis site, I used a Contextual filter on the News Update view.

`Configure contextual filter: Content: Related Employee Profiles (field_related_employee_profiles)`

The related employee profiles field is on the News Items that I want tied to the profile. When the filter value is not available a default value is provided from the `Content ID from URL`. So if the News Update `A` has Profile `B` listed as a related profile, A will show B.

This is one of those rare occasions when drupal is actually satisfying.

# Sorensen config first attempt

The import failed due to the following reasons:

The Basic Page content type on demographics has a file attachment field that needs to get deleted. Sorensen lacked a Editor site role. Those two issues were the only things stopping the config sync from working.

# Support Site Config sync

Export current support site config. `drush config-export vcs`

Enabled Media and Media Library modules.

The import failed due to the following reasons:

Missing Profile Content type `large-support` created

```
"node.type.profile"
"media.type.file"
"field.storage.node.field_profile_facebook"
"field.storage.node.field_profile_linkedin"
"field.storage.node.field_profile_twitter"
```

# Support Site News Updates Continued

Remove all sorensen staff user roles.

Get all permissions onto the Editor role. Delete the Sorensen Staff role.

Use git diff on the updated `user.editor.role.yml`

Current editor permissions filtered through sorensen.

```
uuid: 6964f504-baf0-4031-8b73-ec6ec39042ab
langcode: en
status: true
dependencies: {  }
id: editor
label: Editor
weight: 3
is_admin: null
permissions:
  - 'access administration pages'
  - 'access comments'
  - 'access content overview'
  - 'access files overview'
  - 'access in-place editing'
  - 'access media overview'
  - 'access shortcuts'
  - 'access taxonomy overview'
  - 'access toolbar'
  - 'access tour'
  - 'access user contact forms'
  - 'access user profiles'
  - 'access webform overview'
  - 'access webform submission log'
  - 'administer google analytics'
  - 'administer imce'
  - 'administer menu'
  - 'administer nodes'
  - 'administer shortcuts'
  - 'administer taxonomy'
  - 'administer url aliases'
  - 'administer webform'
  - 'administer webform element access'
  - 'administer webform submission'
  - 'change own username'
  - 'clone news_item content'
  - 'clone news_update content'
  - 'clone page content'
  - 'clone profile content'
  - 'clone publications content'
  - 'create audio media'
  - 'create file media'
  - 'create image media'
  - 'create media'
  - 'create news_item content'
  - 'create news_update content'
  - 'create page content'
  - 'create profile content'
  - 'create publications content'
  - 'create remote_video media'
  - 'create url aliases'
  - 'create video media'
  - 'create webform'
  - 'customize shortcut links'
  - 'delete all revisions'
  - 'delete any audio media'
  - 'delete any downloadable content'
  - 'delete any file media'
  - 'delete any image media'
  - 'delete any image_attribution content'
  - 'delete any media'
  - 'delete any news_item content'
  - 'delete any news_update content'
  - 'delete any page content'
  - 'delete any person content'
  - 'delete any profile content'
  - 'delete any publications content'
  - 'delete any remote_video media'
  - 'delete any video media'
  - 'delete any web_content content'
  - 'delete any webform content'
  - 'delete any webform submission'
  - 'delete media'
  - 'delete own audio media'
  - 'delete own downloadable content'
  - 'delete own file media'
  - 'delete own image media'
  - 'delete own image_attribution content'
  - 'delete own news_item content'
  - 'delete own news_items content'
  - 'delete own news_update content'
  - 'delete own page content'
  - 'delete own person content'
  - 'delete own profile content'
  - 'delete own publications content'
  - 'delete own remote_video media'
  - 'delete own video media'
  - 'delete own web_content content'
  - 'delete own webform'
  - 'delete own webform content'
  - 'delete own webform submission'
  - 'delete webform submissions own node'
  - 'edit any audio media'
  - 'edit any file media'
  - 'edit any image media'
  - 'edit any news_item content'
  - 'edit any news_items content'
  - 'edit any news_update content'
  - 'edit any page content'
  - 'edit any person content'
  - 'edit any profile content'
  - 'edit any publications content'
  - 'edit any remote_video media'
  - 'edit any video media'
  - 'edit any webform'
  - 'edit any webform submission'
  - 'edit own audio media'
  - 'edit own downloadable content'
  - 'edit own file media'
  - 'edit own image media'
  - 'edit own image_attribution content'
  - 'edit own news_item content'
  - 'edit own news_items content'
  - 'edit own news_update content'
  - 'edit own page content'
  - 'edit own person content'
  - 'edit own profile content'
  - 'edit own publications content'
  - 'edit own remote_video media'
  - 'edit own video media'
  - 'edit own webform'
  - 'edit own webform content'
  - 'edit own webform submission'
  - 'edit webform submissions any node'
  - 'edit webform submissions own node'
  - 'link to any page'
  - 'revert all revisions'
  - 'revert news_item revisions'
  - 'revert news_items revisions'
  - 'revert news_update revisions'
  - 'revert page revisions'
  - 'revert person revisions'
  - 'revert profile revisions'
  - 'revert publications revisions'
  - 'revert webform revisions'
  - 'skip CAPTCHA'
  - 'switch shortcut sets'
  - 'update any media'
  - 'update media'
  - 'use admin toolbar search'
  - 'use text format basic_html'
  - 'view all media revisions'
  - 'view all revisions'
  - 'view any webform submission'
  - 'view news_item revisions'
  - 'view news_update revisions'
  - 'view own unpublished media'
  - 'view own webform submission'
  - 'view page revisions'
  - 'view person revisions'
  - 'view profile revisions'
  - 'view publications revisions'
  - 'view the administration theme'
  - 'view unpublished paragraphs'
  - 'view webform revisions'
  - 'view webform submissions any node'
  - 'view webform submissions own node'
```

Accidentally deleted a view that depended on the Sorensen Staff role. I purged the old config and replaced the role with the editor restriction.

I checked what else could have been deleted by going through the role delete dialog on the prod site. All is well.

Exporting Sorensen Config

`field.field.node.news_update.field_category` includes two different taxonomies for the news update field. I need to change that in config before importing it to ta new file.

Config before adding hero video

```
"field.field.node.news_update.field_category"
"field.field.node.news_update.body"
"field.storage.node.field_category"
"taxonomy.vocabulary.category"
"core.entity_form_display.node.news_update.default"
"core.entity_view_display.node.news_update.default"
"core.entity_view_display.node.news_update.teaser"
"block.block.sorensensocialmedialinksforhomepage"
```

Updated advanced pages view to sort by last modification. Also made the news update view show promoted items first.

```
"views.view.news_updates"
"views.view.pages_with_advanced_html"
```

# Support Form JSON Data

```
json:
  key:
  token:
  pos: top
  due: null
  idList: 5ab160ed2e906a4f06871e9b
  name: milesgwood@virginia.edu
  i_want_to_: 'Request Training & Assistance'
  url_of_page_you_want_edited: null
  how_urgent_is_this_request_: 'Not Urgent'
  video_of_problem: null
  screenshot_of_problem: null
  desc: test
  idLabels: 5ab15ec14b8e8a87d266d7dd
  uri: /request/sorensen
  ```

# Add loading icon to video and screenshot section of support form

Inside the label add a div with the spinner class

Upload Video/ Screenshot then <div class="loader"></div>

jQuery(".js-webform-image-file label").append("<div class='loader'></div>");
jQuery(".js-webform-video-file label").append("<div class='loader'></div>");

```
(function($, document, window) {

    function addLoadingSpinner(inputFile) {
  inputFile.append("<div class='loader'></div>");
}

$("#edit-screenshot-of-problem-upload-button--2").change(function(){
      var inputImage= $(".js-webform-image-file label");
      addLoadingSpinner(inputImage);
      console.log("Screenshot Upload Start");
 });

 $("#edit-video-of-problem-upload-button--2").change(function(){
       var inputVideo = $(".js-webform-video-file label")
       addLoadingSpinner(inputVideo);
       console.log("Video Upload Start");
  });

})(jQuery, document, window);
```

# Solar New Updates

Config that comes from solar to next site:

This allows for imce file uploads.

```
core.entity_form_display.paragraph.bp_image.default
```

# CEPS News updates

The changes to make the IMCE file manager appear on image selections needs the caption field as well

```
field.field.paragraph.bp_image.field_caption
field.storage.paragraph.field_caption
```

Got two errors on config import but it still worked

```
A non-existent config entity name returned by FieldStorageConfigInterface::getBundles(): entity type: taxonomy_term, bundle: local_option_sales_tax, field name: field_schooldivnum

Drupal\Core\Field\FieldException: Attempt to create a field field_hero_video_direct_link that does not exist on entity type node. in Drupal\field\Entity\FieldConfig->getFieldStorageDefinition() (line 312 of /mnt/gfs/uvacooperdev/livedev/docroot/core/modules/field/src/Entity/FieldConfig.php).
```

Unable to add user role to multiple Users at once. Look into this `system.action.user_add_role_action.site_manager` and `system.action.user_remove_role_action.site_manager`

but with the editor role

Unable to add user role to multiple Users at once. Look into this `system.action.user_add_role_action.editor` and `system.action.user_remove_role_action.editor`

# CSR News Update

Made minor changes to editor permissions to allow for CSR Projects content type.

Not having profile picture on the slider makes it so that the following images don't all load!

Improved the News Updates view so that it works with individual profiles and individuals can hide their content from the front page view.

`block.block.coopercenter_units_local_tasks.yml`

Determines where your tabs show up (view edit clone delete etc.) and what region they are in.

`field.field.paragraph.spotlight.field_spotlight_image`

Added description to the image portion explaining how to edit the pictures. I created a page for the tutorial to exist in. [Direct Link](https://support.coopercenter.org/photo-editing)



Copied all of these files from CSR to master set of config. They make the IMCE actually work for the specific image types people need.

```
"block.block.coopercenter_units_local_tasks"
"field.field.paragraph.spotlight.field_spotlight_image"
"views.view.news_updates"
"imce.profile.member"
"imce.settings"
"field.storage.paragraph.field_image"
"field.field.paragraph.banner.field_image"
"field.field.paragraph.flex_grid_child.field_flex_image"
```

# VIG - News Updates

Clone from prod.

`image.style.media_library` prevented the config sync. I exported current config, deleted that config file and imported the change with the deleted config. Then I enabled the media library.

#SEI and LEAD News Update

`image.style.media_library` is already in active config. Need to export and delete for both sites. I'm doing the news updates at the same time for each site.

#BeHeardCVA - News Udpate

This News Update is different since the site is on a different theme. I'll need to copy over the template files from cooper center units.

Sent update to Tom and Kara about site updates coming. They haven't logged on in two weeks so I doubt they needed the notification.

## Transferring twig files for Spotlight and News Updates

Here are all the files I identified as needed - they are in a folder called `new-twig-elements`

```
new file:   new-twig-elements/block--photo-slider-flow.html.twig
new file:   new-twig-elements/block--photo-slider.html.twig
new file:   new-twig-elements/block--profileslider.html.twig
new file:   new-twig-elements/field--field-flex-grid-child.html.twig
new file:   new-twig-elements/field--field-hero-video-link.html.twig
new file:   new-twig-elements/field--node--field-additional-links--profile.html.twig
new file:   new-twig-elements/field--node--field-high-quality-headshot.html.twig
new file:   new-twig-elements/field--node--field-profile-facebook--profile.html.twig
new file:   new-twig-elements/field--node--field-profile-linkedin--profile.html.twig
new file:   new-twig-elements/field--node--field-profile-twitter--profile.html.twig
new file:   new-twig-elements/node--news-update--teaser.html.twig
new file:   new-twig-elements/node--profile.html.twig
new file:   new-twig-elements/page--node.html.twig
new file:   new-twig-elements/paragraph--flex-grid-child.html.twig
new file:   new-twig-elements/paragraph--flex-grid.html.twig
new file:   new-twig-elements/paragraph--flex-grid_1_4.html.twig
new file:   new-twig-elements/paragraph--spotlight.html.twig
```

Templates are working without the CSS. However the NU views aren't displaying because there is no block region for them to display.

I added the content full width region to the theme.info file. It doesn't have the views in it though. I will import the views again from config.

Each block has a theme field in it for example this NU block of 12 which i changed to beheardcva in 2 locations.

```
uuid: 50593de6-9577-4e1d-9323-be3a83612d7f
langcode: en
status: true
dependencies:
  config:
    - views.view.news_updates_full_grid
  module:
    - system
    - views
  theme:
    - beheardcva
id: views_block__news_updates_full_grid_block_1
theme: beheardcva
region: cfw
weight: -16
provider: null
plugin: 'views_block:news_updates_full_grid-block_1'
settings:
  id: 'views_block:news_updates_full_grid-block_1'
  label: ''
  provider: views
  label_display: '0'
  views_label: ''
  items_per_page: none
visibility:
  request_path:
    id: request_path
    pages: "/web/news-grid\r\n/test/news-updates\r\n/all-news-updates"
    negate: false
    context_mapping: {  }
```

In Cloud9 there is a refactor option for twig config files. `Ctrl+Shift+F` or find in files. It searches whatever directory you select and offers a replace option.

I searched all the beheardcva config files for `theme: coopercenter_units` and replaced it with `theme: beheardcva`. There is still the issue of the dependencies being incorrect.

Deleting the ` config/beheardcva/block.block.coopercenter_units...` files from config gets rid of the duplicate blocks.

CSS compared core to style and got rid of quite a bit of un-needed css.

# Demographics News Update tutorial

Create 2 news updates and log the process, then make the tutorial.

Start at account login page.
Find the external page you want to share.
Decide on a photo
Copy the title
Copy the external link

Created video. Make sure to limit the scope of the videos you are creating. Keep them small. No larger than 5 minutes.

# Support Site Private Files Directory

[acquia docs on setting private file path](https://support.acquia.com/hc/en-us/articles/360005307793-Setting-the-private-file-directory-on-Acquia-Cloud)

I need to use environment variables to set the private file path. Looks like it is already set as it needs to be. The files just aren't being served from the private folder.

The strategic plan is being served from this url:

https://support.coopercenter.org/system/files/media/files/2020-04/StrategicPlan_FullDigitalVersion.pdf

[File system config](https://support.coopercenter.org/admin/config/media/file-system) says that the private file path is `/mnt/files/uvacooper.prod/sites/support/files-private`

I just changed the default download method to Private local files served by Drupal to see if that changes the access control.

Still have full access to the file I uploaded before the radio button switch of "default download method".

I also changed the file path on the Files media content type to include the word private in it so I can tell if the filepath has actually changed. It has

https://support.coopercenter.org/system/files/private/media/files/2020-04/test1.docx

Now it is working!!!

To summarize

1. On [File System Config](/admin/config/media/file-system) set the Default Download method to Private local files served by drupal.
2. On the File field of the File Media type set the field visibility to custom permissions with only authenticated users being allowed to view the values of the field.
3. Click the field settings tab of that field and set the upload destination to Private Files.
4. Upload a test file and copy the direct link. Then logout and attempt to view the file again.
5. Make sure that you can access the directories through the imce file browser so you can delete files.

# News Updates - fix view of two on homepage

Changed the sort for news updates - promoted needs to be `descending` not ascending. Promoted being selected puts it at a 1. Promoted not being selected puts it at a 0.

# Sorensen Config Changes for Board Members

```
field.storage.node.field_profile_position_on_board                         | Create
field.storage.node.field_profile_is_board_member                           | Create
field.storage.node.field_profile_alumni_program                            | Create
field.storage.node.field_board_member_location                             | Create
field.field.node.profile.field_profile_position_on_board                   | Create
field.field.node.profile.field_profile_is_board_member                     | Create
field.field.node.profile.field_profile_alumni_program                      | Create
field.field.node.profile.field_board_member_location                       | Create
block.block.photosliderflowboardmembercustomblockuseforboardmemberprofiles | Create
core.extension                                                             | Update
field.field.node.profile.field_profile_email                               | Update
core.entity_form_display.node.profile.default                              | Update
core.entity_view_display.node.profile.teaser                               | Update
core.entity_view_display.node.profile.default                              | Update
views.view.profile_contact_info_table                                      | Update
```

All of these config entries got slightly changed in this config update for sorensen.

Create alternate Admin account for Amy to use while I am away. - Done

# Fix .htaccess in config directories

```
Security warning: Couldn't write .htaccess file. Please create a .htaccess file in your /mnt/www/html/uvacooper.prod/config/vig directory which contains the following lines:
# Deny all requests from Apache 2.4+.
<IfModule mod_authz_core.c>
  Require all denied
</IfModule>

# Deny all requests from Apache 2.0-2.2.
<IfModule !mod_authz_core.c>
  Deny from all
</IfModule>

# Turn off all options we don't need.
Options -Indexes -ExecCGI -Includes -MultiViews

# Set the catch-all handler to prevent scripts from being executed.
SetHandler Drupal_Security_Do_Not_Remove_See_SA_2006_006
<Files *>
  # Override the handler again if we're run later in the evaluation list.
  SetHandler Drupal_Security_Do_Not_Remove_See_SA_2013_003
</Files>

# If we know how to do it safely, disable the PHP engine entirely.
<IfModule mod_php5.c>
  php_flag engine off
</IfModule>
<IfModule mod_php7.c>
  php_flag engine off
</IfModule>
```

# FireEye Randsomware

IPs listed in the report

128.143.86.3 - cncHost - demographics.virginia.edu
52.109.2.30 - seems to be where the malware came from

IP addresses from dig

128.143.86.3 - demographics.virginia.edu
128.143.21.137 - statchatva.org
52.216.105.90 - racialdotmap.demographics.coopercenter.org
52.87.30.162 - demographics.coopercenter.org

104.26.10.156 and 104.26.11.156 - api.rss2json.com

Here's what I think is happening:

demographics.virginia.edu is IP 128.143.86.3 which is what appears in the log.
demographics.virginia.edu is the old site prior to the drupal 8 migration. We can just turn that off.

# Code updates

Needed to check media and support site. JUST CHECK SUPPORT
ctools 3.4
colorbox 1.6
image_widget_crop 2.3
imce 2.2
pathauto 1.8
token 1.7
views_data_export 1.0-rc1
webform 5.11

THIS ONE WAS MISSING FROM MEDIA

redirect_after_login

composer require 'drupal/imce:^2.2'

keep externalauth 1.1
keep simplesamlauth 3.2

# Font changes

font-family: adobe-caslon-pro", serif;

font-family: franklin-gothic-urw, wingdings;

Added fonts using adobe fonts:


Added the html.html.twig

<link rel="stylesheet" href="https://use.typekit.net/giv7wwf.css">

# Converting lots of mov to mp4

```
for i in *.mov;
  do name=`echo "$i" | cut -d'.' -f1`
  echo "$name"
  ffmpeg -i "$i" "${name}.mp4"
done
```


# Set spotlight section height through JS

Get the height of the right side image
jQuery("#spotlight-img").css("height")

Set the height of the text section
jQuery("#spotlight").css("height", "600px")

In 2 lines
var spotlight-img = $("#spotlight-img").css("height");
$("#spotlight").css("height", spotlight-img);

In one line
jQuery("#spotlight").css("height", jQuery("#spotlight-img").css("height"));
$("#spotlight").css("height", $("#spotlight-img").css("height"));

# Validate custom form data for CEPS LOST data

[Drupalize Me Tutorial](https://drupalize.me/tutorial/validate-form-form-controller?p=2766)

Within the Controller for my LOST form, I want to add some validation code.

`/docroot/modules/custom/lost_to_csv/src/Controller/LostToCsv.php`


```php
/**
* Implements form validation.
*
* @param array $form
*   The render array of the currently built form.
* @param \Drupal\Core\Form\FormStateInterface $form_state
*   Object describing the current state of the form.
*/
public function validateForm(array &$form, FormStateInterface $form_state) {
$submission = $form_state->getValue('text');

// Check that submission is of type string
if(gettype($submission) != 'string'){
    $form_state->setErrorByName('text', $this->t('Submission was not a text string.'));
}

if (strlen($submission) < 10){
    $form_state->setErrorByName('text', $this->t('Submission was too short, please fill out the field as described.'));
}


// Split up the lines of the submission into an array called $lost
$lost = str_getcsv($submission, "\n");

// Make sure the top line is in the correct format and that it exists
if($lost[0] == "month,year,tax,locality"){
    array_shift($lost);
}
else{
    $form_state->setErrorByName('text', $this->t('We have an error on the first line of your submission. Make sure the fields are in the right order and there are no trailing commas.<br>Error: <code>' . $lost[0] . '</code><br>Correct Format: <code>month,year,tax,locality</code>'));
}

if(gettype($lost) != 'array'){
    $form_state->setErrorByName('text', $this->t('Error in processing form input. Lost field not parsed as an array.'));
}

// Deal with each line one at a time
foreach ($lost as $line){
    $lost_fields = explode(",", $line); //Array
    $month = $lost_fields[0]; //String
    $year = $lost_fields[1]; //String
    $tax = $lost_fields[2]; //String
    $locality_name = $lost_fields[3]; //String


    // Check that month is a string
    if(gettype($month) != 'string'){
        $form_state->setErrorByName('text', $this->t('A month value was not parsed as a String when it should have been.'));
    }
    // Check that month is between 1 and 12 when parsed as an int
    $month_int = intval($month);
    if($month_int < 1 || $month_int > 12){
        $form_state->setErrorByName('text', $this->t('The month needs to be between 1 and 12. <code>' . $line . '</code>'));
    }


    // Check that year is a string
    if(gettype($year) != 'string'){
        $form_state->setErrorByName('text', $this->t('A year value was not parsed as a String when it should have been.'));
    }
    // Check that year is between 1800 and 2100 when parsed as an int
    $year_int = intval($year);
    if($year_int < 1800 || $year_int > 2100){
        $form_state->setErrorByName('text', $this->t('The year needs to be a valid 4 digit year.<code>' . $line . '</code>'));
    }
    if(strlen($year_int) != 4){
        $form_state->setErrorByName('text', $this->t('The year needs to be a valid 4 digit year. <code>' . $line . '</code>'));
    }

    // Check that tax is a string
    if(gettype($tax) != 'string'){
        $form_state->setErrorByName('text', $this->t('The tax value was not parsed as a String when it should have been.'));
    }

    // Check that the tax is a number
    if(!is_numeric($tax)){
        $form_state->setErrorByName('text', $this->t('The tax needs to be a valid number.<code>' . $line . '</code> <br> Tax:' . $tax));
    }

    // Check that locality is a string
    if(gettype($locality_name) != 'string'){
        $form_state->setErrorByName('text', $this->t('The locality value was not parsed as a String when it should have been.'));
    }
    // Check that the locality has enought letters
    if(strlen($locality_name) < 5){
        $form_state->setErrorByName('text', $this->t('The locality needs to be a full name of a locality. It must match the localities in the database. <code>' . $line . '</code>' ));
    }
    // Check Locality for extra trailing commas
    $comma = ',';
    if( strpos($locality_name, $comma) !== false ) {
         $form_state->setErrorByName('text', $this->t('The locality needs to be a full name of a locality with trailing commas removed. It must match the localities in the database. <code>' . $line . '</code>'));
    }
}
}
```

Had to change the roles that are allowed to see the /import-lost-form forom within the .routing.yml file. administrator+editor means OR. Using a + means they must have both roles.

# News Updates on coopercenter.org site

Adding all the `new-twig-elelments` folder to the main cooper center site. There are some duplicates that need to be removed.

Importing the config from the latest demographics config failed. Need to swap out the theme name in all of the config files.

After adding media.type.file.yml the import suceeded.

# Module defined menu links

[Documentation](https://www.drupal.org/docs/drupal-apis/menu-api/providing-module-defined-menu-links)

Generate a new module called `submit_support_request` using drupal console `drupal genereate:module`.

Then I added a file for the menu link `submit_support_request.links.menu.yml` with the following contents:

```
submit_support_request.admin:
  title: 'Report Website Problem'
  description: 'Report a problem or submit a website work request through the support.coopercenter.org site'
  parent: system.admin
  url: https://support.coopercenter.org/request
  weight: 100
```

Now on the theme style I added the following style:

# Exporting VDOT data to CSV

Navigate to the [VDOT survey Webform results download page](https://vdot.coopercenter.org/admin/structure/webform/manage/2018_vdot_survey/results/download)

## Format Options

Export as `Delimited Text` using a comma as the Delimiter. Check the Generate Excel compatible file.

## Element Options

Semicolon delimiter for multiples since we're creating a CSV and we want them in one column.
I saved these options but you want to show the labels whenever possible.

## Header Options

Show the Element titles (label) and use a comma delimiter.

## Download Options

Submitted to: `Content` with the ID of the webform content ID `16241` for 2019. This is the Webform content page you created. You'll get the ID by going to the Content overview and finding the Node ID for the most recent Webform.

Limit to All Completed submissions only.

# 2020 VDOT form setup

First you need a CSV of VDOT receipts for the previous year. This file gets uploaded to the custom modules folder `/docroot/modules/custom/2019_VDOT_receipts.csv`.

Create a new migration source yaml file `/docroot/modules/custom/vdot_user_csv_migration/config/install/migrate_plus.migration.vdot_receipts_2019.yml` in the install profile for your custom vdot module.

Update the full path of the VDOT receipts csv file in the yaml file which looks like this presently `"/mnt/gfs/uvacooperdev/livedev/docroot/modules/custom/2019_VDOT_receipts.csv"`.

Import the new vdot migration using drush.

```
drush config-import -y --partial --source=modules/custom/vdot_user_csv_migration/config/install
```

# Generating New Minimal

php -d memory_limit=-1 /home/uvacooper/.c9/node/bin/composer require drupal/views_bootstrap drupal/entity_browser drupal/redirect
