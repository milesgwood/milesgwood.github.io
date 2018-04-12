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

Install and enable the externauth and simplesamlphp modules. You get this error from the simplesaml enabling because the php library still needs to be set up according to [this documentation.](https://simplesamlphp.org/docs/stable/simplesamlphp-sp)
```
Warning: include_once(/lib/_autoload.php): failed to open stream: No such file or directory in simplesamlphp_auth_check_library() (line 82 of modules/simplesamlphp_auth/simplesamlphp_auth.install).
Warning: include_once(): Failed opening '/lib/_autoload.php' for inclusion (include_path='.:/Applications/DevDesktop/common/pear:/usr/lib/php') in simplesamlphp_auth_check_library() (line 82 of modules/simplesamlphp_auth/simplesamlphp_auth.install).
SimpleSAMLphp module requires the simplesamlphp library. See README file for installation instructions.
```

## Get the SimpleSAMLphp library configured
5. Edit the config.php file
I just copied all of the data from the 1.14 version that I already had. Edits to config php will go at the bottom of this
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
 I just straight up copied the data from the old authsources too. I changed the entityID to https://supportdev1.coopercenter.org/

 For the privatekey and the certificate I am going to use the UVA supplied one instead of the senf signed one I tried this with initially. I did not add any of the CA chain certificates.


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
You must use the https:// URL because simplesaml will not work without it. You can't securely authenticate if you can't securely connect. Getting  SSL certificate is easy. Simply make the request on the acquia enterprise account under the SSL tab. They'll give you a key which you send to your SSL provider. In our case, this is UVA service now. They send you back a bunch of certificates and you copy the certificates to Acquia through the same page you got the key to make your request. In the top box put the X509 Certificate only, Base64 encoded. In the intermediaries box put the X509 Intermediates/root only Reverse, Base64 encoded certificate. This is a standard certificate, not a legacy one. Now back to the actual simplesaml work.  

So I got a SSL certificate that covers sigle level subdomains of coopercenter.org. The support dev site I want to get SSO working for is https://supportdev1.coopercenter.org. So I need to follow the acquia tutorial on how to get SimpleSAMLphp working.

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

## Reference Docs

[Description of UVA info from idP ](http://its.virginia.edu/netbadge/defaultpolicy.html)

[Garbage UVA walkthrough that you can't use since you can't access Apache.](http://its.virginia.edu/netbadge/unixdevelopers.html) It does have a link to the needed XML metadata of the UVA idP

[simplesamlphp_auth Plugin](https://www.drupal.org/project/simplesamlphp_auth)

[Acquia Walkthrough](https://docs.acquia.com/articles/using-simplesamlphp-acquia-cloud-site)

[Another walkthrough that is Drupal 8 specific](http://valuebound.com/resources/blog/how-to-configure-single-sign-on-across-multiple-drupal-8-platforms-or-websites)

[UVA Dev docs](http://its.virginia.edu/netbadge/developers.html)
[UVA Shibboleth No good for SimpleSaml]http://its.virginia.edu/netbadge/unixdevelopers.html)



SWITCHED DEV branch to SSO. TO just work on site use the support branch instead.

Questions.
1. Why does support.dd:8083/simplesaml not work but https://supportdev1.coopercenter.org/simplesaml does?
2. Should the cert directory have my self signed cert and private key OR the UVA supplied cert and private key? (It's purpose is to identify the SP-supportdev1.cooperceter.org to the idp-urn:mace:incommon:virginia.edu)
3. What data should I be sending to UVA ITS?
4. Are the CA chain certs needed too? or just the main cert and private key.


So I have the simplesaml interface working on the dev site. I am going to parse the XML metadata from `https://shibidp.its.virginia.edu/shibboleth/uva-idp-metadata.xml` in the parser on the simplesaml admin interface here `:8083/simplesaml/admin/metadata-converter.php`.

This makes me think that the metadata is not correct for the dev site simplesaml. I was told I need a saml20-idp-remote.php file and a shib13-idp-remote.php file.

So I got it working with the old version, now I just need to get the site registered as an authorized SP.

## Success!!!

After going to the `supportdev1.coopercenter.org/simplesaml` url and entering the old password for the admin account, I went to the test configured SP. I got directed to netbadge which allowed me to login and returned values for my user account's session. How do I use these values to actually sake and sign in to a drupal account?

```
Your attributes
urn:oid:1.3.6.1.4.1.5923.1.1.1.9
staff@virginia.edu
employee@virginia.edu
member@virginia.edu
urn:oid:1.3.6.1.4.1.5923.1.1.1.1
member
staff
employee
urn:oid:2.5.4.4	Greatwood
urn:oid:2.5.4.42	Miles
urn:oid:1.3.6.1.4.1.5923.1.5.1.1
cn=WEB_NAS,ou=Groups,o=University of Virginia,c=US
cn=vprgs,ou=Groups,o=University of Virginia,c=US
cn=fm_registrations,ou=Groups,o=University of Virginia,c=US
cn=fm_clients,ou=Groups,o=University of Virginia,c=US
cn=CCPS_NAS,ou=Groups,o=University of Virginia,c=US
cn=ccps_shared_mailbox,ou=Groups,o=University of Virginia,c=US
cn=fm_csr_admin,ou=Groups,o=University of Virginia,c=US
cn=fm_readonly,ou=Groups,o=University of Virginia,c=US
urn:oid:0.9.2342.19200300.100.1.3	mg9jd@Virginia.EDU
SAML Subject
NameId	_1ddda62656c77db3b323d43e1b13d5da
Format	urn:oasis:names:tc:SAML:2.0:nameid-format:transient```
```

Even though the idP worked correctly. When I tried to install the simplesaml drupal module it failed.
```
Warning: include_once(/lib/_autoload.php): failed to open stream: No such file or directory in simplesamlphp_auth_check_library() (line 82 of modules/simplesamlphp_auth/simplesamlphp_auth.install).

Warning: include_once(): Failed opening '/lib/_autoload.php' for inclusion (include_path='.:/var/www/html/uvacooperdev/library/:/usr/share/php:/usr/share/pear') in simplesamlphp_auth_check_library() (line 82 of modules/simplesamlphp_auth/simplesamlphp_auth.install).

SimpleSAMLphp module requires the simplesamlphp library. See README file for installation instructions.
```

### Failed Ideas
1. I tried manually setting the location of the simplesamlphp library in autoload and that caused 500 server issues.
2. I tried requiring composer to add simplesamlphp/simplesamlphp and that failed because it doesn't import the configurations I painfully setup.

So since I had moved the simplesamlphp library files it wasn't finding them. The symlink that acquia requires I do made the `lib/_autoload.php` file and the config file impossible for the drupal module to find. I need to add some info according to the part 13 of [this tutorial](https://simplesamlphp.org/docs/stable/simplesamlphp-install#section_13)

Now, we need to make a few configuration changes. First, let's edit `~/public_html/simplesaml/_include.php:`

Change the two lines from:
```
require_once(dirname(dirname(__FILE__)) . '/lib/_autoload.php');
```
to something like:
```
require_once('/var/www/html/uvacooperdev/old-attempt-simplesamlphp-1.14.15/lib/_autoload.php');
```
And then at the end of the file, you need to change another line from:
```
$configdir = dirname(dirname(__FILE__)) . '/config';
to:
$configdir = '/var/www/html/uvacooperdev/old-attempt-simplesamlphp-1.14.15/config';
```

I found that those changes didn't solve the missing library problem which makes sense since they are inside the library files that I can't seem to get the module to find. I went to the module's README and found this.

```
## INSTALLATION WITHOUT COMPOSER

1. Make sure you have a working SimpleSAMLphp installation. It needs to be a
standalone installation, which has a "vendor" folder in the root of the project.
2. Download the simplesamlphp_auth module
3. Uncompress it
4. Move it to the appropriate modules directory (usually, /modules)
5. In your settings.php file, add the location of your SimpleSAMLphp
installation (no trailing slashes):
```
So I need to edit my settings.php file by adding this to the support site's settings.php file.
```
$settings['simplesamlphp_dir'] = '/var/www/html/uvacooperdev/old-attempt-simplesamlphp-1.14.15';
```

SUCCESS!!!!! From now on if you see a variable is missing like this variable `$dir = Settings::get('simplesamlphp_dir');`, you should code it into the site's settings.php file. That code is querying the settings array for that specific website.

Now you can enable SimpleSaml SSO [through the account settings page!!!!](https://supportdev1.coopercenter.org/admin/config/people/accounts)

Now the module is active but I don't know how to connect it to the actual login for the site. Also, I can't seem to logout of the site anymore either. 
