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
