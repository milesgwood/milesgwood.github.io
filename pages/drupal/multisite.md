---
layout: default
---

# Multisite installation
I want to easily duplicate the home site so that I can create the unit page sites and enjoy my family's vacation in 2 weeks. The moon is going to block out the fucking sun and I'm not gonna miss that little cheesy bastards big moment.

Use the auto creation tool for multisite on Acquia Dev Desktop. Make sure you use the correct names for the sites when you make them so that the dev site matches the live site except for the domain. The subdomains should all match.
https://docs.acquia.com/dev-desktop/multisite

The Acquia documentation provides a lot of useful information but it is all handled by dev desktop so don't worry too much about it all. My goal is to use the Backup and Migrate module to effectively clone a site with Acquia handling all of the pesky environment issues.

1. Pull the site that you want to copy from live server
2. Make a new multisite using Dev Desktop > More > New Multisite
3. Go to the local site of the new site you just made. Make sure the URL looks correct
4. Follow the installation procedure just as you would with an ordinary new site
5. Enter the same admin password for the site as all other sites

[Drupal Documentation](https://www.drupal.org/docs/7/multisite-drupal/multi-site-sharing-the-same-code-base)

# Backup And Migrate Module

Now that we have our new empty site, we need to populate it. The easiest way to do this is with the Backup and Migrate tool.
1. Enable the backup tool on the new site. If it won't appear in Config > Development > Backup & Migrate , then uninstall and reinstall it
2. Make a backup of the site you want to copy. You need to get the Public Files folder and the Default Drupal Database. Save them locally and name them so you know which is files and which is the database.
3. Upload the files to the new empty site.
4. Upload the database to the new site.
5. Clear Cache in developer tools
6. Start working on the new site you just successfully cloned

# Launching the new site after changes are made

Since this is a sprint. I want to take this process all the way to completion so I know that my method will work. I want to launch my copied site with a few extra pieces of content on my actual domain. moebot.audio is the domain and I'll add lead.moebot.audio to the start of the domain. I'm sure there is some piece of code I have to edit to ensure that Acquia actually navigates to the correct site.

You must edit the sites.php file so that it explains to drupal what folders are needed to properly display the site. Once those code changes are committed, then you need to make sure that Acquia is on the correct branch so that those code  changes actually show up. Go into the Acquia Evironment and switch the code to the correct branch. 

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
