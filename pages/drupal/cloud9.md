---
layout: default
---

Enable Live development to edit code directly on your Dev environment. Access your code in the `~/dev/livedev` directory on the staging-17490.prod.hosting.acquia.com server. After editing the code on your Dev environment you will need to commit any changes.

Cloud 9 Public Key needs to be added to Acquia so we can ssh to the acquia instance

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDXVbG/1E/m2SpHX2b48hRiXGvzf7jEWHw1racGOAmvtVWxv617n1lRXIzsj+41UZ+R7oK8K+XJ8f/kvlWnDugF6XHi1MSHevfFlzKy+C2Ep60iObgY1t2nY13jEuoXj+Of7wY8Kah5IdeEKKRIAJ5Sd7C59ucPQBwc2YwJ8Py9E40OmM/gIEVr+zCNzQZJ56+8eExwEXjpFLIM9B+bLOlCuiiUYMsQ54BlWl08dQ9fXo0FSHVihPkO9+nxVN4wgZE7/jjkKikGKQ4KC2GAoU0wiS+Ur3sOMKBAHHzPXpqcxPnn9Mz6zRFWhJN7KJyWe5HQacCI5voaS8HLcQWjHPgQwsUDVDo132A2drRPoKmz3v6mo3mrSDIs0vmL5Z8c1D4neu+bsmi3XvVpvnQWgoJx4olRAA7MVMn9E92GFwQxG04ZRfaqr9piWynvSO9kdz326+zZXqI6M8LaoT1c+bZuG3BtKX9nvXNfItFh7Xd01qnTGVaR4Cglsp/OGaHTqBkkIKFp5sCT6tX2SDKS079t9tf11wSFCh/MVnmI2hVngw/06egXq1ewp1J6enw3FrCzCmSt2C4NpXGDre8AHqDzWJe7wemW3qG3kaB3BS+Gyo2ZLKTV5WiKyXFFhtOI2Thcfce6dlVHWFURpa0NXKGxDSoywkLcBEavEuSnFb/saw== root+873929913536@cloud9.amazon.com
```

ssh into dev environment from your local machine

Username: uvacooper.dev

Host: staging-17490.prod.hosting.acquia.com

[Install Cloud 9 and node js](https://community.c9.io/t/how-to-use-c9-with-acquia-cloud/18410)

```bash
curl -L https://raw.githubusercontent.com/c9/install/master/install.sh | bash
echo 'export PATH=$HOME/.c9/node/bin:$PATH' >> ~/.bashrc
. ~/.bashrc
```

![Cloud9 Settings](../../images/cloud9settings.png)

```
echo 'export PATH=$HOME/.c9/node/bin:$PATH' >> ~/.bashrc
. ~/.bashrc
```

In advanced settings set the environment root to `/home/uvacooper/dev/livedev` and the nodejs binary path to `/mnt/gfs/home/uvacooper/.c9/node/bin/node`

## Module Development for Drupal on cloud9

We're going to setup a fresh drupal site with could9 on an ec2 instance and get all of the essential components to start developing a module.

Goals
1. Install composer
2. Install Drush
2. Install Drupal site fresh
3. Create new module
4. Connect site to a debugger for remote debugging

First create your new environment using a small ec2 instance. The micro instance doesn't offer enough ram so the second option is required.

```bash
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer
export PATH="$HOME/.composer/vendor/bin:$PATH"
source ~/.bash_profile
composer global require drush/drush:dev-master
composer global update
drush --version
```

You should now have composer installed and drush version greater than 8.0. I have 9.4-dev installed after all that code ran.

Before installing drupal, clean the amazon environment of old versions of PHP. I want to use 7.1 from now on so let's erase php56 and install 71.

```
sudo yum remove php56*
sudo yum install php71
php --version

PHP 7.1.27 (cli) (built: Mar  8 2019 18:22:16) ( NTS )
Copyright (c) 1997-2018 The PHP Group
Zend Engine v3.1.0, Copyright (c) 1998-2018 Zend Technologies
```

Find how much memory is allowed for php. Composer will need a lot to install drupal. 128 is certainly not enough.

```
php -r "echo ini_get('memory_limit').PHP_EOL;"
```

Increase the allowed memory by editing your php.ini file. Set the memory limit = -1. Also set `date.timezone = America/New_York`. In vi you use the / character to search.

```
sudo vi /etc/php-7.1.ini
```

These lines go in the php.ini file
```
memory_limit = -1

date.timezone = America/New_York

opcache.enable=1
opcache.memory_consumption=128
opcache.interned_strings_buffer=8
opcache.max_accelerated_files=4000
opcache.revalidate_freq=60
opcache.fast_shutdown=1
opcache.enable_cli=1
```

Restart the web server. After the install of drupal you can set the php limit again. `memory_limit = 512MB`

```
sudo yum install php56-gd
sudo yum install php56-mbstring
sudo service httpd restart
sudo service mysqld restart


/usr/libexec/mysql55/mysqladmin -u root password 'new-password'
/usr/libexec/mysql55/mysqladmin -u root -h ip-172-31-27-204 password 'new-password'
```

Now that those settings are set, you can install drupal using composer or by downloading the package manually and unpacking it where you want it.


```
composer create-project drupal-composer/drupal-project:8.x-dev website --stability dev --no-interaction

curl -O https://ftp.drupal.org/files/projects/drupal-8.5.6.tar.gz
tar xvf drupal-8.5.6.tar.gz
mv drupal-8.5.6/* ~/environment/
mv drupal-8.5.6/.htaccess ~/environment/
```

Now that drupal is installed, you should be able to click run in cloud9 while the /core/install.php file is open and then preview that page in browser. Click the preview button and it will open up  a small window with the install screen. You'll be able to go through the first few pages until the database page.

If you are told youre missing the gd or other extensions, install it using yum.

```
sudo yum install php71-gd
sudo yum install php71-mbstring
sudo yum install php71-pdo
```

Now let's setup the database, create a root user and password.

```
sudo service mysqld start
/usr/libexec/mysql55/mysql_secure_installation
mysql -u root -p
```

I installed core in the environment folder.

```
git clone --branch 8.8.x https://git.drupalcode.org/project/drupal.git

````

At this point your should be able to go through the rest of the site setup and view the finished blank site.

Install drupal console so you can use the module builder.

```
curl https://drupalconsole.com/installer -L -o drupal.phar
sudo mv drupal.phar /usr/local/bin/drupal
sudo chmod +x /usr/local/bin/drupal
cd ~/environment/my_site/web
drupal
```

Run `drupal generate:module` to start making the module!

## Initial module installs

```
composer require drupal/admin_toolbar
drush en admin_toolbar -y
```

## Preferences and code formatting

[PHP Code Formatting tutorial](https://medium.com/icf-church-developers/php-formatting-for-cloud9-ide-9f90ca6fbbad)

```
wget wget http://cs.sensiolabs.org/download/php-cs-fixer-v2.phar -O php-cs-fixer -O ~/php-cs-fixer
sudo mkdir ~/bin
sudo mv ~/php-cs-fixer ~/bin
sudo chmod a+x ~/bin/php-cs-fixer
```

Go into Preferences, enable PHP format code on save and set the formatter rules to `php-cs-fixer fix "$file" --rules=@Symfony,@PSR2`


## Apache not starting

```
sudo service mysqld restart
sudo service httpd restart
sudo service mysqld status
sudo service httpd status
```

# Update to Core with issues

Install Composer

```
curl -sS https://getcomposer.org/installer | php
php composer require phpunit/phpunit
```

Copy over all of the core files and extra files after unpacking it all.

```
wget https://ftp.drupal.org/files/projects/drupal-8.6.1.tar.gz
tar -xvzf drupal-8.6.1.tar.gz
```

Run the database updates script if needed. Here is the db_backup script for future reference.

```bash
# !/bin/bash
docroot="/home/uvacooper/dev/livedev/docroot"
backup_folder="/home/uvacooper/dev/livedev/db_backups/"
today=`date +%Y-%m-%d.%H:%M`
echo "Starting Database Backups" && \
cd docroot/sites && \
for SITE in ceps certify newsletter cooper csr demographics lead sei sorensen support vig
do
    cd $SITE && \
    echo "Backing Up" $SITE && \
    drush sql-dump --result-file=$SITE.sql && \
    mv $docroot/$SITE.sql $backup_folder$today-$SITE.sql &&\
    cd ..
done
cd ../../db_backups &&\
zip -r db_backup_$today.zip $backup_folder
```

## Godaddy Setup Cloud9

Failed because you can't use Python 2.7 on GoDaddy.
https://ferugi.com/blog/nodejs-on-godaddy-shared-cpanel/

## SASS on cloud9

So sass is installed on the Cooper Center website livedev server. You can check with:

```
sass --version
1.11.0 compiled with dart2js 2.0.0
```

To start watching the sass files run:

```
cd /home/uvacooper/dev/livedev/docroot/themes/coopercenter_units/css
sass --watch .

or
sass --watch .:output_dir/
```

# Clone live site to module dev environment

Use composer to install backup_migrate and then enable it in the dashboard.
```
composer require drupal/backup_migrate
```

Add the following to .htaccess to allow larger file uploads.

```
php_value upload_max_filesize 32M
php_value post_max_size 64M
```

Manually import the database sql dump. You may need to [reset the mysqld password for root](https://www.a2hosting.com/kb/developer-corner/mysql/reset-mysql-root-password).

```
sudo service mysqld stop
sudo mysqld_safe --skip-grant-tables &
mysql
UPDATE mysql.user SET Password=PASSWORD('NEW-PASSWORD') WHERE User='root';
FLUSH PRIVILEGES;
exit;
mysqladmin -u root -p shutdown
sudo service mysqld start
mysql -u root -p develop < vdot.sql
```

If the mysql server refuses the import increase the size of allowed packets and restart mysqld.

```
sudo vim /etc/my.cnf
max_allowed_packet=64M
wq
sudo service mysqld restart
```

Now the database should work. You need to sync the config database by improting the config files. Export them all, copy them over and import them.

```
../../vendor/drush/drush/drush config-import
```

Backup the working database from inside the site directory

```
../../vendor/drush/drush/drush sql-dump --result-file=/home/ec2-user/environment/db_backup.sql
mysql -u root -p develop < vdot.sql
```


# Fresh install from scratch. I want a script for it all.

## Download and install drupal

Create a fresh environment and use an Amazon Linux distro, not ubuntu.

```
curl -O https://ftp.drupal.org/files/projects/drupal-8.6.14.tar.gz
tar xvf drupal-8.6.14.tar.gz
mv drupal-8.6.14/* ~/environment/
mv drupal-8.6.14/.htaccess ~/environment/
```

Run the index.php file. Then preview the running application and it should take you to the install screen. The URL is NOT an ip address. It looks like this:

https://e3044f433a1946d98862e9f7be037687.vfs.cloud9.us-east-2.amazonaws.com/core/install.php

[Required PHP extensions](https://www.drupal.org/docs/8/system-requirements/php-requirements)

```
sudo yum remove php56*
sudo yum install php71 -y
sudo yum install php71-gd -y
sudo yum install php71-mbstring -y
sudo yum install php71-pdo -y
sudo yum install php71-opcache -y
sudo yum install php71-mysqlnd -y

OR just enable them all

sudo yum install php71* -y

php --version

PHP 7.1.27 (cli) (built: Mar  8 2019 18:22:16) ( NTS )
Copyright (c) 1997-2018 The PHP Group
Zend Engine v3.1.0, Copyright (c) 1998-2018 Zend Technologies
```

After changing PHP it should still work. You can navigate to the install screen. Still don't install yet.

Now let's edit the php features and settings.

```
sudo vi /etc/php-7.1.ini
```

Use / to search for memory limit and set it to 256M from 128M. Search for date.timezone and set it as below. Additionally, enable opcache which we installed above.

```
memory_limit = 256M
date.timezone = America/New_York

opcache.enable=1
opcache.memory_consumption=128
opcache.interned_strings_buffer=8
opcache.max_accelerated_files=4000
opcache.revalidate_freq=60
opcache.fast_shutdown=1
opcache.enable_cli=1
```

Install composer so you can easily add modules.

```
curl -sS https://getcomposer.org/installer | php && \
sudo mv composer.phar /usr/local/bin/composer && \
export PATH="$HOME/.composer/vendor/bin:$PATH" && \
source ~/.bash_profile && \
composer global require drush/drush:dev-master && \
composer global update && \
drush --version
```

composer --version
Composer version 1.8.5 2019-04-09 17:46:47


## Setup the database.

Now let's setup the database, create a root user and password.

```
sudo service mysqld start
/usr/libexec/mysql55/mysql_secure_installation
mysql -u root -p
CREATE DATABASE website;
exit;
Set the password based on your lastpass saved password
```

Start the MYSQL database

```
sudo service mysqld start
```

Now you can actually use the database and go through the install. Set database name to the one you created `website`. Set user to root and enter the password.
