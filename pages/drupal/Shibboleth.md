---
layout: default
---

# Setting Up Netbadge SSO with Acquia Cloud Enviroments

[UVA provides this tutorial](http://its.virginia.edu/netbadge/unixdevelopers.html) about how to setup Shibboleth software on a website. However, Acquia Cloud doesn't support shibboleth software for their instances since they don't allow access to their Apache instances. I need to find a way to enable SSO using SimpleSAML.

[This Acquia Cloud  Tutorial](https://docs.acquia.com/articles/using-simplesamlphp-acquia-cloud-site) has an overview of the process for setting up SSO. Below are the steps I actually tried:

## Goal - get SSO working in Development enviroment

1. Download the SimpleSAMLphp library
2. Put the library next to the docroot folder
3. Make a symbolic link to the www folder of the simplesaml library so it is visible to the webserver.
`cd docroot; ln -s ../simplesamlphp/www simplesaml`
4. Install the Externalauth module and the simplesamlphp_auth modules. When trying to enable the simplesamlphp_auth module, I get an error that the SimpleSAMLphp library isn't isntalled or configured.
### Get the SimpleSAMLphp library configured
5. Edit the config.php file
I edited some basic info in the config.php file of the simplesaml library installation
```
`'auth.adminpassword' => 'DefaultPassword!1',`
`'technicalcontact_name' => 'Miles_Greatwood',`
`'technicalcontact_email' => 'miles.gwoood@gmail.com',`
```
 6. Edit the .htaccess file in docroot
  -Add the two lines with + diff to the docroot/.htaccess
```
  # Copy and adapt this rule to directly execute PHP files in contributed or
  # custom modules or to run another PHP application in the same directory.
   RewriteCond %{REQUEST_URI} !/core/modules/statistics/statistics.php$
  + #Allow access to simplesaml paths
  + RewriteCond %{REQUEST_URI} !^/simplesaml
  # Deny access to any other PHP files that do not match the rules above.
  # RewriteRule "^.+/.*\.php$" - [F]
```
7. After editing the htaccess file I no longer get errors when trying to access the simplesaml module web interface.
I did not need to follow the rest of this [SimpleSAMLphp library installation](https://simplesamlphp.org/docs/stable/simplesamlphp-install) since the Acquia Cloud tutorial above already had me create the symbolic link in the docroot folder.
8. Now I need to [configuring the Service Provider](https://simplesamlphp.org/docs/stable/simplesamlphp-sp). The SP  is what talks to the UVA idP or identity provider to facilitate the authentication and retrieval of needed session cookies from the idP.
9. In config/authsources.php I left all fields null so they would auto configure with the exception of the idp for my default-sp array. I changed the idp to  
`'idp' => 'urn:mace:incommon:virginia.edu',`
10. Continuing with the SP configuration I created a self signed cert in the cert directory.
```
openssl req -newkey rsa:2048 -new -x509 -days 3652 -nodes -out saml.crt -keyout saml.pem
```
11. Using [this XML file for the UVA IDP](https://shibidp.its.virginia.edu/shibboleth/uva-idp-metadata.xml) I used the converter in the simplesaml web interface to get the php needed for saml20-idp-remote.php and shib13-idp-remote.php in the metadatafolder of the simplesamlphp library. The converter is found at an address similar to this `http://uvacooper.test.dd:8083/simplesaml/admin/metadata-converter.php`

At this point I need to make a request to ITS so that the idP server will talk with my newly created SP.

Made a request using the generated XML file with the stage server's local entity ID and information.
Request ID REQ0040191

Request denied and told to talk with Chris Klein (cdk4f) to find out where I fucked up.

# Questions
[]  What resources do I need from the idP server? Just the uid / computing ID?
[]  How do I request idP access for all of our servers (dev and production)

# To Do
[]  Get ITS accept my metadata for the dev server and repeat for the live server.
[]  Change the storage of session objects to sql storage like the Acquia tutorial states
[]  Finish simplesaml_auth module setup
[]  Figure out how to create user accounts on Drupal side with the Netbadge credentials

This lists the information we'll get as a non UVA non InCommon Federation SP
http://its.virginia.edu/netbadge/defaultpolicy.html

Since we're not using Shibboleth I have no idea how to use this information on this site here
http://its.virginia.edu/netbadge/unixdevelopers.html

So I'm still working on setting up the SP since I can't get a response from the IDP until they approve my request.
https://simplesamlphp.org/docs/stable/simplesamlphp-sp

Next is configuring the actual plugin and setting up database storage of the identity records.
https://docs.acquia.com/articles/using-simplesamlphp-acquia-cloud-site
https://www.drupal.org/project/simplesamlphp_auth

Simple Saml module acquia install - https://docs.acquia.com/articles/using-simplesamlphp-acquia-cloud-site
