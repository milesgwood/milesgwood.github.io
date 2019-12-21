---
layout: default
---

# Wordpress Website Start to Finish

Starting with nothing, I'm going to create a new woocommerce store on AWS. Here's a general map of what is going to happen.
- Buy a domain on google domains
- Launch an EC2 instance on aws
- Connect that instance to the purchased domain
- Connect your EC2 isntance to Cloud9
- Get a SSL cert from cloudflare
- Install Wordpress
- Choose a WooCommerce Theme
- Connect the site to a payment gateway
- Add products to the site
- Optimize Page Speed
- Optimize SEO

## Buy your domain

Go to google domains and purchase your domain for the site. I'm creating a store to sell locking hat pin backs so I'm going with the name `neverloseapin.com`. It will cost 12$ a year for the domain.

![google domains](../../images/googledomain.png)

## Launch a new Amazon EC2 instance and install wordpress on it

[So this will reference a previous tutorial I did.](phpMyAdmin.md) It covers how to launch a bitnami instance of wordpress on a t2.micro EC2 instance and connect it with a phpMyAdmin account.

Once you have wordpress installed fresh and working you can use the host IP address to set your domain's A records. This tutorial is very handwavy but you want to come out of this step with a fresh wordpress instance without ssl.

![ip](../../images/ec2-ip.png)

## Connect your domain to Cloudflare

Open up a cloudflare account and your google domain's dashboard. On the cloudflare side, add your site and get to the screen where it asks for the records. You want to make an A record going to your EC@ instance's Public IP address and a CNAME record that points the www. version of the domain to neverloseapin.com.

![cloudflare](../../images/cloudflare.png)

Now go to the google domains side, click the DNS tab and enter the Nameservers from the cloudflare page your were just adding records to.

![names](../../images/domain-nameservers.png)

This will route traffic to cloudflare nameservers and grant you the ability to have a SSL certificate on your website.

## Connect Cloud9 to your EC2 instance

Before we enable SSL through cloudflare we need to get access to the ec2 instance via ssh. Instead of simply connecting to the server, we'll go ahead and setup the Cloud9 server we'll be developing on.

First task is to make sure you have ssh access to the ec2 instance. You may need to edit your security group to allow for ssh access from your IP. You want to ssh using your downloaded key. The defualt user is ubuntu for AWS ec2 instances.

```
ssh ubuntu@54.236.45.250 -i WordpressRestoreOld.pem
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-1050-aws x86_64)
*** System restart required ***
       ___ _ _                   _
      | _ |_) |_ _ _  __ _ _ __ (_)
      | _ \ |  _| ' \/ _` | '  \| |
      |___/_|\__|_|_|\__,_|_|_|_|_|

  *** Welcome to the Bitnami WordPress 4.9.4-2 ***
  *** Documentation:  https://docs.bitnami.com/aws/apps/wordpress/ ***
  ***                 https://docs.bitnami.com/aws/ ***
  *** Bitnami Forums: https://community.bitnami.com/ ***
bitnami@ip-172-31-79-149:~$
```

Now that your have connected to your EC2 instance, you can setup cloud9 access to the instance.

![cloud9-set](../../images/cloud9-setup.png)

Cloud9 will ask you to add a key to your EC2 instance's collection of authorized keys. You'll want to copy that public key and then edit the authorized_keys file on the ec2 server.


```
cd ~/.ssh
vim authorized_keys
```

Press `i` to insert text and then paste the public key into that authorized_keys file. To save hit `ESC` - `:wq`.

### Install Cloud9 Packages on Server

Clou9 will need some node, python and other goodies to work properly so we need to install them.

```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.32.0/install.sh | bash
exit
ssh ubuntu@54.236.45.250 -i WordpressRestoreOld.pem
nvm install 6
node -v
which node
```

Alternative:

```
sudo apt-get install nodejs-legacy
```


That first line installs nvm. You have to restart your terminal before it takes effect so exit and ssh back into the server. The output is a path of the node executable `/home/bitnami/.nvm/versions/node/v6.14.4/bin/node` in my case. If you don't get a path, run `which node` again. Enter the path into the cloud9 form field asking for a node path.

You will want to add the node binary to the environment's path variable. Add the node parent folder to the path.  `/home/bitnami/.nvm/versions/node/v6.14.4/bin/`

```
sudo vim /etc/environment
```

Alternative way of adding to the path.

```
export PATH="$PATH:/path/to/dir"
```

![cloud9settings](../../images/cloud9settings.png)

Now if you click the continue button, you will get an error message that asks you to install python 2.7.

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python2.7
```

Cloud9 requires some special permissions so you need to make sure the account you provide is root or at least you can add the ownership of certain folders to bitnami.

```
chown bitnami:bitnami /usr/etc
```


## Prepare the server and wordpres for Cloudflare SSL  

[Tutorial](https://support.cloudflare.com/hc/en-us/articles/227634427-Using-Cloudflare-with-WordPress)

[Setting up the server with cod_cloudflare](https://www.cloudflare.com/technical-resources/#mod_cloudflare)

# Monica's site

vim /opt/bitnami/mysql/my.cnf

cd
ssh -i "monica-key.pem" ubuntu@ec2-3-133-160-220.us-east-2.compute.amazonaws.com

mysql -u root -p

GRANT SUPER ON *.* TO 'bn_wordpress'@'localhost';

# Installing nodejs on Bitnami Style Server

Connecting Cloud9 to it requires me to add the ssh key to authorized keys on the server and install node js.
```

sudo apt-get install nodejs
nodejs -v
v4.2.6
which nodejs
/usr/bin/nodejs
```

## Cloud9 installing python 2.7

Cloud9 requires python 2.7 to work. [Here's a tutorial on how to install python 2.7](https://tecadmin.net/install-python-2-7-on-ubuntu-and-linuxmint/) without replacing the python3 version that already exists on the system.

```
sudo apt-get update
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

cd /usr/src
sudo wget https://www.python.org/ftp/python/2.7.17/Python-2.7.17.tgz
sudo tar xzf Python-2.7.17.tgz

cd Python-2.7.17
sudo ./configure --enable-optimizations
sudo make altinstall
```

Finally check the version that installed:

```
python2.7 -V
Python 2.7.17

which python2.7
/usr/local/bin/python2.7
```

At this point in the installation cloud9 succeeds in the installation of the required packages! Time to start actually creating pages!

# Creating a HTML directory for a custom coded HTML site - Failed!!!

Find the .htaccess file

sudo find / -name ".htaccess"

Created .htaccess with this location `/home/bitnami/.htaccess`

```
# enable the directives - assuming they're not enabled globally
ExpiresActive on

# send an Expires: header for each of these mimetypes (as defined by server)
ExpiresByType image/png "access plus 1 month"
ExpiresByType image/gif "access plus 1 month"
ExpiresByType image/jpeg "access plus 1 month"

# Force HTTPS for a specific domain
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteCond %{HTTP:X-Forwarded-Proto} !https
RewriteCond %{HTTP_HOST} ^milesgreatwood.com$
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [NE,L,R=301]
```


Find the `httpd.conf` where we tell the server where to go for different domains.

```
sudo find / -name "httpd.conf"
```

Gives me

```
/opt/bitnami/apache2/conf/httpd.conf
/opt/bitnami/apache2/conf/original/httpd.conf
/opt/bitnami/apache2/conf/bitnami/httpd.conf
/opt/bitnami/bnsupport/original-data/apache2/conf/httpd.conf
```

Home on this server is `/home/bitnami/`

Editing that first one as there is already an index.html file here `/home/bitnami/htdocs` I just want to open that page with a virtualhost port.

It looks that these entries need to be placed below the `Listen 80` line [source](https://httpd.apache.org/docs/2.4/vhosts/examples.html)

I believe this file below shouldn't have been edited.
```
sudo vim /opt/bitnami/apache2/conf/httpd.conf   
```

```
<VirtualHost *:80>
  DocumentRoot /home/bitnami/htdocs
  ServerName milesgreatwood.com
</VirtualHost>

<VirtualHost *:443>
  DocumentRoot /home/bitnami/htdocs
  ServerName milesgreatwood.com
</VirtualHost>
```

[Tutorial](https://docs.bitnami.com/general/infrastructure/lamp/configuration/configure-custom-application/)

Correct file to edit for VirtualHosts `/stack/apache2/conf/extra/httpd-vhosts.conf` [video](https://www.youtube.com/watch?v=kU4S8XhCXoQ). It's favorited.

I'm working on an apache server trying to create [name based virtual hosts](http://httpd.apache.org/docs/2.4/vhosts/name-based.html). IP based virtual hosts is when you have diffrent websites on different servers all managed by apache. That's not relevant to me today.


```
<VirtualHost *:80>
  DocumentRoot /home/bitnami/htdocs
  ServerName milesgreatwood.com
</VirtualHost>

<VirtualHost *:443>
  DocumentRoot /home/bitnami/htdocs
  ServerName milesgreatwood.com
</VirtualHost>
```

This is where I placed my new site index.html file. I now need to get my domain to point to it.
`/opt/bitnami/apps/dmtdreams`

[From](https://docs.bitnami.com/general/infrastructure/lamp/configuration/configure-custom-application/)

To configure your application to use a virtual host instead of the prefix URL, make these changes:

Delete the following line in the `/opt/bitnami/apache2/conf/bitnami/bitnami-apps-prefix.conf` file:

Include "/opt/bitnami/apps/myapp/conf/httpd-prefix.conf"
Add a new link in the /opt/bitnami/apache2/conf/bitnami/bitnami-apps-vhosts.conf file:

Include "/opt/bitnami/apps/myapp/conf/httpd-vhosts.conf"
Some applications require further changes in configuration files or the database. Please check the exact changes in the application’s documentation.


Had to create the `myapp` folder which i called dmtdreams as well as the conf folder and the httpd-vhosts.conf file which i filled with this:

```
<VirtualHost *:80>
  DocumentRoot /opt/bitnami/apps/dmtdreams
  ServerName milesgreatwood.com
</VirtualHost>

<VirtualHost *:443>
  DocumentRoot /opt/bitnami/apps/dmtdreams
  ServerName milesgreatwood.com
</VirtualHost>
```

In the wordpress side the directory is

```
drwxr-xr-x  3 root root 4096 Oct 15 02:07 bitnami
drwxr-xr-x  3 root root 4096 Oct 28 00:40 dmtdreams
drwxr-xr-x  5 root root 4096 Oct 15 02:07 phpmyadmin
drwxr-xr-x  7 root root 4096 Oct 15 02:07 wordpress
```

and the conf and htdocs are like this

```
drwxr-xr-x 2 bitnami root      4096 Oct 15 02:02 bin
lrwxrwxrwx 1 root    root        14 Oct 15 02:07 .bitnamimeta -> ../../var/meta
-r-xr--r-- 1 root    root   8510156 Oct 15 01:39 bnconfig
drwxr-xr-x 4 bitnami root      4096 Oct 15 02:02 conf    ------------ 755 owned by bitnami
drwxrwxr-x 5 bitnami daemon    4096 Oct 15 02:01 htdocs  ------------ 775 owned by bitnami group is daemon
drwxr-xr-x 2 root    root      4096 Oct 15 02:01 licenses
drwxrwxr-x 2 bitnami daemon    4096 Oct 21 01:44 tmp
```

Inside the conf folder

```
-rw-r--r-- 1 bitnami root  256 Oct 15 02:02 banner.conf
drwxr-xr-x 2 bitnami root 4096 Oct 15 02:01 certs
-rw-r--r-- 1 bitnami root  719 Oct 15 02:02 htaccess.conf
-rw-r--r-- 1 bitnami root 1045 Oct 15 02:07 httpd-app.conf
-rw-r--r-- 1 bitnami root  455 Oct 15 02:07 httpd-prefix.conf
-rw-r--r-- 1 bitnami root  846 Oct 28 00:17 httpd-vhosts.conf   ------- all are owned by bitnami and 644
drwxr-xr-x 2 bitnami root 4096 Oct 15 02:02 php-fpm
```

Inside htdocs of wordpress `/opt/bitnami/apps/wordpress/htdocs`

Notice that the containing folder is owned by the same user/group as index.php
All readable files are `664 bitnami daemon`

```
drwxrwxr-x  5 bitnami daemon  4096 Oct 15 02:01 .
drwxr-xr-x  7 root    root    4096 Oct 15 02:07 ..
-rw-rw-r--  1 bitnami daemon   420 Nov 30  2017 index.php
-rw-rw-r--  1 bitnami daemon 19935 Jan  1  2019 license.txt
-rw-rw-r--  1 bitnami daemon  7447 Apr  8  2019 readme.html
-rw-rw-r--  1 bitnami daemon  6919 Jan 12  2019 wp-activate.php
drwxrwxr-x  9 bitnami daemon  4096 Oct 15 02:05 wp-admin
-rw-rw-r--  1 bitnami daemon   369 Nov 30  2017 wp-blog-header.php
-rw-rw-r--  1 bitnami daemon  2283 Jan 21  2019 wp-comments-post.php
-rw-r-----  1 bitnami daemon  4253 Oct 21 01:48 wp-config.php
drwxrwxr-x  7 bitnami daemon  4096 Oct 21 01:44 wp-content
-rw-rw-r--  1 bitnami daemon  3847 Jan  9  2019 wp-cron.php
drwxrwxr-x 20 bitnami daemon 12288 Oct 15 02:02 wp-includes
-rw-rw-r--  1 bitnami daemon  2502 Jan 16  2019 wp-links-opml.php
-rw-rw-r--  1 bitnami daemon  3306 Nov 30  2017 wp-load.php
-rw-rw-r--  1 bitnami daemon 39551 Jun 10 13:34 wp-login.php
-rw-rw-r--  1 bitnami daemon  8403 Nov 30  2017 wp-mail.php
-rw-rw-r--  1 bitnami daemon 18962 Mar 28  2019 wp-settings.php
-rw-rw-r--  1 bitnami daemon 31085 Jan 16  2019 wp-signup.php
-rw-rw-r--  1 bitnami daemon  4764 Nov 30  2017 wp-trackback.php
-rw-rw-r--  1 bitnami daemon  3068 Aug 17  2018 xmlrpc.php
```

My files are matching

```
cd dmtdreams
sudo mkdir htdocs
sudo chmod 775 htdocs
sudo chown bitnami htdocs
sudo chgrp daemon htdocs
```

It's really starting to look like this bitami instance will not let me have my own website here. I did it totally differently last time. LAST TRY!

## Restarting Apache and MySQL
```
sudo /opt/bitnami/ctlscript.sh restart apache
```

## Vim Tricks

God note for using vim. To search type `/search word` and it will find it for you. `n` goes to the next find.
To insert you use i
To save you use `:wq`

https://docs.bitnami.com/oci/apps/wordpress/administration/use-htaccess/
