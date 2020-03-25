---
layout: default
---

# Hero Video Posting

Video Size: 1280x720 mp4 file

The field needs to be named exactly `field_hero_video_direct_link`. Text field plain 400 length.

The tagline must be named `field_tagline` and is also plain text.

The video gets displayed in the `page--node.html.twig` file right after the main-container div class.

```
{# Hero Video #}
{% if node.field_hero_video_direct_link.value %}
    <div class="hero-container">
      <video autoplay loop muted playsinline class="hero-bg">
        <source src="{{ node.field_hero_video_direct_link.value }}" type="video/webm" alt="HTML5 background video">
      </video>
    </div>
    {#Tagline#}
    {% if node.field_tagline.value %}
        <div class="overlay">
            <div id="tagline">
                {{ node.field_tagline.value }}
            </div>
        </div>
    {% endif %}
{% endif %}
```

# Displaying full width

This is a hack to get the video to display full width within the container no matter the page size. You add the surrounding div and the styling on the iframe itself.

```
<div style="position:relative;height:0;padding-bottom:56.25%">
<iframe allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="" frameborder="0" height="360" src="https://www.youtube.com/embed/videoseries?list=PLer5YrCq8SkzmOJ2z1dgyhVLKTVOU76kC&amp;ecver=2"

style="position:absolute;width:100%;height:100%;left:0" width="640">
</iframe>
</div>
```
