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

Find how much memory is allowed for php. Composer will need a lot to install drupal. 128 is certainly not enough.

```
php -r "echo ini_get('memory_limit').PHP_EOL;"
```

Increase the allowed memory by editing your php.ini file. Set the memory limit = -1. Also set `date.timezone = America/New_York`. In vi youuse the / character to search.

```
sudo vi /etc/php-5.6.ini
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
```

Now that those settings are set, you can install drupal using composer or by downloading the package manually and unpacking it where you want it.


```
composer create-project drupal-composer/drupal-project:8.x-dev my_site --stability dev --no-interaction

curl -O https://ftp.drupal.org/files/projects/drupal-8.5.6.tar.gz
tar xvf drupal-8.5.6.tar.gz
mv drupal-8.5.6/* ~/environment/
mv drupal-8.5.6/.htaccess ~/environment/
```

Now that drupal is installed, you should be able to click run in cloud9 while the /core/install.php file is open and then preview that page in browser. Click the preview button and it will open up  a small window with the install screen. You'll be able to go through the first few pages until the database page.

If you are told youre missing the gd or other extensions, install it using yum.

```
sudo yum install php56-gd
sudo yum install php56-mbstring
```

Now let's setup the database, create a root user and password.

```
sudo service mysqld start
/usr/libexec/mysql55/mysql_secure_installation
mysql -u root -p
```

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
