---
layout: default
---

# Hero Video Posting

Video Size: 1280x720 mp4 file

The field needs to be named exactly `field_hero_video_direct_link`. Text field plain 400 length.

The tagline must be named `field_tagline` and is also plain text.

The video gets displayed in the `page--node.html.twig.html` file right after the main-container div class.

```
{# Hero Video #}
{% if node.field_hero_video_direct_link.value %}
    <div class="hero-container">
      <video autoplay loop muted class="hero-bg">
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
