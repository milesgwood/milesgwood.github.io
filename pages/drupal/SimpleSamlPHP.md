---
layout: default
---

# Setting Up Netbadge SSO with Acquia Cloud Enviroments

[UVA provides this tutorial](http://its.virginia.edu/netbadge/unixdevelopers.html) about how to setup Shibboleth software on a website. However, Acquia Cloud doesn't support shibboleth software for their instances since they don't allow access to their Apache instances. I need to find a way to enable SSO using SimpleSAML.

[This Acquia Cloud  Tutorial](https://docs.acquia.com/en/stable/resource/using-simplesamlphp-acquia-cloud-site/) has an overview of the process for setting up SSO. Below are the steps I actually tried:

Mary Beth directed me to [another walkthrough](http://valuebound.com/resources/blog/how-to-configure-single-sign-on-across-multiple-drupal-8-platforms-or-websites) that describes getting Simplesamlphp to work with Drupal 8.

## SSL is required
You must use the https:// URL because simplesaml will not work without it. You can't securely authenticate if you can't securely connect. Getting  SSL certificate is easy. Simply make the request on the acquia enterprise account under the SSL tab. They'll give you a key which you send to your SSL provider. In our case, this is UVA service now. They send you back a bunch of certificates and you copy the certificates to Acquia through the same page you got the key to make your request. In the top box put the X509 Certificate only, Base64 encoded. In the intermediaries box put the X509 Intermediates/root only Reverse, Base64 encoded certificate. This is a standard certificate, not a legacy one. Now back to the actual simplesaml work.  

## SimpleSAMLphp configurations:

1. Download the SimpleSAMLphp library
2. Put the library next to the docroot folder
3. Make a symbolic link to the www folder of the simplesaml library so it is visible to the webserver. You don't want the other files visible on the web.
```
cd docroot; ln -s ../simplesamlphp/www simplesaml
```
4. Generate certificates in the cert folder inside the outer simplesamlphp-1.14.8 folder (not visible to the web) as (DRUPAL_ROOT/simplesamlphp-1.14.8/cert). You may need to create the cert folder.
```
openssl req -new -x509 -days 3652 -nodes -out saml.crt -keyout saml.pem
```
## Manual edits to files in SimpleSAMLphp library
#### overview
You're going to edit the config.php file and fill in all of the needed information.

 You need to set where the information about authenticated users will be stored. It goes into the netbadge database that you created on Acquia Cloud. Set a $sqldsn , $sqlusername, and $sqlpassword for each of the possible environments. If you aren't storing the user's info in a database, you need to find an alternative place to store the info.



#### Edits inside of the config array
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
'cooper-dev-sp' => array(
  'saml:SP',
  'entityID' => 'https://uvacooperdev.prod.acquia-sites.com',
  'idp' => 'urn:mace:incommon:virginia.edu' ,
  'privatekey' => 'saml.pem',
  'certificate' => 'saml.crt',
  'discoURL' => null,
),
```

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

10. If you haven't created certificates yet, you need to before making the request to your IDP. I created a self signed cert in the cert directory and set their values in the config file. Check the tutorials at the top for exact syntax. The purpose of these key / cert pairs is to identify your SP to the IDP. They need to know who you are and you prove that by holding onto a secret key.
```
openssl req -newkey rsa:2048 -new -x509 -days 3652 -nodes -out saml.crt -keyout saml.pem
```

11. Using [this XML file for the UVA IDP](https://shibidp.its.virginia.edu/shibboleth/uva-idp-metadata.xml) I used the converter in the simplesaml web interface to get the php needed for `saml20-idp-remote.php` and `shib13-idp-remote.php` in the metadatafolder of the simplesamlphp library. The converter is found at an address similar to this `http://uvacooper.test.dd:8083/simplesaml/admin/metadata-converter.php`

12. At this point you should be able to login to the simplesaml admin page and see your SP configured. If you click on the federation tab, you should be redirected to netbadge but be unable to login since the IDP doesn't recognize you yet.

12. Send off your request to UVA ITS or whatever IDP you are using. You have created a service provider and need your IDP to recognize your SP for it to work. [Here is the request form](https://virginia.service-now.com/com.glideapp.servicecatalog_cat_item_view.do?v=1&sysparm_id=6e4e233a6fc726007aeffee09d3ee433&sysparm_link_parent=966aaf8f6f9e0200287a2d65ad3ee40a&sysparm_catalog=25dfeeb46f004200287a2d65ad3ee46e&sysparm_catalog_view=service_request_catalog_portal_page).

## Make ITS request for the support site IDP

[Link to Request Page](https://virginia.service-now.com/com.glideapp.servicecatalog_cat_item_view.do?v=1&sysparm_id=6e4e233a6fc726007aeffee09d3ee433&sysparm_link_parent=966aaf8f6f9e0200287a2d65ad3ee40a&sysparm_catalog=25dfeeb46f004200287a2d65ad3ee46e&sysparm_catalog_view=service_request_catalog_portal_page)

1. Add a SP to authsources.php (library/config/authsources.php)
```
'support-prod-sp' => array(
  'saml:SP',
  'entityID' => 'https://support.coopercenter.org',
  'idp' => 'urn:mace:incommon:virginia.edu' ,
  'privatekey' => 'saml.pem',
  'certificate' => 'saml.crt',
  'discoURL' => null,
),
```
2. Go to the [/simplesaml admin page](https://ceps.coopercenter.org/simplesaml)
3. Grab the SP metadata from the [Federation page](https://ceps.coopercenter.org/simplesaml/module.php/core/frontpage_federation.php)
4. Send off that info in an IT request  
5. Once they approve your SP you can test it on the Authentication tab
6. Get the attribute names from testing the SP
7. Enter those attribute names into the simplesaml_auth module UI

## More edits to the simplesamlphp library

Since we are using a symlink, these require_once statements break. They can't find the files they need since calling `dirname(dirname(__FILE__))` doesn't actually return the directory name it needs. Hard coding the values solves the issue.

Edit `simplesaml/www/_include.php`

Edit line 96 and 34 of public simplesamlphp library so it doesn't strictly define config directory. `_include.php`
```php
/**
 * Disable magic quotes if they are enabled.
 */
function removeMagicQuotes()
{
    if (get_magic_quotes_gpc()) {
        foreach (array('_GET', '_POST', '_COOKIE', '_REQUEST') as $a) {
            if (isset($$a) && is_array($$a)) {
                foreach ($$a as &$v) {
                    // we don't use array-parameters anywhere. Ignore any that may appear
                    if (is_array($v)) {
                        continue;
                    }
                    // unescape the string
                    $v = stripslashes($v);
                }
            }
        }
    }
    if (get_magic_quotes_runtime()) {
        set_magic_quotes_runtime(false);
    }
}

if (version_compare(PHP_VERSION, '5.4.0', '<')) {
    removeMagicQuotes();
}

// initialize the autoloader
//require_once(dirname(dirname(__FILE__)).'/lib/_autoload.php');
// Edited 3-18 By milesgwood
require_once('/var/www/html/'. $_ENV['AH_SITE_NAME'] .'/old-attempt-simplesamlphp-1.14.15/lib/_autoload.php');

// enable assertion handler for all pages
SimpleSAML_Error_Assertion::installHandler();

// show error page on unhandled exceptions
function SimpleSAML_exception_handler($exception)
{
    if ($exception instanceof SimpleSAML_Error_Error) {
        $exception->show();
    } elseif ($exception instanceof Exception) {
        $e = new SimpleSAML_Error_Error('UNHANDLEDEXCEPTION', $exception);
        $e->show();
    } else {
        if (class_exists('Error') && $exception instanceof Error) {
            $code = $exception->getCode();
            $errno = ($code > 0) ? $code : E_ERROR;
            $errstr = $exception->getMessage();
            $errfile = $exception->getFile();
            $errline = $exception->getLine();
            SimpleSAML_error_handler($errno, $errstr, $errfile, $errline);
        }
    }
}

set_exception_handler('SimpleSAML_exception_handler');

// log full backtrace on errors and warnings
function SimpleSAML_error_handler($errno, $errstr, $errfile = null, $errline = 0, $errcontext = null)
{
    if (!class_exists('SimpleSAML_Logger')) {
        /* We are probably logging a deprecation-warning during parsing. Unfortunately, the autoloader is disabled at
         * this point, so we should stop here.
         *
         * See PHP bug: https://bugs.php.net/bug.php?id=47987
         */
        return false;
    }

    if ($errno & SimpleSAML_Utilities::$logMask || !($errno & error_reporting())) {
        // masked error
        return false;
    }

    static $limit = 5;
    $limit -= 1;
    if ($limit < 0) {
        // we have reached the limit in the number of backtraces we will log
        return false;
    }

    // show an error with a full backtrace
    $e = new SimpleSAML_Error_Exception('Error '.$errno.' - '.$errstr);
    $e->logError();

    // resume normal error processing
    return false;
}

set_error_handler('SimpleSAML_error_handler');

//milesgwood edit for remote server issues
$configdir = '/var/www/html/'. $_ENV['AH_SITE_NAME'] .'/old-attempt-simplesamlphp-1.14.15/config';

//$configdir = SimpleSAML\Utils\Config::getConfigDir();
if (!file_exists($configdir.'/config.php')) {
    header('Content-Type: text/plain');
    echo("You have not yet created the SimpleSAMLphp configuration files.\n");
    echo("See: https://simplesamlphp.org/docs/devel/simplesamlphp-install-repo\n");
    exit(1);
}

// set the timezone
SimpleSAML\Utils\Time::initTimezone();
```

## Reference Docs

[Description of UVA info from idP ](http://its.virginia.edu/netbadge/defaultpolicy.html)

[Garbage UVA walkthrough that you can't use since you can't access Apache.](http://its.virginia.edu/netbadge/unixdevelopers.html) It does have a link to the needed XML metadata of the UVA idP.

[simplesamlphp_auth Plugin](https://www.drupal.org/project/simplesamlphp_auth)

[Acquia Walkthrough](https://docs.acquia.com/articles/using-simplesamlphp-acquia-cloud-site)

[Another walkthrough that is Drupal 8 specific](http://valuebound.com/resources/blog/how-to-configure-single-sign-on-across-multiple-drupal-8-platforms-or-websites)

[UVA Dev docs](http://its.virginia.edu/netbadge/developers.html)
[UVA Shibboleth No good for SimpleSaml](http://its.virginia.edu/netbadge/unixdevelopers.html)

# Drupal Module Setup

1. You need to install and enable the externauth and simplesamlphp modules.
2. Enter the attribute names for userIDs into the module's configuration page.

## Troubleshooting

Even though the idP worked correctly. When I tried to install the simplesaml drupal module it failed.
```
Warning: include_once(/lib/_autoload.php): failed to open stream: No such file or directory in simplesamlphp_auth_check_library() (line 82 of modules/simplesamlphp_auth/simplesamlphp_auth.install).

Warning: include_once(): Failed opening '/lib/_autoload.php' for inclusion (include_path='.:/var/www/html/uvacooperdev/library/:/usr/share/php:/usr/share/pear') in simplesamlphp_auth_check_library() (line 82 of modules/simplesamlphp_auth/simplesamlphp_auth.install).

SimpleSAMLphp module requires the simplesamlphp library. See README file for installation instructions.
```
You get this error from the simplesaml enabling because the php library still needs to be set up according to [this documentation.](https://simplesamlphp.org/docs/stable/simplesamlphp-sp). I hardcoded the file paths in `/lib/_autoload.php` to solve the issue.

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

SUCCESS!!!!! From now on if you see a variable is missing like this variable `$dir = Settings::get('simplesamlphp_dir');`, you should code it into the site's settings.php file. That code is querying the settings array for that specific variable.

Now you can enable SimpleSaml SSO [through the account settings page!!!!](https://supportdev1.coopercenter.org/admin/config/people/accounts)

### Dev Site Netbadge login

simplesaml is configured on the dev site so I want to get that working with the automatic account creation. Then I want to get a idp service provider setup for the live site. Test it on dev and then roll it out to the live sites.

So I am able to get the attributes using the simplesaml admin login. I am working on setting up accounts using the actual module. So I have a netbadge login button on the login page but it doesn't actually link to anywhere. I am thinking that the cookie isn't being stored in the sql database as it should.

It looks like I am not actually using the netbadge database to store anything. I need to edit the config file for the simplesaml library.

After adding the netbadge database to the settings and the store.type array I got this error where the access is denied using the correct password. I am changing the database name from netbadge to uvacooperdb145495 to see if that changes anything. It worked again. The name of the database is set in the acquia interface, not the name I used.
```
The website encountered an unexpected error. Please try again later.</br></br><em class="placeholder">PDOException</em>: SQLSTATE[HY000] [1044] Access denied for user &#039;s33747&#039;@&#039;localhost&#039; to database &#039;netbadge&#039; in <em class="placeholder">SimpleSAML_Store_SQL-&gt;__construct()</em> (line <em class="placeholder">54</em> of <em class="placeholder">/mnt/www/html/uvacooperdev/old-attempt-simplesamlphp-1.14.15/lib/SimpleSAML/Store/SQL.php</em>).
```

Now I have the netbadge and auth module working together but the attribute names are all wrong.
```
The website encountered an unexpected error. Please try again later.</br></br><em class="placeholder">Drupal\simplesamlphp_auth\Exception\SimplesamlphpAttributeException</em>: Error in simplesamlphp_auth.module: no valid &quot;eduPersonPrincipalName&quot; attribute set. in <em class="placeholder">Drupal\simplesamlphp_auth\Service\SimplesamlphpAuthManager-&gt;getAttribute()</em> (line <em class="placeholder">165</em> of <em class="placeholder">modules/simplesamlphp_auth/src/Service/SimplesamlphpAuthManager.php</em>).
```

I'm going to try the only attribute that made any sense to me. -
urn:oid:0.9.2342.19200300.100.1.3
eduPersonPrincipalName - failed

Using that attribute worked!!!!! I don't know why it has such a strange name though.

The live site was broken as a result of the settings.php file specifying the wrong location of the simplesamlphp library. The correct entry takes account of the environment site.
```
$settings['simplesamlphp_dir'] = '/var/www/html/'. $_ENV['AH_SITE_NAME'] .'/old-attempt-simplesamlphp-1.14.15';
```
This turns into uvacooperdev uvacooper and other site enviroment folder names.
