---
layout: default
---

# phpStorm on Windows

Download and install it from jetbrains. You'll need to open the docroot folder in phpStorm and enable drupal module.

Add php that your site is using and the composer executable to the path by adding the containing folders.

Set the php version in composer as well
```
"config": {
    "vendor-dir": "vendor",
    "platform": {
        "php": "7.1.1"
    }
```

Update php.ini to have higher memory limit.

```
; Maximum amount of memory a script may consume (128MB)
; http://php.net/memory-limit
memory_limit = -1
```

# Install Composer and drush globally on windows

Run bash on windows by starting it with `bash` from a regular cmd terminal. Then put composer in both your bash and windows PATH.

```
bash
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php --install-dir=bin --filename=composer
export PATH=$PATH:/w/path
export PATH=/w/acquia/stack/php7_1_x64:$PATH
export PATH=$PATH:/w/acquia/sites/uvacooper-dev/docroot
export PATH=$PATH:/w/acquia/sites/uvacooper-dev
```

Manually add w/path through windows environment variable editor so it also sees composer. It will tell you where it installed composer.

```
C:\Users\miles\AppData\Roaming\Composer\vendor\drush\drush
W:\path
```

Now in a regular windows terminal you should have composer and be able to install drush globally.
`composer require global drush/drush:8.1.7`

Composer also imposes its own limits with environment variables. You can avoid this with adding an extra command to your composer commands.

```
php.exe -d memory_limit=-1 composer.phar require drush/drush:8.1.17
```

Up the composer memory from 1.5GB `COMPOSER_MEMORY_LIMIT=-1 php /w/path/composer update`
