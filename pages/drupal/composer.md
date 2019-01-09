---
layout: default
---

# Installing Composer

I need the composer command line tools to install dependencies for a csv_serialization module needed for the CEPS site. It allows you to directly install dependencies from the command line like `composer require drupal/csv_serialization`. So I'm starting on [the composer site.](https://getcomposer.org/doc/00-intro.md)

[The downloads page has specific instructions that change with each version.](https://getcomposer.org/download/)

```
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('sha384', 'composer-setup.php') === '93b54496392c062774670ac18b134c3b3a95e5a5e5c8f1a9f115f203b75bf9a129d5daa8ba6a13e2cc8a1da0806388a8') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
```

```
php composer-setup.php
All settings correct for using Composer
Downloading...

Composer (version 1.8.0) successfully installed to: /mnt/gfs/uvacooperdev/livedev/docroot/composer.phar
```
So now we have the composer binary which can be run on cmd with `php composer.phar ... ` The file can be renamed by running this during setup `php composer-setup.php --install-dir=bin --filename=composer`
php composer-setup.php --install-dir=/home/uvacooper/.c9/node/bin/composer --filename=composer

Now move composer to a place on the PATH so you can use it globally. The .c9/node/bin folder is already on the path and I can access it.
 ```
 mv composer.phar /home/uvacooper/.c9/node/bin/composer
 ```

 If you can't install it globally like on Acquia, you can just run it with composer.phar in the directory it was installed in.
 Now I can use lines like `composer require drupal/csv_serialization` from the docroot and have modules installed with dependencies.

 php composer.phar install
 php composer.phar require drupal/core
 php composer.phar update
 php composer.phar update drupal/core
 php composer.phar update drupal/core --with-dependencies

 [Drupal Scaffold builds up the default files for Drupal Core versions.](https://github.com/drupal-composer/drupal-scaffold) I want my custom .htaccess file so I need to tell it to exclude my .htaccess file by placing the following in  the extras section. The command gets executed on updates and installs via the scripts section.

 ```
 "drupal-scaffold": {
            "excludes": [
                ".htaccess",
                "robots.txt"
            ]
        }
```

You run `composer update` to express the changes made to the json file. `composer install` takes the lock file and creates the site using that configuration. So when you import the new composer profile, you always run composer install to sync the current files with the files from the lock file. That way all environments are operating on the same code. I haven't figured out how this deploys yet since I took all modules out of git tracking.

To update composer itself you run `composer self-update`

```
You are already using composer version 1.8.0 (stable channel).
```

Get all the current modules from drush `drush pml --no-core --status=enabled`

Enabled but not contrib
vig_course_descriptions
publications_type_2

When launching changes you need to re add the removed git folders for code

```
docroot/core
docroot/modules/contrib
docroot/themes/contrib
vendor
```

You should ignore these
```
docroot/core
docroot/modules/contrib
docroot/themes/contrib
docroot/profiles/contrib
docroot/libraries
```

You should remove these from git when you are updating

```
git rm -r --cached docroot/core
git rm -r --cached docroot/modules/contrib
git rm -r --cached docroot/themes/contrib
git rm -r --cached docroot/profiles/contrib
git rm -r --cached docroot/libraries
git rm -r --cached vendor
git rm -r --cached docroot/vendor
```

https://drupalize.me/tutorial/use-composer-your-drupal-project?p=3233
https://github.com/grasmash/composerize-drupal


```
Install Composer
composer global require grasmash/composerize-drupal
composer composerize-drupal --composer-root=/home/uvacooper/dev/livedev --drupal-root=/home/uvacooper/dev/livedev/docroot --exact-versions --no-update
```

[Found a code edit to add to grasmash's tool to return modules missing their versions.](https://github.com/grasmash/composerize-drupal/pull/8/commits/595d0fe1a233e8f751027f372242994939529c70). The file is located at `~/.composer/vendor/grasmash/composerize-drupal/src/Utility/DrupalInspector.php`

```
<?php
namespace Grasmash\ComposerConverter\Utility;
use Symfony\Component\Finder\Finder;
use Symfony\Component\Yaml\Yaml;
class DrupalInspector
{
    public static function findContribProjects($drupal_root, $subdir)
    {
        if (!file_exists($drupal_root . "/" . $subdir)) {
            return [];
        }
        $finder = new Finder();
        $finder->in([$drupal_root . "/" . $subdir])
            ->name('*.info.yml')
            ->depth('== 1')
            ->files();
        $projects = [];
        $invalid_versions = [];
        foreach ($finder as $fileInfo) {
            $path = $fileInfo->getPathname();
            $filename_parts = explode('.', $fileInfo->getFilename());
            $machine_name = $filename_parts[0];
            $module_info = Yaml::parseFile($path);
            $semantic_version = self::getSemanticVersion($module_info['version']);
            echo "The module previous to this one caused the error due to it lacking a version:" . $machine_name . " " . $semantic_version . "\n";
            if ($semantic_version === false) {
                $invalid_versions[] = $machine_name;
            } else {
                $projects[$machine_name] = $semantic_version;
            }
        }
        if (!empty($invalid_versions)) {
            throw new \Exception("The following projects contain invalid versions: " . implode(', ', $invalid_versions));
        }
        return $projects;
    }
    /**
     * Generates a semantic version for a Drupal project.
     *
     * 3.0
     * 3.0-alpha1
     * 3.12-beta2
     * 4.0-rc12
     * 3.12
     * 1.0-unstable3
     * 0.1-rc2
     * 2.10-rc2
     *
     * {major}.{minor}.0-{stability}{#}
     *
     * @return string
     */
    public static function getSemanticVersion($drupal_version)
    {
        // Strip the 8.x prefix from the version.
        $version = preg_replace('/^8\.x-/', null, $drupal_version);
        if (preg_match('/-dev$/', $version)) {
            return preg_replace('/^(\d).+-dev$/', '$1.x-dev', $version);
        }
        $matches = [];
        preg_match('/^(\d{1,2})\.(\d{0,2})(\-(alpha|beta|rc|unstable)\d{1,2})?$/i', $version, $matches);
        $version = false;
        if (!empty($matches)) {
            $version = "{$matches[1]}.{$matches[2]}.0";
            if (array_key_exists(3, $matches)) {
                $version .= $matches[3];
            }
        }
        // Reject 'unstable'.
        return $version;
    }
}
```
