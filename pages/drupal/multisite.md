---
layout: default
---

# Multisite installation

Use the auto creation tool for multisite on Acquia Dev Desktop
https://docs.acquia.com/dev-desktop/multisite

[Drupal Documentation](https://www.drupal.org/docs/7/multisite-drupal/multi-site-sharing-the-same-code-base)

## Troubleshooting guide

For installing permission on sites/default should be 755 [drwxr-xr-x]:

`ls -l sites/`

`chmod 755 sites/default`

For the install permission on settings.php should be 644 [-rw-r--r--]:

`ls -l sites/default/settings.php`

`chmod 644 settings.php `

At all times files folder should be 755
Inside the files folder should be 775 if 755 isn't working

`chmod -R 755 sites/default/files`

I edited the crap out of the http.conf file for Apahce
/private/etc/apache2/http.conf
/private/etc/apache2


## After install you need to set settings to read only and default to read execute.

`chmod 555 sites/default`

`chmod 444 sites/default/settings.php`

I am having no success getting the install to work with the subdomain of http://sei.coopercenter.org:8083/install.php.
