---
layout: default
---

# Installing Composer

I need the composer command line tools to install dependencies for a csv_serialization module needed for the CEPS site. It allows you to directly install dependencies from the command line like `composer require drupal/csv_serialization`. So I'm starting on [the composer site.](https://getcomposer.org/doc/00-intro.md)

Run this code to install composer locally.
```
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('SHA384', 'composer-setup.php') === '544e09ee996cdf60ece3804abc52599c22b1f40f4323403c44d44fdfdd586475ca9813a858088ffbc1f233e9b180f061') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
```

 Now move composer to a place on the PATH so you can use it globally
 ```
 mv composer.phar /usr/local/bin/composer
 ```

 Now I can use lines like `composer require drupal/csv_serialization` from the docroot and have modules installed with dependencies.
