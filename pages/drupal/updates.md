---
layout: default
---

I want to update the drupal core files from 8.3.5 to 8.3.7 using drush on my local installation. [Here's a fantastic walkthrough for the update process.](https://www.drupal.org/docs/8/update/update-procedure-in-drupal-8).

First you need to put the site in to maintenance mode/
`drush maintenance_mode 1`

Then Rebuild the cache. This is a great command to run if you can't access the actual clear cache button.

`drush cr`

## Execute the updates:

This no longer works in Drupal 8.4

Update Drupal core: `drush up drupal`

Update a single module: `drush up module_name`

Only apply security updates: `drush up --security-only`

Now bring it out of maintenance mode and clear the cache again.
```
drush sset system.maintenance_mode 0
drush cr
```

## Databse updates

After updating modules you have to run databsae updates as well. I ran into problems because I had no config directory declared in the settings.php file. I manually added one [according to this support ticket.](https://www.drupal.org/node/2782367). I found the directory in the files folder for that particular site.

Line 252
```
$config_directories = array(
    CONFIG_SYNC_DIRECTORY => 'sites/lead/files/config_4b06c7b07661b7a22f353e8a7a5d4b246c3ee2d8'
);
```

# Updating Drush Itself

For the upgrade from 8.3 to 8.4 I need to update drush otherwise the Drupal Core Update will fail.

Check your drush version with `drush version` I am running 8.1.10. I have Composer installed globally so I will use that to update drush. Composer version 1.5.2

From docroot add drush to the composer file with `composer require drush/drush`. Running `composer update` just updates composer. I don't know if it updates drush because after running require drush drush I already had drush version 8.1.14. I can now run the drupal update process as I have listed above.

Or you can use composer to update to a specific version of drush
```
composer require drush/drush:9.*
drush version
```

## Troubleshooting

When running drush commands I got an error
```
Error: Declaration of Drush\Command\DrushInputAdapter::hasParameterOption($values) must be compatible with Symfony\Component\Console\Input\InputInterface::hasParameterOption($values, $onlyParams = false) in /Applications/DevDesktop/tools/vendor/drush/drush/lib/Drush/Command/DrushInputAdapter.php, line 27
d-172-25-19-187:docroot miles$ drush --version
 Drush Version   :  8.1.10
```

I upgraded to Drush 8.1.15 `composer require drush/drush:8.1.15` and the problem went away. Drush 9 had a different problem where the command i wanted to use was not defined even after a cache clear.
```
[Symfony\Component\Console\Exception\CommandNotFoundException]  
 Command "migrate-import" is not defined.
```

## Editing your bash profile
```
PATH=$PATH:/usr/local/bin/drushphar
export PATH
```

This creates the added item in just one users bash profile.
Place that code, or whatever part of that code isn't already incorporated, in one of the following places:

One user = $HOME/.bash_profile
All users except root = /etc/profile
root = /root/.bash_profile

You can open and see the bash profile with this.
```
touch ~/.bash_profile; open ~/.bash_profile
```

Working Bash Profile Format
```
export PATH=$PATH:/usr/local/bin/drushphar
export PATH=$PATH:/Applications/DevDesktop/tools

[[ -s ‘$HOME/.rvm/scripts/rvm’ ]] && source ‘$HOME/.rvm/scripts/rvm’ # Load RVM into a shell session *as a function*
source ~/.profile
```

Results of echo $PATH
```
echo $PATH

/Users/miles/.rvm/gems/ruby-2.4.1/bin:/Users/miles/.rvm/gems/ruby-2.4.1@global/bin:/Users/miles/.rvm/rubies/ruby-2.4.1/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/local/share/emacs/site-lisp/ruby:/usr/local/munki:/usr/local/bin/drushphar:/Applications/DevDesktop/tools:/Users/miles/.rvm/bin
```

# Manual Update of Drupal- ! WORKS

Drush and Composer failed to update Drupal correctly. So I opted to manually update Drupal to 8.4.0. Just delete everything except for sites themes modules and profiles. Core and Vendor are the core files and dependencies that need updating. By doing this update you lose all of the custom changes made to all the other files so back things up.

You have to re add these changes after the update of core files and the following database updates. These go into htaccess

```
<IfModule mod_setenvif.c>
  # Added to block a high-traffic IP address
  SetEnvIf AH_CLIENT_IP ^151\.80\.27\.116 $ DENY=1
  SetEnvIf AH_CLIENT_IP ^46\.229\.168\.65 $ DENY=1
  SetEnvIf AH_CLIENT_IP ^217\.182\.132\.25 $ DENY=1
  SetEnvIf AH_CLIENT_IP ^217\.182\.132\.32 $ DENY=1
  Order allow,deny
  Allow From All
  Deny from env=DENY
</IfModule>
```

Updating the site brought with it some errors from jQuery. The bind method became depracated which was easy to replace with the on() method. The trickier problem was a new error in bootstrap caused by a file loaded by a CDN bootstrap.js has an error where it tries to select $("#") which now is an error and breaks all dropdowns. My solution is to make my own edited custom version of the js and host it on my github.


# Manual edits to drupal

I want to exclude lost data from the database:

/Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/modules/node/src/Plugin/Search/NodeSearch.php

So I added a condition to the where clause in the updateIndex method.
Updated version of the update code.
```
/**
   * {@inheritdoc}
   */
  public function updateIndex() {
    // Interpret the cron limit setting as the maximum number of nodes to index
    // per cron run.
    $limit = (int) $this->searchSettings->get('index.cron_limit');

    $sub = db_select('node');
    $sub->addField('node', 'nid');
    $sub->condition('node.type', 'lost', '<>');

    $query = db_select('node', 'n', ['target' => 'replica']);
    $query->addField('n', 'nid');
    $query->leftJoin('search_dataset', 'sd', 'sd.sid = n.nid AND sd.type = :type', [':type' => $this->getPluginId()]);
    $query->addExpression('CASE MAX(sd.reindex) WHEN NULL THEN 0 ELSE 1 END', 'ex');
    $query->addExpression('MAX(sd.reindex)', 'ex2');

    $query->condition(
        $query->andConditionGroup()
            ->condition('n.nid', $sub, 'IN')
            ->condition(
            $query->orConditionGroup()
              ->where('sd.sid IS NULL ')
              ->condition('sd.reindex', 0, '<>')
      ));
    $query->orderBy('ex', 'DESC')
      ->orderBy('ex2')
      ->orderBy('n.nid')
      ->groupBy('n.nid')
      ->range(0, $limit);


    $nids = $query->execute()->fetchCol();
    if (!$nids) {
      return;
    }

    $node_storage = $this->entityManager->getStorage('node');
    foreach ($node_storage->loadMultiple($nids) as $node) {
      $this->indexNode($node);
    }
  }
```

## Updating Drupal to 8.5.0-rc1

Updating to the release candidate since it doesn't seem to be causing issues

Error on drush cr after the replacing of the core files. Replaced everything except modules profiles sites and themes. Delete everything else that the new core offers.

```
drush cr

PHP Fatal error:  Declaration of Drush\Command\DrushInputAdapter::hasParameterOption() must be compatible with Symfony\Component\Console\Input\InputInterface::hasParameterOption($values, $onlyParams = false) in /Applications/DevDesktop/tools/vendor/drush/drush/lib/Drush/Command/DrushInputAdapter.php on line 27

composer require drush/drush:8.1.16
```

After uninstalling the backup migrate plugin I got this error. Solution is to run the database updates BEFORE uninstalling any plugins or anything. Run updates as an atomic action.

```
Drupal\Core\Entity\Exception\UnsupportedEntityTypeDefinitionException: The entity type block_content does not have a "published" entity key. in Drupal\Core\Entity\EditorialContentEntityBase::publishedBaseFieldDefinitions() (line 32 of /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Core/Entity/EntityPublishedTrait.php).
Drupal\Component\Plugin\Exception\PluginNotFoundException: The "file_uri" plugin does not exist. in Drupal\Core\Plugin\DefaultPluginManager->doGetDefinition() (line 52 of /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Component/Plugin/Discovery/DiscoveryTrait.php).
```

Another Error after running the database updates
```
views module
Update #8500
Failed: Drupal\Core\Entity\Exception\UnsupportedEntityTypeDefinitionException: The entity type block_content does not have a "published" entity key. in Drupal\Core\Entity\EditorialContentEntityBase::publishedBaseFieldDefinitions() (line 32 of /Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Core/Entity/EntityPublishedTrait.php).
```

The site seems to still work despite this error on the views module database update. After a second run of update.php the site seems to have completed all of the core updates correctly.

A bunch of the modules required the contribute module to perform their database updates so I copied it to the modules directory.

The site is running really slow after this update. It's really struggling to bring up the admin pages.

Secondary update of migrate tools and migrate plus was needed.

Sorensen looks great but the rest of the sites are broken now. I don't know if it is the drupal update or the modules that caused but I expect it is the core update that did it. I'm going to attempt to update the sei site with drush instead of the regular gui. If this all fails then I will just revert to the site on Stage which is pre-update.

So to update drush I have to get composer the right kind of drush. My global install of composer is using drush/drush dev-master. So maybe if I update drush there I will get it inside my project. The global composer file is stored at `composer global update`

```
composer global update
```

I edited the global composer file to have this in it.
```
{
    "require": {
        "drush/drush": "8.1.16"
    }
}
```

I am failing to update drush with composer. [Tutorial](https://drupal.stackexchange.com/questions/222188/updating-drush-with-composer). Requiring a newer version of drush worked to get `drush cr` working. I want to see if it will work with updating drupal.

```
composer require drush/drush
drush --version
9.2.1
```
In this version the update command is deprecated.
```
drush ups

The pm-updatestatus command was deprecated. Please see `composer show` and `composer outdated`. For security release notification, see `drush pm:security`.  
```

## Update Drupal and Modules with Drush

With drush 9.2.1 I can now downgrade to drush 8.1.16 [Here's how to actually preform the update.](https://www.drupal.org/docs/8/update/update-core-via-drush-option-3)
```
composer require drush/drush:8.1.16  

drush --version
 Drush Version   :  8.1.16

cd sites/sei
drush ups
drush up
drush updb
drush entup
```

Error on sorensen after sei update
```
exception 'Drupal\Component\Plugin\Exception\PluginNotFoundException' with message 'The "group_permission" plugin does not exist.' in  [error]
/Users/miles/Sites/devdesktop/uvacooper-dev/docroot/core/lib/Drupal/Component/Plugin/Discovery/DiscoveryTrait.php:52
Stack trace:

drush cr
drush en group_permission
```

1. Pull database from live environment
2. Make sure you have drush 8.1.16 (if not `composer require drush/drush` and `composer require drush/drush:8.1.16`)
3. Run ` drush cr and drush ups` to make sure drush is working
4. Copy Core files over  (this may revert you back to the previous version of drush and you'll need to repeat previous steps)
5. cd into sites/sorensen
6. Run `drush updb` to get the database updates for the core update
7. Run `drush entup`
8. Run `drush up` for the module updates
9. Run `drush updb`
10. Run `drush entup`

```
Local site is fine but live site gives this Error - FIXED BY ANOTHER DEV DEXKTOP PUSH

The website encountered an unexpected error. Please try again later.</br></br><em class="placeholder">Symfony\Component\HttpKernel\Exception\AccessDeniedHttpException</em>:  in <em class="placeholder">Drupal\Core\Routing\AccessAwareRouter-&gt;checkAccess()</em> (line <em class="placeholder">114</em> of <em class="placeholder">core/lib/Drupal/Core/Routing/AccessAwareRouter.php</em>).
```

Had to enable contribute module before last database update
```
drush en -y contribute
drush updb
```

# Drupal Updates

Want to update drupal to 8.5.4 from 8.5.3. So update core first, then test. Then update modules, database, entities and test again.

1. Download all the current site databases from production.
2. Pull the code form production.
3. Replace the Drupal core files manually.
4. Update the database and entities  
5. Update all the modules
6. Test

### Copying Core Files over

Download the latest core files. Select all of the contents of the new core files EXCEPT modules profiles sites and themes folders.

DO NOT COPY
- modules
- profiles
- sites
- themes

### Runing the drush updates

```
drush --version
composer require drush/drush:8.1.16
cd sites/support
drush cr
drush ups
drush updb
drush entup
```

### Troubleshooting

I'm attempting to update the webform module separately since it is causing issues. I made some manual edits to the simplesamlphp module code so now I can't update the module without recreating the edits in the updated module. I'll leave it alone for now.

- Manually transfer the Webform module code and then run drush updb
- Don't update the simplesamlphp module
- Don't update the Quick Node Clone module

# Cloud9 Updates

Since Dev Desktop takes forever to actually copy the databases, I will perform all my code and cored updates on cloud9 now. It connects directly to the DEV environment so I can quickly copy all of the databases from the live sites if something goes wrong. Then I can run the script to preform all of the database updates.

1. Sync Databases from the live sites
2. Create a new branch using the SSH connector on dev desktop or by simply connecting directly with command
```
ssh uvacooper.dev@staging-17490.prod.hosting.acquia.com
git branch my-new-branch
git checkout my-new-branch
git push
git push --set-upstream origin core-8-5-6
```
3. Copy the core code for updates and extract it to the correct folders. Replace everything except sites, themes, .htaccess, and modules. (optional module updates here too)
```
weget https://ftp.drupal.org/files/projects/drupal-8.5.6.tar.gz
tar -xzf drupal-8.5.6.tar.gz
```
4. Clear the cache with `drush cr` and then clear the varnish on acquia
5. Verify all the dev sites are working and you can sign in.
6. Run the DB update script that's above the docroot
7. Test the sites on dev
8. Test the sites on stage
9. Copy all DB and swith the code on live
10. Clear cache and debug errors on all live sites

# Delete erroneous table manually from dev database

```
ssh -i priv_key staging-17490.prod.hosting.acquia.com
mysql -u xxxxx -p
enter the password on the database page
SHOW DATABASES;
USE xxxxxx;
DROP TABLE entity_usage;
```

Looks like 4 sites are using a module that requires entity_usage without having it.

```
drush pm-uninstall paragraphs_library
```
