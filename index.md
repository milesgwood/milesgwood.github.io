# Recent Work

This site's goal is to provide quality explanation of the work I've been doing. If I or anyone else reads one of these pages and doesn't understand what's going on without clicking a link, I have been lazy and failed to make this a useful resource. Links don't help to understand anything, they just point you to a encyclopedia and tell you to go find the real answer you were looking for. All resources, links, and instructions need to be explained so that they can be useful later.

Don't be a lazy pile of garbage Miles. Write something useful.

## AWS work

[phpMyAdmin on AWS](/pages/AWS/phpMyAdmin)

## Bash and Scripting

[Bash Scripting](pages/bash/examples)

[Ubuntu on Windows and Jeckyll Setup](pages/bash/ubuntu-bash-jeckyll-setup.md)

## Drupal

[Config Import Export](pages/drupal/config)

[SimpleSamlPHP and Drupal Netbadge setup](pages/drupal/SimpleSamlPHP)

[Using Composer](pages/drupal/composer)

[Manual Database Inserts](pages/drupal/database)

[Launching Sites](pages/drupal/launching-sites)

[Drupal 7 -> 8 Migrate](pages/drupal/migrate)

[Multisite](pages/drupal/multisite)

[Page Templates](pages/drupal/templates)

[Twig Templates](pages/drupal/twig)

[Drupal Updates](pages/drupal/updates)

[General Work notes](pages/drupal/work-notes)

## Git

[Setup and Reverting](pages/git/git)

## Python

[Making a Database Connection](pages/python/database_connection)

## React

[First Project](pages/react/getting-started)

## Sass

[Sass](pages/sass/sass)

## Computer Troubleshooting and Pages Setup

[Windows Setup](pages/setup/desktop)
[Atom KeyBindings](pages/setup/keybindings)

# How to Download site and run locally

```bash
#!/bin/bash
#Pull this file out outside of this directory and run it ./pull_and_run
if ! [ -f milesgwood.github.io/_config.yml ]; then
    echo "_config.yml File not found! Cloning"
    git clone https://github.com/milesgwood/milesgwood.github.io.git && /
    git clone https://github.com/pages-themes/midnight.git && /
    cd midnight && /
    script/bootstrap && /
    echo "Changing directory to milesgwood.github.io" && /
    cd ../milesgwood.github.io/ && /
    cp -n -R ../midnight/* . && /
    echo "Copying gem 'github-pages', group: :jekyll_plugins to Gemfile"
    echo "gem 'github-pages', group: :jekyll_plugins" >> Gemfile && /
    cd ..
fi
cd milesgwood.github.io/ && /
git pull && /
python -mwebbrowser http://localhost:4000 && /
bundle update && /
bundle exec jekyll serve && /

#Commit The Changes
 git status
 read -p "Commit description: " desc
 git add . && /
 git commit -m "$desc" && /
 git push
 ```
[Localhost Port 4000](http://localhost:4000)

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

#Emphasis
*This text will be italic*
_This will also be italic_

**This text will be bold**
__This will also be bold__

_You **can** combine them_

# Task Lists

- [x] @mentions, #refs, [links](), **formatting**, and <del>tags</del> supported
- [x] list syntax required (any unordered or ordered list supported)
- [x] this is a complete item
- [ ] this is an incomplete item

#Tables

First Header | Second Header
------------ | -------------
Content from cell 1 | Content from cell 2
Content in the first column | Content in the second column

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

[For valid code block assignments try to use capitals as this list specifies.](https://github.com/github/linguist/blob/master/lib/linguist/languages.yml)

JavaScript bash Ruby HTML PHP Java Python

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/milesgwood/milesgwood.github.io/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
