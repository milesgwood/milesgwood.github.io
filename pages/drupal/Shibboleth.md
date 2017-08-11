---
layout: default
---

# Setting Up Netbadge SSO with Acquia Cloud Enviroments

[UVA provides this tutorial](http://its.virginia.edu/netbadge/unixdevelopers.html) about how to setup Shibboleth software on a website. However, Acquia Cloud doesn't support shibboleth software for their instances since they don't allow access to their Apache instances. I need to find a way to enable SSO using SimpleSAML.

[This Acquia Cloud  Tutorial](https://docs.acquia.com/articles/using-simplesamlphp-acquia-cloud-site) has an overview of the process for setting up SSO. Below are the steps I actually tried:

Mary Beth directed me to [another walkthrough](http://valuebound.com/resources/blog/how-to-configure-single-sign-on-across-multiple-drupal-8-platforms-or-websites) that describes getting Simplesamlphp to work with Drupal 8.

## Goal - get SSO working in Development enviroment

1. Download the SimpleSAMLphp library
2. Put the library next to the docroot folder
3. Make a symbolic link to the www folder of the simplesaml library so it is visible to the webserver.
`cd docroot; ln -s ../simplesamlphp/www simplesaml`
4. Install the Externalauth module and the simplesamlphp_auth modules. When trying to enable the simplesamlphp_auth module, I get an error that the SimpleSAMLphp library isn't installed or configured.
## Get the SimpleSAMLphp library configured
5. Edit the config.php file
 - You need to add where the information about authenticated users will be stored. It goes into the netbadge database that you created on Acquia Cloud. Set a $sqldsn , $sqlusername, and $sqlpassword for each of the possible environments.
 - Inside of the config array
    - baseurlpath
    - certdir
    - showerrors => true
    - errorreporting => true
    (These previous two need to be false in a live enviroment after this is all set up)
    - auth.adminpassword
    - secretsalt
    - technicalcontact_name
    - database.dsn => '$sqldsn'  <-- This was set outside of config array in previous bullet
    - database.username => $sqlusername
    - database.password => $sqlpassword

    ```php
    if (isset($_ENV['AH_SITE_ENVIRONMENT'])) {
    switch ($_ENV['AH_SITE_ENVIRONMENT']) {
        case 'dev':
            $sqldsn = 'mysql:host=127.0.0.1;dbname=netbadge';
            $sqlusername = 'username';
            $sqlpassword = ''******';';
            break;
            //Change these credentials later from acquia
        case 'test':
            $sqldsn = 'mysql:host=127.0.0.1;dbname=netbadge';
            $sqlusername = 'theusernameonAcquiaCloud';
            $sqlpassword = '******';
            break;
        case 'prod':
            $sqldsn = 'mysql:host=dbmaster-17482.prod.hosting.acquia.com;dbname=netbadge';
            $sqlusername = 'theusernameonAcquiaCloudForThisEnviroment';
            $sqlpassword = ''******';';
            break;
    }
}
```
Here's some of the variables in the config array:
```php    
'baseurlpath' => 'https://' . $_SERVER['SERVER_NAME'] . '/simplesaml/',
    'certdir' => 'cert/',
    'loggingdir' => 'log/',
    'datadir' => 'data/',
```

   Database credentials

    ```php
    'database.dsn' => $sqldsn,
    'database.username' => $sqlusername,
    'database.password' => $sqlpassword,
    ```

 6. Edit config/authsources.php
  ```php
  //Duplicate these Miles for more SP on each server using different entity ID
  'cooper-dev-sp' => array(
    'saml:SP',
    'entityID' => 'https://uvacooperdev.prod.acquia-sites.com',
    'idp' => 'urn:mace:incommon:virginia.edu' ,
    'privatekey' => 'saml.pem',
    'certificate' => 'saml.crt',
    'discoURL' => null,
),
```
## SSL is required
You must use the https:// URL because simplesaml will not work without it. You can't securely authenticate if you can't securely connect.

 7. Edit the .htaccess file in docroot
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
After editing the .htaccess file I no longer get errors when trying to access the simplesaml module web interface.
I did not need to follow the rest of this [SimpleSAMLphp library installation](https://simplesamlphp.org/docs/stable/simplesamlphp-install) since the Acquia Cloud tutorial above already had me create the symbolic link in the docroot folder.

8. Now I need to [configuring the Service Provider](https://simplesamlphp.org/docs/stable/simplesamlphp-sp). The SP  is what talks to the UVA idP or identity provider to facilitate the authentication and retrieval of needed session cookies from the idP.

9. In config/authsources.php I left all fields null so they would auto configure with the exception of the idp for my default-sp array. I changed the idp to  
`'idp' => 'urn:mace:incommon:virginia.edu',`

10. Continuing with the SP configuration I created a self signed cert in the cert directory.
```
openssl req -newkey rsa:2048 -new -x509 -days 3652 -nodes -out saml.crt -keyout saml.pem
```

11. Using [this XML file for the UVA IDP](https://shibidp.its.virginia.edu/shibboleth/uva-idp-metadata.xml) I used the converter in the simplesaml web interface to get the php needed for saml20-idp-remote.php and shib13-idp-remote.php in the metadatafolder of the simplesamlphp library. The converter is found at an address similar to this `http://uvacooper.test.dd:8083/simplesaml/admin/metadata-converter.php`

### Request Specifics
These requests are needed for each of the environments we'll be working in. Dev and Production are the main focuses. The request is made to virginia.service.now
![First Part of idP Request](../../assets/images/idP_request0.png)
Get the URL for the metadata from the simplesaml web interface. domain/simplesamlphp
![Second Part of idP Request](../../assets/images/idP_request.png)


# To Do
- [x] Downlaod library and make it visible
- [ ] Get ITS accept my metadata for the dev server and repeat for the live server.
- [x] Change the storage of session objects to sql storage like the Acquia tutorial states
- [ ] Finish simplesaml_auth module setup
- [ ] Figure out how to create user accounts on Drupal side with the Netbadge credentials

[Description of UVA info from idP ](http://its.virginia.edu/netbadge/defaultpolicy.html)

[Garbage UVA walkthrough that you can't use since you can't access Apache.](http://its.virginia.edu/netbadge/unixdevelopers.html) It does have a link to the needed XML metadata of the UVA idP

[simplesamlphp_auth Plugin](https://www.drupal.org/project/simplesamlphp_auth)

[Acquia Walkthrough](https://docs.acquia.com/articles/using-simplesamlphp-acquia-cloud-site)

[Another walkthrough that is Drupal 8 specific](http://valuebound.com/resources/blog/how-to-configure-single-sign-on-across-multiple-drupal-8-platforms-or-websites)
