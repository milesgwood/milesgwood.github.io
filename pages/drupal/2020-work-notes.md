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
```

I want to make this block using twig and the grid of all blocks using react.
