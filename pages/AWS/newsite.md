---
layout: default
---

# New Website Time

Got the IP address and the key from launching the EC2 instance with Ubuntu Bitnami Wordpress installed.

## Connecting to Cloud9

Connecting Cloud9 to it requires me to add the ssh key to authorized keys on the server and install node js.
```
sudo apt-get install nodejs

nodejs -v
v4.2.6
```

[NVM tutorial](https://tecadmin.net/install-nodejs-with-nvm/)

```
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.bashrc

nvm -v
v0.35.0
```

I didn't actually end up using nvm. The first install worked and this is the location that you need to enter for cloud9 to work.

```
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

# Creating a HTML directory for a custom coded HTML site

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

Failed

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

It's really starting to look like this binami instance will not let me have my own website here. I did it totally differently last time. LAST TRY!

## Restarting Apache and MySQL
```
sudo /opt/bitnami/ctlscript.sh restart apache
```


## Vim Tricks

God note for using vim. To search type `/search word` and it will find it for you. `n` goes to the next find.
To insert you use i
To save you use `:wq`

https://docs.bitnami.com/oci/apps/wordpress/administration/use-htaccess/
