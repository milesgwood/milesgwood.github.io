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
