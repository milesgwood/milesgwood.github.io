---
layout: default
---

## Amazon Web Services Projects

### Goal: Get PhpMyAdmin on a new AWS account

#### Create an EC2 instance with a LAMP stack and then install phpMyAdmin. Seems easy enough right?

[Instance Launch tutorial](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html#ec2-launch-instance)

#### Connect to instance

You have to make sure your key file is not publicly readable. So fix the permissions.
```
chmod 400 AWSKey1-15-2018phpMyAdmin.pem
ssh -i "AWSKey1-15-2018phpMyAdmin.pem" ec2-user@ec2-52-15-207-39.us-east-2.compute.amazonaws.com
```

#### Installing stack

[Tutorial with command](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-LAMP.html)

This command installs apache php7 mysql server and a php mysql connector.
```
sudo yum install -y httpd24 php70 mysql56-server php70-mysqlnd
sudo service httpd start
sudo chkconfig httpd on
```
