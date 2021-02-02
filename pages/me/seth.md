---
layout: default
---

http://sethrogendoyouwanttogoto.space/

I purchased the domain sethrogendoyouwanttogoto.space so I can get his attention and try to connect with the man that is trying to free humanity from the delusion of god.

I want to free humanity and myself from delusions and superstitions. I want Seth to get on board with my no religion in space website. I think he'd find it funny.

At setup before doing anything

1. Name servers are default
2. DNSSEC is endabeld ???
3. No registered hosts are setup

Copied the cloudflare name servers. Now I need to point the cloudflare server to the AWS IP.

Create an A record pointing to `3.86.106.172`

sethrogendoyouwanttogoto.space

Created the first version of the message to seth.

This movie came out 6 years ago.

```
sudo vim /etc/httpd/conf/httpd.conf

<VirtualHost *:80>
  DocumentRoot /home/ec2-user/public_html/sethrogendoyouwanttogoto.space
  ServerName sethrogendoyouwanttogoto.space
</VirtualHost>
<VirtualHost *:443>
  DocumentRoot /home/ec2-user/public_html/sethrogendoyouwanttogoto.space
  ServerName sethrogendoyouwanttogoto.space
</VirtualHost>

sudo service httpd restart
sudo service httpd status
```

## This was a hysterically stupid idea. I'mn suprised I can launce a site on an amazon EC2 instane while drinking.

Project abandoned... cause it's moronic.
