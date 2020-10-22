---
layout: default
---

# htaccess

.htaccess in the docroot

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

# Virtual Hosts

Send a specific site to a specific folder as it's root. `/etc/httpd/conf/httpd.conf`

Below the line that reads `Listen 80` insert all of your site's document roots.

```
<VirtualHost *:80>
DocumentRoot /var/www/html/
ServerName milesgreatwood.com
</VirtualHost>

<VirtualHost *:443>
DocumentRoot /var/www/html/
ServerName milesgreatwood.com
</VirtualHost>

<VirtualHost *:80>
  DocumentRoot /home/ec2-user/public_html/mycatisthebestcat.com
  ServerName mycatisthebestcat.com
</VirtualHost>

<VirtualHost *:443>
  DocumentRoot /home/ec2-user/public_html/mycatisthebestcat.com
  ServerName mycatisthebestcat.com
</VirtualHost>
```
