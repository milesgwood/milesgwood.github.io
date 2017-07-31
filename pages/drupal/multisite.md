---
layout: default
---

# Multisite installation

Use the auto creation tool for multisite on Acquia Dev Desktop
https://docs.acquia.com/dev-desktop/multisite

[Drupal Documentation](https://www.drupal.org/docs/7/multisite-drupal/multi-site-sharing-the-same-code-base)

##Troubleshooting guide

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

#DNS

All of the sites have the same DNS
52.87.30.162

C:\Users\miles>tracert coopercenter.org
This is the ip address for the old site.
  54.227.239.108


  Main site - coopercenter.org
    54.227.239.108
  ceps.coopercenter.org -  Economic Policy
  csr.coopercenter.org - Survey Research
  certification.coopercenter.org - Constitutional officers cert
  sei.coopercenter.org - Lead trainings
  sorenseninstitute.org - Political leadership
  uip.coopercenter.org - university internship programs x
  vig.coopercenter.org - Virginia Institute of gov
    52.44.228.42
  demographics.coopercenter.org - Demographics
    128.143.21.13
