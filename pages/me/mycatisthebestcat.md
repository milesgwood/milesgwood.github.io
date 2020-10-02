---
layout: default
---

# Get the domain to point through cloudflare

Add new site to cloudflare and create an `A` record pointing the name `@` which is the root domain to IPv4 address `3.86.106.172`.

Also create a CNAME record that points the `www` name to the full domain name or in this case `mycatisthebestcat.com`.

In google domains, point the nameservers to the custom addresses of `karl.ns.cloudflare.com` and `maya.ns.cloudflare.com`

# Create a new folder on cloud9

Copy one of the existing sites and replace the folder name. Then edit the httpd.conf file and restart the apache server.

```
sudo vim /etc/httpd/conf/httpd.conf

<VirtualHost *:80>
  DocumentRoot /home/ec2-user/public_html/mycatisthebestcat.com
  ServerName mycatisthebestcat.com
</VirtualHost>
<VirtualHost *:443>
  DocumentRoot /home/ec2-user/public_html/mycatisthebestcat.com
  ServerName mycatisthebestcat.com
</VirtualHost>

sudo service httpd restart
sudo service httpd status
```

# Star Trek font

Pulled font from [fontspace](https://www.fontspace.com/stardate-81316-font-f28430) which was created by emwedo.
