---
layout: default
---

#SASS phpFileStorm setup Sass

![Screenshot of setup](assets/images/Screen Shot 2017-09-05 at 3.17.44 PM.png)

```
/Users/miles/.rvm/gems/ruby-2.4.1/bin/sass
--no-cache --update $FileName$:$FileNameWithoutExtension$.css
$FileNameWithoutExtension$.css:$FileNameWithoutExtension$.css.map
```

![settings-sass](../../images/settings-sass.png)

Sass is easier but having all of these preset css values is horrible.

I found a great trick for editing multiple lines at once in phpStorm.
The alt key adds a new cursor so you can type in two places at once.

Get rid of the .header margin

```css
#search-block-form > div > div,
#edit-submit {
  margin-top: 10px;
}

#footer {
  background-color: #002654;
  color: #ffffff;
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  padding: 1rem;
  margin-bottom: 0;
}

*,
*:before,
*:after {
  box-sizing: inherit;
}
```

Here's a great codepen on [getting a footer to actually stick to the bottom of the page](https://codepen.io/cbracco/pen/zekgx). It recommends that you set the foother to absolute bottom and then add bottom padding to the parent element of the footer to equal height of the footer. Without that padding if the content reached the footer they would hide each other instead of pushing the footer lower. The height of the page needs to be at least 100% to push the footer off.

http://ceps.dd:8083/sites/ceps/files/default_images/3-2_0073_samuel-zeller-34751.png

## Flexbox

[Docs](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Typical_Use_Cases_of_Flexbox)

### Properties of parent

display: flex
justify-content: space-between - puts space between all items

justify-content: center; - Centers it on primary axis
align-items: center; - Centers on y axis

align-items: flex-start -puts item at top  
align-items: flex-end - puts item at bottom

flex-direction: column; - which direction do the items stretch - good for switching to mobile or cards
flex-direction: row-reverse; - for putting content in reverse order on main axis

### Properties of child

flex: auto - which means flex: 1 1 auto - which means all item grow and shrink at same rate.

```
C:/Ruby24/bin/sass.bat
$FileName$:$FileNameWithoutExtension$.css
$FileNameWithoutExtension$.css:$FileNameWithoutExtension$.css.map
```

3. Make sure that the ruby folder is added to the path. You can get to the windows path through start > Environment Variables

## SASS on cloud9

So sass is installed on the Cooper Center website livedev server. You can check with:

```
sass --version
1.11.0 compiled with dart2js 2.0.0
```

To start watching the sass files run:

```
cd /home/uvacooper/dev/livedev/docroot/themes/coopercenter_units/css
sass --watch .

or
sass --watch .:.

or
sass --watch .:output_dir/
```

[You can also lighten and darken colors with sass functions.](https://robots.thoughtbot.com/controlling-color-with-sass-color-functions)

```
background: lighten( $lt_grey,  5% )
background: lighten( $lt_grey,  10% )
```

# Animations

Tip for chrome. You can inspect animations in the devtools. It's next to the console.

# Border box

By default the box sizing is `content-box`. That means that the width doesn't include the padding or border which is annoying. When you set something to be 200px you expect it to be 200px.

How do I set the box-sizing to border-box everywhere?

[source](https://w3bits.com/box-sizing-reset/)

```
html
  box-sizing: border-box

*,
*:before,
*:after
  box-sizing: inherit
```

# Sass Ampresand tutorial

https://css-tricks.com/the-sass-ampersand/

The ampresand symbol refers to all of the parent compiled classes

```
.parent {
  .child {
    .grand-child & {
      &.sibling { }
    }
  }
}
```

Compiles to

```
.grand-child .parent .child.sibling {}
```

Notice that the compiled version starts at the outside most layer `parent child` and then adds that into the `grand-child` on the right.

If you want to keep things nested you can do that without making the sass too specific.

`@at-root` to the rescue

You can exit the sass tree with `@at-root` . That makes that level taken out of the tree as if it were its own thing.

```
.grand-parent {
  .parent {
    @at-root .child {}
  }
}
```

https://cssanimation.rocks/pseudo-elements/

Pseudo elements are added in for free before or after elements. You need to give them content to make them visible.

Psuedo elements are not psuedo classes. Pseudo elements use two :: while classes only use one : .

# Grep

You can use grep to find function definitions. `grep -rli 'function_name_here'` will recursivley search the current directory for (case insensitive) function names and return matching files.

# Select sibling

You can use the `+` to select the sibling element. Below is an example where if the input is checked then the paragraph next to it will have a line through.

```html
<div class="item">
  <input type="checkbox" />
  <p>This is an inbox layout.</p>
</div>
```

```css
input:checked + p {
  background: #f9f9f9;
  text-decoration: line-through;
}
```

# Hide Element entirley at bottom of something

```scss
.outside {
  position: relative;
  overflow: hidden;
  .inside {
    position: absolute;
    bottom: 0;
    transform: translateY(100%) translateY(-5px); //You can add more than one translates to a transform
  }
}
```

# Hide and show element using transform: scale(x)

```scss
a:after {
  content: '';
  position: absolute;
  height: 1px;
  width: 100%;
  bottom: 0;
  left: 0;
  visibility: hidden;
  background-color: #fff;
  transform: scaleX(0);
  -webkit-transform: scaleX(0);
}

a:hover:after {
  transform: scaleX(1);
  -webkit-transform: scaleX(1);
  visibility: visible;
}
```

# Extend & Inheritance

Using `%` and `@extend` you can create sections of scss that are shared and don't print unless you extend them in an actual class. This keeps your scss very neat.

```scss
%animate-underline {
  position: relative;

  &:before {
    content: '';
    position: absolute;
    width: 100%;
    height: 1px;
    bottom: 0;
    left: 0;
    background-color: $color__white;
    visibility: hidden;
    -webkit-transform: scaleX(0);
    transform: scaleX(0);
    -webkit-transition: all 0.25s ease-in-out 0s;
    transition: all 0.25s ease-in-out 0s;
  }

  &:hover {
    &:before {
      visibility: visible;
      -webkit-transform: scaleX(1);
      transform: scaleX(1);
    }
  }
}

a {
  @extend %animate-underline;
}
```
