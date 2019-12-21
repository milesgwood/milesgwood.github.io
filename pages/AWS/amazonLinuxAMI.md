---
layout: default
---

# A Fresh Start

Keep your goals clear and document every step of the process. Jumping into things quickly turns you into a useless snail. Today I just want to launch a LAMP stack and make sure that I can create different webpages on it. Let's start with a hello world page.

1. In my milesgreatwood@virginia.edu AWS account I started to launch an instance.
2. I'm choosing the following EC2 Server

```
Amazon Linux 2 AMI (HVM), SSD Volume Type - ami-0b69ea66ff7391e80 (64-bit x86) / ami-09c61c4850b7465cb (64-bit Arm)

Amazon Linux 2 comes with five years support. It provides Linux kernel 4.14 tuned for optimal performance on Amazon EC2, systemd 219, GCC 7.3, Glibc 2.26, Binutils 2.29.1, and the latest software packages through extras.

Root device type: ebs Virtualization type: hvm ENA Enabled: Yes

Instance Type	ECUs - vCPUs	- Memory (GiB) -	Instance Storage (GB)	EBS-Optimized Available	Network Performance

t2.micro -	Variable -	1 -	1 -	EBS only	-	Low to Moderate
```

IP address is - `3.86.106.172`

# Domain setup

I setup all of the domains I own to point to the same server.

`A` records take the name of the site `dmtdreams.net` and point to an IP `3.86.106.172`

`CNAME` records just replace a name so www.site.com becomes site.com. you'd enter `www` in the first box and site.com as where it points to.

 Lastly I logged into google doamins and made sure all the nameservers point to cloudflare so I have SSL.


## Connect to the server with hyper so you can add the cloud9 ssh key

```
cd /~.ssh
cp /mnt/c/Users/miles/Dropbox/Keys/dmtdreams.pem .
chmod 600 dmtdreams.pem  
ssh ec2-user@3.86.106.172 -i dmtdreams.pem
sudo vim ~/.ssh/authorized_keys
i to insert
end to jump to the End
hit enter and then paste it the key from cloudn9
:wq to save
```

Go into cloud9 and setup the username `ec2-user` and the host `3.86.106.172`.

At this point the key is copied but nodejs isn't installed. You need to install nodejs for the server to  work.

# Installing nodejs on Amazon Linux

Amazon linux doesn't let you use apt-get, you have to use yum.

[NVM tutorial](https://tecadmin.net/install-nodejs-with-nvm/)

```
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
source ~/.bashrc
export NVM_DIR="$HOME/.nvm"
exit
ssh ec2-user@3.86.106.172 -i dmtdreams.pem
nvm -v
v0.35.2
```

Now that we have Node Version Manager we need to install the latest nodejs release. So first we list the available releases and install them with the latest Node Package Manager option.

```
nvm ls-remote
nvm install 13.5.0 --latest-npm
node -v
v13.5.0
npm -v
6.13.4
```

Now you can connect the cloud9 portal to the server. You don't need to specify the path of the node binaries but you can find them like this:

```
which node
~/.nvm/versions/node/v13.5.0/bin/node
```

All of the packages seem to install successfully so use Amazon linux AMI for future sites. The Bitnami Wordpress version causes issues.  

# Install and start Apache Webserver

Here we are updating all the linux packages, installing apache webserver, and starting it. The last line makes sure the server restarts if it is stopped.

```
sudo yum install httpd -y
sudo service httpd start
sudo chkconfig httpd on
```

Now you should see the apache test page when you visit the site. If you don't then you need to update your inbound connections rules in Amazon security groups. You need to allow HTTP and HTTPS traffic from anywhere.

```
yum info httpd

Loaded plugins: extras_suggestions, langpacks, priorities, update-motd
Installed Packages
Name        : httpd
Arch        : x86_64
Version     : 2.4.41
Release     : 1.amzn2.0.1
Size        : 4.0 M
Repo        : installed
From repo   : amzn2-core
Summary     : Apache HTTP Server
URL         : https://httpd.apache.org/
License     : ASL 2.0
Description : The Apache HTTP Server is a powerful, efficient, and extensible
            : web server.

sudo service httpd status
```

# Set Permissions on Apache html folder

[Permissions Info](https://docs.aws.amazon.com/efs/latest/ug/wt2-apache-web-server.html)

So apache by default serves files from `/var/www/html/` but we want to serve them from the user folder so cloud9 can edit them and find them in `/home/ec2-user`.

```
sudo mkdir milesgreatwood.com
```

At this point the permissions are as follows in public_html

```
drwxr-xr-x 3 root root 32 Dec 20 23:15 .
drwxr-xr-x 4 root root 33 Dec 20 22:49 ..
drwxr-xr-x 2 root root  6 Dec 20 23:15 milesgreatwood.com
```

We need to change that so the ec2-user is the owner rather than root. This makes ec2-user the owner and recursivley adds permissions for others(o) to read(+r)

```
sudo chown ec2-user milesgreatwood.com
sudo chmod -R o+r milesgreatwood.com
cd milesgreatwood.com
echo "<html><h1>Hello from Amazon EFS</h1></html>" > hello.html
```

The updated permissions from the public_html folder.

```
drwxr-xr-x 4 ec2-user ec2-user  45 Dec 21 00:55 .
drwx--x--x 8 ec2-user ec2-user 180 Dec 20 23:58 ..
drwxr-xr-x 2 ec2-user ec2-user  24 Dec 20 23:48 dmtdreams
drwxr-xr-x 2 ec2-user ec2-user  24 Dec 20 23:48 milesgreatwood
```

public_html 755
ec2-user 711
Folders inside 755
Files 755 or 644

# Setting up the sites within the User Home folder

```
cd /home/ec2-user
mkdir public_html
sudo chmod 750 public_html
cd public_html
mkdir milesgreatwood
sudo chmod 755 milesgreatwood
cd milesgreatwood
echo "<html><h1>Hello from Amazon EFS</h1></html>" > hello.html
```

Now we need to setup the virtual hosts to point the different domains to the correct servers. Edit the `httpd.conf file` and then restart apache. Enter these virtual host entries below the `Listen 80` line.

```
sudo vim /etc/httpd/conf/httpd.conf
```

```
<VirtualHost *:80>
  DocumentRoot /home/ec2-user/public_html/milesgreatwood.com
  ServerName milesgreatwood.com
</VirtualHost>
<VirtualHost *:443>
  DocumentRoot /home/ec2-user/public_html/milesgreatwood.com
  ServerName milesgreatwood.com
</VirtualHost>

<VirtualHost *:80>
  DocumentRoot /home/ec2-user/public_html/dmtdreams.net
  ServerName dmtdreams.net
</VirtualHost>
<VirtualHost *:443>
  DocumentRoot /home/ec2-user/public_html/dmtdreams.net
  ServerName dmtdreams.net
</VirtualHost>

<VirtualHost *:80>
  DocumentRoot /home/ec2-user/public_html/deemsday.com
  ServerName deemsday.com
</VirtualHost>
<VirtualHost *:443>
  DocumentRoot /home/ec2-user/public_html/deemsday.com
  ServerName deemsday.com
</VirtualHost>

<VirtualHost *:80>
  DocumentRoot /home/ec2-user/public_html/dilatory.fun
  ServerName dilatory.fun
</VirtualHost>
<VirtualHost *:443>
  DocumentRoot /home/ec2-user/public_html/dilatory.fun
  ServerName dilatory.fun
</VirtualHost>

<VirtualHost *:80>
  DocumentRoot /home/ec2-user/public_html/grandideasexecutedbysnails.com
  ServerName grandideasexecutedbysnails.com
</VirtualHost>
<VirtualHost *:443>
  DocumentRoot /home/ec2-user/public_html/grandideasexecutedbysnails.com
  ServerName grandideasexecutedbysnails.com
</VirtualHost>
```

Now we restart apache to check if the changes took place.

```
sudo service httpd restart
sudo service httpd status
```

# Enable User Directory Public HTML files

[Enable userdir](https://www.tecmint.com/enable-apache-userdir-module-on-rhel-centos-fedora/)

```
sudo vim /etc/httpd/conf.d/userdir.conf
```

In this file you need to set UserDir to `enabled` and uncomment the `public_html` line. The path to the end user account 'public_html' directory must be accessible to the webserver userid.  This usually means that ~userid must have permissions of 711, ~userid/public_html must have permissions of 755, and documents contained therein must be world-readable. Otherwise, the client will only receive a "403 Forbidden" message.

```
sudo chmod 711 /home/ec2-user
sudo chmod 755 /home/ec2-user/public_html
```
