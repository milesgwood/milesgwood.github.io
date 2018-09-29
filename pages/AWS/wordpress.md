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
