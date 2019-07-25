---
layout: default
---

I want to create a custom block that exists in a module. The block needs to display the slider of profile info. I'll start by simply trying to create a block through code.

- Login to the cloud9 module dev site.
- Make sure the database is started.
```
sudo service mysqld status
sudo service mysqld start
```
- Then you can run the application (by running index.html) and then click preview which will generate a URL that you can use to access the site.

```
composer global update
```

Composer doesn't seem to want to cooperate with the site. Adding global updates lots of packages but doesn't update core for some reason.

Make sure you have drush installed. If you can't access it adjust the path to include it.

```
export PATH="$HOME/.composer/vendor/bin:$PATH"
cd sites/default
drush updb
```

Make sure drupal console is installed as well so we can run `drupal generate:module` For this module composer is broken on this site so I can't use drupal console.

```
composer require drupal/console:~1.0 --prefer-dist --optimize-autoloader
```

Install some basic modules

```
composer require drupal/admin_toolbar:^1.26
composer require drupal/module_filter:^3.1
composer require drupal/bootstrap:^3
composer require drupal/bootstrap_paragraphs:2.0.0-beta6
composer require drupal/devel
drush en devel_generate -y
drush en admin_toolbar module_filter -y
```


[Tutorial on Creating custom block with twig template](https://ws.agency/blog/how-create-custom-blocks-d8-and-set-display-twig)

[Drupal tutorial](https://www.drupal.org/docs/8/theming/twig/create-custom-twig-templates-for-custom-module)

## Actual start of creating the module

- Create a photo-slider module folder
- Create a `photo-slider.info.yml` file
```
name: WS Custom Example Block
description: A custom block created in code
type: module
core: 8.x
package: Custom
version: '1.0'
dependencies:
  - drupal:node
```
- Create a `photo_slider.module` file
This file defines the variables to be passed to the template and names the template. These variables are accessed in the twig file you'll create with `content.title`.
```
<?php

// Implements hook_theme()
function photo_slider_theme() {
  return array(
   'photo_slider_block' => array(
            'variables' => array('title' => NULL, 'description' => NULL),
            'template' => 'block--photo-slider',
        ),
  );
}
```
- Create `src/Plugin/Block/PhotoSlider.php`
This file declares the block ID and admin label so that you can find it in the Block Layout page. This is also where you will create the logic that fills in the variables.

```
<?php

namespace Drupal\photo_slider\Plugin\Block;

use Drupal\Core\Block\BlockBase;

/**
 * Provides a 'photo_slider custom' block.
 *
 * @Block(
 *   id = "photo_slider_custom_block",
 *   admin_label = @Translation("Photo Slider Custom Block"),
 *
 * )
 */
class PhotoSlider extends BlockBase {
  /**
   * {@inheritdoc}
   */
  public function build() {
  // do something
    return array(
      'title' => 'Cooper Center Staff',
      'description' => 'Websolutions Agency is the industry leading Drupal development agency in Croatia'
    );
  }
}
```

- Create the `block--photo-slider.html.twig`
This file actually uses the variables to create the slider. You will need to create a loop here to use all the nodes available.
```
{#
/**
 * @file
 * Photo Slider custom block.
 */
#}
 <div>
    <h2>TWIG</h2>
    <h1>{{ content.title }}</h1>
    <p>{{ content.description }}</p>
 </div>
 ```

 Now I need to create some content of the profile type.

Export the current config and take note of where it gets placed in files.

```
drush config-export
copy the needed config files
drush config-import
composer require drupal/devel
drush en devel devel_generate -y
```


[Generate content of type profile](https://befused.com/drupal/drush-devel-generate)

The `--kill` deletes all the previously made content.
```
drush genc 20 --types=profile
drush genc 20 --types=profile --kill
```

nodes -> 43 -> values -> field_profile_email -> x-default -> 0 -> value
nodes -> 43 -> values -> title -> x-default

```
<h2>Output3</h2>
{% for key, profile in content.profiles %}

  {% if profile.field_profile_facebook.uri %}
    <div class="field--item profile-link"><a href="{{ profile.field_profile_facebook.uri }}"><img class='grow' src="/themes/custom/coopercenter_units/_assets/retina-circular-icons/32/facebook.png"/></a></div>
  {% endif %}
  {% if profile.field_profile_linkedin.uri %}
    <div class="field--item profile-link"><a href="{{ profile.field_profile_linkedin.uri }}"><img class='grow' src="/themes/custom/coopercenter_units/_assets/retina-circular-icons/32/linkedin.png"/></a></div>
  {% endif %}
  {% if profile.field_profile_twitter.uri %}
    <div class="field--item profile-link"><a href="{{ profile.field_profile_twitter.uri }}"><img class='grow' src="/themes/custom/coopercenter_units/_assets/retina-circular-icons/32/twitter.png"/></a></div>
  {% endif %}

  {#{{ file_url(profile.field_profile_photo_square.entity.fileuri) }}#}

  {#{{ profile.field_profile_photo_square.entity.url() }}#}
  {{ profile.field_profile_photo_square.entity.fileuri }}

{% endfor %}
```

Second version of the slider


```
<!-- Base MasterSlider style sheet -->
<link href="/masterslider/style/masterslider.css" rel="stylesheet" /><!-- MasterSlider Template Style -->
<link href="/masterslider/style/ms-staff-style.css" rel="stylesheet" type="text/css" /><!-- google font Lato -->
<link href="https://fonts.googleapis.com/css?family=Lato:300,400" rel="stylesheet" type="text/css" />
<!-- jQuery --><script src='/masterslider/jquery.min.js'></script><script src='/masterslider/jquery.easing.min.js'></script>
<!-- Master Slider --><script src='/masterslider/masterslider.min.js'></script>
<!-- template for the round images-->
<div class="ms-staff-carousel ms-round">
<!--Template for the square exclueds the ms-round class--><!--<div class='ms-staff-carousel'>--><!-- masterslider -->
  <div class="master-slider" id="masterslider">

    <div class="ms-slide"><img alt="lorem ipsum dolor sit" data-src="/sites/csr/files/pictures/staff-slider/8.jpg" src="/masterslider/style/blank.gif" />
    <div class="ms-info">
      <h3>Thomas M. Guterbock</h3>

<h4>Director, Center for Survey Research</h4>

<p class="email">E-Mail: <a href="mailto:tomg@virginia.edu">tomg@virginia.edu</a></p>

<p class="phone">Phone: (434) 243-5223</p>

<p>Thomas M. Guterbock, founding director of CSR, received extensive training in quantitative, multivariate methods and has applied these in CSR research, publications and his applied work. In his role as senior project designer and project director for the Center, he has originated and implemented numerous studies, including many that involve either complex sampling, complex questionnaire protocols, or complex analysis strategies.</p>

<ul class="ms-socials ">
	<li class="ms-ico-1 link"><a href="https://www.linkedin.com/in/tom-guterbock-3596b4/">linkedin</a></li>
	<li class="ms-ico-tw gs"><a href="https://scholar.google.com/citations?user=8FOi1iIAAAAJ&amp;hl=en">google</a></li>
</ul>
</div>
</div>

<div class="ms-staff-info" id="staff-info">&nbsp;</div>
<script type='text/javascript'>
      var slider = new MasterSlider();
      slider.setup('masterslider', {
        loop: true,
        width: 240,
        height: 240,
        speed: 20,
        view: 'flow',
        preload: 0,
        space: 0,
        wheel: true
      });
      slider.control('arrows');
      slider.control('slideinfo', {
        insertTo: '#staff-info'
      });
    </script></div>
</div>
```
