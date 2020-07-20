---
layout: default
---

# Markdown Editing

The Markdown editor is far superior to Atom. You can get a live preview immidiatley with images and everything. To start the preview open an Markdown file `.md` and hit `Ctrl + Shift + V`.

You can even click on the text in the preview and the file will open with the cursor at that point!

# Sass Editing

VSCode doesn't support easy Sass compiling in different folders. For some reason the @import statements don't work. I solved this without needing to keep all of the css in the same directory as the sass. Just run this command in the terminal from the project root: 

```
sass --watch SASS:css
```

Don't use the compile files menu element. Use the terminal. In order to get the `Open in Browser` feature to work on right click, the compile files option remains in the menu. This is part of the "Sass/Less/Scss/Typescript/Javascript/Jade/Pug Compile Hero Pro" extension. I disabled the sass compilation on save to avoid dist folders appearing.

# SCSS Editing

I really prefer the SASS syntax but the SCSS extensions work far better. You can jump to variable and function definitions with `Ctrl + Click`. The tips are also much more useful. You can hover over the attribute to get the options available to you. 

```
sass --watch SCSS:css
```

# Drupal Editing 

[Drupal.org reccommended setup and extensions](https://www.drupal.org/docs/develop/development-tools/configuring-visual-studio-code)

Extensions to Enable

[Composer](https://marketplace.visualstudio.com/items?itemName=ikappas.composer)

You must specify the command path

2. 