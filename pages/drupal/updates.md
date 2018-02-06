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
