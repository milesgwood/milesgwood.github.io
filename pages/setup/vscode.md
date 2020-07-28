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

# Extensions to Enable for Drupal on Macbook

[Drupal.org reccommended setup and extensions](https://www.drupal.org/docs/develop/development-tools/configuring-visual-studio-code)

[Additional Extenstions](https://github.com/viatsko/awesome-vscode)

## Debugger for Chrome

Lets you debug JS that is served from a locally served file. You can set breakpoints in VScode.

## phpcs

php code linting and sniffing

```bash
composer global require squizlabs/php_codesniffer
composer global require drupal/coder
```

Open up your User settings.json or alternativley your Workspace settings.json.
`~/Library/Application Support/Code/User/settings.json`

Add the following to the settings array:

```
    "phpcs.enable": true,
    "phpcs.standard": "/Users/miles/.composer/vendor/drupal/coder/coder_sniffer/Drupal",
    "phpcs.executablePath": "/Users/Shared/Sites/devdesktop/drupal-8.9.1/vendor/bin/phpcs",
```

In the user settings I set path to the Drupal Code Standards configuration that is set by drupal/coder `/Users/miles/.composer/vendor/drupal/coder/coder_sniffer/Drupal`

Open a random theme or core PHP file to check if the number of errors changes when you set the phpcs.standard field. When you save settings.json you should see the number of errors flucuate.

To get the linter to inspect .theme files and other php files with irregular endings you have to edit the JS for the linter. This is a [current open issue on DO](https://github.com/ikappas/vscode-phpcs/issues/159).

Add `lintArgs.push('--extensions=inc,install,module,php,profile,theme');` after line 111 of `~/.vscode/extensions/ikappas.phpcs-1.0.5/server/src/linter.js`. Then errors will be reported on .theme and .module files where you write loads of hooks. This was my biggest complaint about using PHPStorm. The linter wouldn't recognize .theme files so I was writing PHP blind.

Add the following to settings.json to get PHP to validate your code as you type. It requires the path to your current PHP installation. Again you should have a php file open so you can test to see if you get additional errors on typing. With the linter I get 5 errors on an incomplete function definition. With this setting added I get additional errors.

```
    "php.validate.enable": true,
    "php.validate.executablePath": "/Applications/DevDesktop/php7_2_x64/bin/php",
    "php.validate.run": "onType"
```



## phpbcf PHP Code Beautifier and Fixer

```
composer require "squizlabs/php_codesniffer=*"
```

## PHP DocBlocker

Automatically adds PHP docblocs.

## empy-indent

Automatically removes indentations on empty lines

## PHP Debug

The extension is already installed however after inserting a phpinfo(); into my index.php file on my drupal site and entering that output HTML into [this xdebug checking site](https://xdebug.org/wizard.php) I see that xdebug isn't enabled. Acquia seems to already have installed xdebug 2.6.0. I just needed to add these lines to enable remote debugging to the php.ini

```
zend_extension="/Applications/DevDesktop/php7_2_x64/ext/xdebug.so"

;;;;;;;;;;;;;;;;;;;
; Module Settings ;
;;;;;;;;;;;;;;;;;;;

[XDebug]
xdebug.remote_enable = 1
xdebug.remote_autostart = 1
```

## [PHP Intelephense](https://marketplace.visualstudio.com/items?itemName=bmewburn.vscode-intelephense-client)

Code autocompletion.

## [Composer](https://marketplace.visualstudio.com/items?itemName=ikappas.composer)

You must specify the path to composer `/usr/local/bin/composer` in the extension settings.

To run a command you hit `F1` and then type the command for example clear cache.

Running these commands created and issue where I had to choose the project folder after typing the command. To get aroud this I created a symbolic link to the folder where my markdown notes are.

```ln -s /Users/miles/Documents/milesgwood.github.io/pages/ notes```

### Editing ~./bash_profile

Drush commands aren't executable from the VS code terminal. The drush installation is found under DevDesktop's install.

I'm adding what DevDesktop adds to the path normally.

```
vim ~/.bash_profile

export PHP_ID=php7_2; export PATH="/Applications/DevDesktop/$PHP_ID/bin:/Applications/DevDesktop/mysql/bin:/Applications/DevDesktop/tools:$PATH"
```

## Twig Language 2 & Drupal 8 Twig Snippets

Gives you twig language support and some quick twig snippets.

# Drupal Console

You must install Drupal Console Launcher globally first. These commands will move the launcher into your /usr/local/bin directory and set it to be executable by everyone. You may need to use "sudo" with the "mv" command. Lastly we test the install with `drupal about`.
```
curl https://drupalconsole.com/installer -L -o drupal.phar
mv drupal.phar /usr/local/bin/drupal
chmod +x /usr/local/bin/drupal
```

Now we must install drupal console on each specific site using composer and test with `drupal site:status`.

```
composer require drupal/console:~1.0 --prefer-dist --optimize-autoloader --sort-packages
```

## Updating Drupal Console

To update the global launcher, navigate to somewhere outside of your Drupal 8 site and run `drupal self-update`.

To update your site's Drupal Console navigate to each site root and run the following:

```
composer update drupal/console --with-dependencies
```
