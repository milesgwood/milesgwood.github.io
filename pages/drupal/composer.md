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


# Composer Setup on Existing sites

So Composer only adds and removes code from a site. It doesn't handle any configurations or touch the databases at all. So I need to add composer to my sites but to do that I have to add all the modules at once it seems.

https://github.com/grasmash/composerize-drupal

We need to move the contributed code to specific folders. We want to have only one .gitignore and one composer.json. I moved all my modules to the custom folder and all the contributed modules to the contrib folder. [Anatomy of Composer Project](https://drupalize.me/tutorial/anatomy-composer-project?p=3233)

The require section has `[vendor]/[package-name]": "[version constraint]"` format with a carrat ^ for the most recent version. For example `"drupal/webform_bootstrap": "^5.0",` would install the most recent webform_bootstrap module.

After installing the composerize-drupal plugin I ran this command and got an error in the Acquia Logs saying it can't locate module files. I need to clear the cache somehow.

```
composer composerize-drupal --composer-root=/mnt/gfs/uvacooperdev/livedev --drupal-root=/mnt/gfs/uvacooperdev/livedev/docroot --exact-versions --no-update
```

So after moving all of the files the site is broken. I need to reset the cache. `drush cr` has no effect.

I'm going to clear the opcache by making an executable bash script called `/usr/local/bin/opcache-clear`. I can't put things in bin so I had to put it above my docroot and run it.

```
#!/bin/bash
WEBDIR=/mnt/gfs/uvacooperdev/livedev/docroot
RANDOM_NAME=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13)
echo "<?php opcache_reset(); ?>" > ${WEBDIR}${RANDOM_NAME}.php
curl http://coopercenter.org/${RANDOM_NAME}.php
rm ${WEBDIR}${RANDOM_NAME}.php
```

I also tried to clear the APC cache by running this php file. You have to stick it below the docroot to navigate to it in the browser. Acquia said it was not able to run the function. So I don't think this worked.

```
<?php
apc_clear_cache();
```

What seemed to work was runnint the drush cr command from the docoot and the actual site folder. I also changed the memory size for all the caches in acquia and that seemed to do something. I got a 500 error instead of the WSOD.

I then had to fix the theme template branding file so that the cooper center logo displayed.

Now the media site is working so I will clear the cache for all the other sites and make sure they are working. I want to figure out how to clone the sites to a new Amazon EC2 instance and make a tutorial about it. My understanding is that I need to backup the database, config files, and then transfer over the custom code. Then all I need to do is run the composer lines to install the modules and dependencies.

So I ran the composer generate command from the `~/dev/livedev` folder and got an actual output composer.json file.

```
composer composerize-drupal --composer-root=/home/uvacooper/dev/livedev --drupal-root=/home/uvacooper/dev/livedev/docroot --exact-versions --no-update
```

composer.json
```
{
    "name": "my/project",
    "description": "Project template for Drupal 8 projects with composer",
    "type": "project",
    "license": "GPL-2.0-or-later",
    "authors": [
        {
            "name": "",
            "role": ""
        }
    ],
    "repositories": {
        "drupal": {
            "type": "composer",
            "url": "https://packages.drupal.org/8"
        },
        "asset-packagist": {
            "type": "composer",
            "url": "https://asset-packagist.org"
        }
    },
    "require": {
        "php": "^5.5.9|>=7.0.8",
        "composer/installers": "^1.2.0",
        "cweagans/composer-patches": "^1.6.5",
        "drupal-composer/drupal-scaffold": "^2.5.4",
        "grasmash/drupal-security-warning": "^1.0.0",
        "oomphinc/composer-installers-extender": "^1.1",
        "wikimedia/composer-merge-plugin": "^1.4.1",
        "drupal/backup_migrate": "4.0.0",
        "drupal/bootstrap_paragraphs": "2.0.0-beta6",
        "drupal/captcha": "1.0.0-beta1",
        "drupal/csv_serialization": "1.4.0",
        "drupal/ctools": "3.0.0",
        "drupal/devel": "1.2.0",
        "drupal/externalauth": "1.1.0",
        "drupal/google_analytics": "2.3.0",
        "drupal/imce": "1.7.0",
        "drupal/paragraphs": "1.5.0",
        "drupal/pathauto": "1.3.0",
        "drupal/quick_node_clone": "1.8.0",
        "drupal/recaptcha": "2.3.0",
        "drupal/token": "1.1.0",
        "drupal/contribute": "1.0.0-beta7",
        "drupal/calendar": "1.x-dev",
        "drupal/colorbox": "1.4.0",
        "drupal/config_update": "1.5.0",
        "drupal/contact_formatter": "1.1.0",
        "drupal/admin_toolbar": "1.25.0",
        "drupal/entity_reference_revisions": "1.6.0",
        "drupal/entity_usage": "2.0.0-alpha8",
        "drupal/examples": "1.x-dev",
        "drupal/features": "3.7.0",
        "drupal/field_permissions": "1.0.0-rc1",
        "drupal/first_time_login": "1.1.0",
        "drupal/group": "1.0.0-rc2",
        "drupal/mailchimp": "1.8.0",
        "drupal/migrate_plus": "4.1.0",
        "drupal/migrate_source_csv": "2.2.0",
        "drupal/migrate_tools": "4.1.0",
        "drupal/projects": "1.2.0",
        "drupal/redirect_after_login": "2.3.0",
        "drupal/shortcode": "1.0.0-rc1",
        "drupal/simplesamlphp_auth": "3.0.0-rc6",
        "drupal/views_data_export": "1.0.0-beta1",
        "drupal/views_templates": "1.0.0-alpha1",
        "drupal/viewsreference": "1.4.0",
        "drupal/vocab": "*",
        "drupal/webform": "5.1.0",
        "drupal/webform_views": "5.0.0-alpha6",
        "drupal/bootstrap": "3.16.0",
        "drupal/core": "8.6.7"
    },
    "require-dev": {},
    "config": {
        "sort-packages": true,
        "discard-changes": true
    },
    "conflict": {
        "drupal/drupal": "*"
    },
    "extra": {
        "enable-patching": true,
        "composer-exit-on-patch-failure": true,
        "patchLevel": {
            "drupal/core": "-p2"
        },
        "patches": [],
        "installer-types": [
            "bower-asset",
            "npm-asset"
        ],
        "installer-paths": {
            "drush/Commands/{$name}": [
                "type:drupal-drush"
            ],
            "docroot/core": [
                "type:drupal-core"
            ],
            "docroot/modules/contrib/{$name}": [
                "type:drupal-module"
            ],
            "docroot/modules/custom/{$name}": [
                "type:drupal-custom-module"
            ],
            "docroot/profiles/contrib/{$name}": [
                "type:drupal-profile"
            ],
            "docroot/profiles/custom/{$name}": [
                "type:drupal-custom-profile"
            ],
            "docroot/themes/contrib/{$name}": [
                "type:drupal-theme"
            ],
            "docroot/themes/custom/{$name}": [
                "type:drupal-custom-theme"
            ],
            "docroot/libraries/{$name}": [
                "type:drupal-library",
                "type:bower-asset",
                "type:npm-asset"
            ]
        },
        "merge-plugin": {
            "include": [
                "docroot/modules/custom/*/composer.json"
            ],
            "replace": false,
            "ignore-duplicates": true
        }
    },
    "minimum-stability": "dev",
    "prefer-stable": true
}
```

# Composer workflow

```
Backup the databases and configurations.
./db_backup.sh
./export_config.sh

Update a single module
$ composer update drupal/ctools --with-all-dependencies

Install a new module
$ composer require drupal/ctools:^1.1.0 --update-with-all-dependencies

Update all packages within version constraints
$ composer update

Remove a unused Plugin
composer remove drupal/vocab
```

Updating numerous packages without touching simplesamlphp_auth is tricky. You need to list all the updates in a single line.

composer.json is missing
```
"drupal/config_update": "^1",
"drupal/field_permissions": "^1",
"drupal/views_data_export": "^1.0",

shortcode
migrate_tools
group
examples
```

simplesamlphp was set to rc6 when it should be 3.0. I set it manually to 3.0

Ran `composer update` with json updated and hard coded simplesaml and externalauth.

Removed this module - `"drupal/admin_toolbar_tools": "1.25.0",`

simplesamlphp/simplesamlphp got updated anyway 1.16.3->1.18.2

Even with that update the sites are working.


For if it fails...

composer update drupal/bootstrap:^3.2 drupal/webform:^5.0 drupal/views_data_export:^1.0 drupal/pathauto:^1 drupal/paragraphs:^1 drupal/mailchimp:^1 drupal/field_permissions:^1   drupal/entity_reference_revisions:^1 drupal/contribute:^1 drupal/admin_toolbar:^2

# Checking if module is installed anywhere

`drush pm-info <module_name>` checks that one site and will list out all the module's info.

This command will check the current list of enabled modules which we can iterate through all the sites to check.

`drush pm-list --pipe --type=module --status=enabled --no-core | grep "projects"`

Here is a script that runs through all the sites and will tell you if it is installed.

```
# !/bin/bash
docroot="/home/uvacooper/dev/livedev/docroot"
echo "Searching for module : " $1 && \

cd docroot/sites && \
for SITE in media ceps certify newsletter cooper csr demographics lead sei sorensen support vig vdot beheardcva
do
    cd $SITE && \
    echo "---Searching" $SITE && \
    drush pm-list --pipe --type=module --status=enabled --no-core | grep $1
    cd ..
done
```

# Error on Updates

The simplesamlphp composer updates breaks the sites. You need to copy the contents of simplesaml_backups to the correct locations which is the `/vendor/simplesamlphp/simplesamlphp` folder. There should be a config, metadata, cert, and log folder there.

Those 4 folders are usually already populated. The log folder is empty but you need to make sure it exists. You can delete the contents of those four folders and copy the correct version from the simplesaml_backups folder.

![folders1](..images/simplesamlfolder1.PNG)
![folders2](..images/simplesamlfolder2.PNG)

After replacing these folders/files, adding the missing pieces to the htaccess file, and clearing the cache, you should be able to get to the actual dev website as well as the /simplesaml admin screen. Commit the code and start testing.

I'd like to be able to automate the testing of the sites after running these updates. There must be some automated testing tools available.
