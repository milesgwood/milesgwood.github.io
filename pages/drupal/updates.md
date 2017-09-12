---
layout: default
---

I want to update the drupal core files from 8.3.5 to 8.3.7 using drush on my local installation. [Here's a fantastic walkthrough for the update process.](https://www.drupal.org/docs/8/update/update-procedure-in-drupal-8).

First you need to put the site in to maintenance mode/
`drush maintenance_mode 1`

Then Rebuild the cache. This is a great command to run if you can't access the actual clear cache button.

`drush cr`

##Execute the updates:

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
