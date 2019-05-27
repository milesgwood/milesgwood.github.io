---
layout: default
---

Installing Drupal through lando on AWS.

```
sudo yum update -y
sudo yum install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
docker info
```

This updates the packages on the EC2 instance, installs docker, starts docker and then sets the user settings so that ec2-user can run commands without sudo. The docker info command will show you the version you're running.

```
Server Version: 18.06.1-ce
```

[Tutorial](https://blog.wodby.com/6-reasons-to-deploy-drupal-8-with-docker-how-to-guide-b2f073e61672)

```
docker pull mariadb
docker pull drupal:8.6.14
docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
drupal              8.6.14              5f5912eac556        3 days ago          447MB
mariadb             latest              97df12fa9319        9 days ago          369MB
lambci/lambda       nodejs4.3           6c30c5c1b1e0        9 months ago        969MB
lambci/lambda       python2.7           377732dd7a1f        9 months ago        974MB
lambci/lambda       python3.6           acf16b1d5297        9 months ago        1.1GB
lambci/lambda       nodejs6.10          da301bf4fe34        9 months ago        1.02GB
```

So now we have drupal and a mariadb MYSQL docker image. We need to spin up drupal and connect it to the database.

```
docker run -e MYSQL_ROOT_PASSWORD=admin -e MYSQL_DATABASE=drupal8 -e MYSQL_USER=drupal8 -e MYSQL_PASSWORD=drupal8 -v mariadb:/var/lib/mysql -d --name mariadb mariadb
docker run --name drupal8 --link mariadb:mysql -p 80:80 -d drupal:8.6.14
docker ps

ec2-user:~/environment $ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS                NAMES
6972ce360c53        drupal:8.6.14       "docker-php-entrypoi…"   18 seconds ago       Up 17 seconds       0.0.0.0:80->80/tcp   drupal8
db17324766ba        mariadb             "docker-entrypoint.s…"   About a minute ago   Up About a minute   3306/tcp             mariadb
```
