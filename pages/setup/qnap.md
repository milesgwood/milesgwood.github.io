---
layout: default
---

# Diable MyQNAPCloud

[Sign in to QNAP.com](https://account.qnap.com/) and unregister the device.

In QTS disable UPnP port forwarding and delete any custom mappings you setup.

# Check 2.5GBe Connection

Open Network and Virtual Switch in Control Panel. Go to Interfaces and verify that Adapter 2 is at 2.5Gbps and Adapter 1 is 100Mbps. They transfer at 75MB and 250MB/s respectivley.

In control panel reset the Web Server settings to default configuration.

# QNAP Jellyfin Setup

Disabled HTTPS, SSL certificate, and automatic port mapping and then restarted the jellyfin container.

I want to setup a reverse proxy with SSL encrypttion to access my server. caddy never worked for me so I will use `traefik` as an alternative.

There is also [NGINX Proxy Manager](https://nginxproxymanager.com/) docker container which has a gui to setup a reverse proxy. It's also apparently easier to setup docker containers through `Portainer` whitch is 1000% times better than Container Station.

In container station create a new container for portainer.

```yaml
version: '3'

services:
  app:
    container_name: portainer
    image: portainer/portainer-ce
    restart: always
    ports:
      - '9000:9000'
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /share/docker/compose/appdata/portainer:/data
```

Checking the current filesystem through ssh I see that `/var/run/docker.sock` exists except it is `docker.sock=`. When I autocomplete on docker it completes to docker.sock so the equals char may be irrevelent. However `/share/docker` does not exist.

After entering in the YAML into container station I'll check to see if those two volumes are different through ssh.

Now `/share/docker/compose/appdata/portainer` exists.

I'm met with these messages in portainer.

Ensure that you have started the Portainer container with the following Docker flag:

-v "/var/run/docker.sock:/var/run/docker.sock" (Linux).

I believe this means it needs to use that docker.sock volume which the second line of the yaml satisfies.

I also read on discord that I need this docker folder to be setup as a shared folder. If this fails to work as is, then I'll setup a shared folder through the control panel and make sure to create a docker user that also uses the shared folder. Right now these folders belong to the admin user and administrators group.

portainer seems to be running.

Within portainer I created a new container using the following YAML

```yaml
version: '3'
services:
  app:
    image: 'jc21/nginx-proxy-manager:latest'
    ports:
      - '35080:80'
      - '35081:81'
      - '35443:443'
    environment:
      DB_MYSQL_HOST: 'db'
      DB_MYSQL_PORT: 3306
      DB_MYSQL_USER: 'npm'
      DB_MYSQL_PASSWORD: 'npm'
      DB_MYSQL_NAME: 'npm'
    volumes:
      - /share/docker/compose/appdata/npm/data:/data
      - /share/docker/compose/appdata/npm/letsencrypt:/etc/letsencrypt
  db:
    image: 'jc21/mariadb-aria:latest'
    environment:
      MYSQL_ROOT_PASSWORD: 'npm'
      MYSQL_DATABASE: 'npm'
      MYSQL_USER: 'npm'
      MYSQL_PASSWORD: 'npm'
    volumes:
      - /share/docker/compose/appdata/npm/mysql:/var/lib/mysql
```

##### CHANGE THE USERNAME AND PASSWORD VALUES ONCE IT IS WORKING

NGINX lets you obtain SSL certificates and also setup the reverse proxy within a GUI.

NGINX is started but hasn't been configured yet. I can see a prompt telling me to login to the admin panel at this address http://192.168.86.46:35080.

Port 35443 responds saying it is a bad request (probably because there is no SSL certificate). Port 35443 takes me to the admin login page.

Default login is/was

admin@example.com
changeme

[This installation guide was helpful for figuring out the admin interface](https://www.youtube.com/watch?v=P3imFC7GSr0)

I'm opening port 80 and 443 on my Google Wifi router and directing them to my NAS.

The Internal Ports need to be set to the NGINX ports 0.0.0.0:35080->80/tcp, 0.0.0.0:35081->81/tcp, 0.0.0.0:35443->443/tcp. The ports are 35080, 35081, and 35443.

The QNAP control panel web server is using port 80 and port 8081 for http and https.

On the NAS running `lsof -i` shows what TCP ports are listening and what application is using them.

Running `netstat -pnltu | grep -i "80"` shows just the entries that contain 80.
tcp 0 0 0.0.0.0:8096 0.0.0.0:_ LISTEN 23331/jellyfin
tcp 0 0 127.0.0.1:58080 0.0.0.0:_ LISTEN 14573/_thttpd_
tcp 0 0 0.0.0.0:35080 0.0.0.0:_ LISTEN 29635/dockerd
tcp 0 0 :::80 :::_ LISTEN 10456/fcgi-p
tcp 0 0 :::8081 :::_ LISTEN 10456/fcgi-p
udp 3584 0 255.255.255.255:8097 0.0.0.0:_ 16835/bcclient
udp 3584 0 255.255.255.255:8097 0.0.0.0:_ 16835/bcclient
udp 3584 0 255.255.255.255:8097 0.0.0.0:_ 16835/bcclient
udp 3584 0 255.255.255.255:8097 0.0.0.0:_ 16835/bcclient
udp 3584 0 255.255.255.255:8097 0.0.0.0:_ 16835/bcclient
udp 3584 0 255.255.255.255:8097 0.0.0.0:_ 16835/bcclient
udp 0 0 255.255.255.255:8097 0.0.0.0:_ 16835/bcclient
udp 0 0 0.0.0.0:67 0.0.0.0:_ 7480/dhcpd
udp 0 0 0.0.0.0:37036 0.0.0.0:_ 7480/dhcpd
udp 0 0 fe80::265e:beff:fe48:4853:546 :::_ 10419/dhclient
udp 0 0 fe80::265e:beff:fe48:4854:546 :::_ 7435/dhclient
udp 0 0 :::17815 :::\* 7480/dhcpd

`netstat -pnltu | grep -i "443"`
tcp 0 0 0.0.0.0:35443 0.0.0.0:\* LISTEN 29635/dockerd

I'm fairly sure that the **dockerd** process is NGINX because port `35081` is the port I use to connect to the admin interface fo NGINX. I want that port listening on 80 and 443.
`netstat -pnltu | grep -i "35081"`
tcp 0 0 0.0.0.0:35081 0.0.0.0:\* LISTEN 29635/dockerd

On my phone, http results in no response. Https results in an immidiate refused connection.

Docker networks are isolated from eachother. By default the a new network is created for the project, which here is `nginxproxymanagernpm_default` in bridge mode. What does bridge mode mean?

`docker network list`
NETWORK ID NAME DRIVER SCOPE
e631e4ef99ec bridge bridge local
597939e612eb host host local
f471fbdc6dd5 nginxproxymanagernpm_default bridge local
0d8e52a4c620 none null local
ed3565dded78 portainer_default bridge local

According to YT tutorial above I need to connect my webapp to the nginxprox... network. I can see that the jellyfin app isn't listening on any ports?

### HOW DO I CONNECT THE JELLYFIN SERVICE TO THE NGINX NETWORK

List all of the networks within docker.

`docker ps`
CONTAINER ID IMAGE COMMAND STATUS PORTS NAMES
8f764a214c4a jc21/mariadb-aria:latest "/scripts/run.sh" Up About an hour 3306/tcp nginxproxymanagernpm_db_1
49aa2ddb9c3b jc21/nginx-proxy-manager:latest "/init" Up About an hour (healthy) 0.0.0.0:35080->80/tcp, 0.0.0.0:35081->81/tcp, 0.0.0.0:35443->443/tcp nginxproxymanagernpm_app_1
183e32ad7755 portainer/portainer-ce "/portainer" Up About an hour 8000/tcp, 0.0.0.0:9000->9000/tcp portainer
41376784449d jellyfin/jellyfin "/jellyfin/jellyfin" Up 2 hours jellyfin

We don't want to expose any ports externally. We want to direct traffic coming in to the correct container, in this case jellyfin.

## Installing Nextcloud server to test if NGINX is getting any traffic at all

docker run --network nginxproxymanagernpm_default --name=nextcloud -d nextcloud

--network specifies the network we want to connect this service to
--name specifies the domain we are using to name this service - this is the Forward Hostname
-d runs the command in the backgournd

Now I see an additional entry
`docker ps`  
CONTAINER ID IMAGE COMMAND PORTS NAMES
fb57e8324022 nextcloud "/entrypoint.sh apac…" 80/tcp nextcloud

Changing the port forwarding rules to direct traffic to the NGINX server made progress. I still see port 80 being used by `fcgi-p`. You can use grep to narrow down the netstat command even further.

`netstat -tulpn | grep :80 | grep LISTEN`
tcp 0 0 0.0.0.0:8096 0.0.0.0:_ LISTEN 23331/jellyfin
tcp 0 0 :::80 :::_ LISTEN 10456/fcgi-p
tcp 0 0 :::8081 :::\* LISTEN 10456/fcgi-p

Changing Web Server port number in control panel to `8999` from port `80`

Requested SSL certificate for neverloseapin.com from NGINX

```
Error: Command failed: /usr/bin/certbot certonly --non-interactive --config "/etc/letsencrypt.ini" --cert-name "npm-1" --agree-tos --email "miles.gwood@gmail.com" --preferred-challenges "dns,http" --domains "neverloseapin.com"
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator webroot, Installer None
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for neverloseapin.com
Using the webroot path /data/letsencrypt-acme-challenge for all unmatched domains.
Waiting for verification...
Challenge failed for domain neverloseapin.com
http-01 challenge for neverloseapin.com
Cleaning up challenges
Some challenges have failed.

    at ChildProcess.exithandler (child_process.js:308:12)
    at ChildProcess.emit (events.js:314:20)
    at maybeClose (internal/child_process.js:1051:16)
    at Process.ChildProcess._handle.onexit (internal/child_process.js:287:5)
```

It appears that port 80 my be blocked by my ISP according to this [port scanner site](https://www.whatsmyip.org/port-scanner/).

## THIS IS NOT AN OPTION AS COX BLOCKS PORT 80 - TRY AGAIN WHEN YOU MOVE TO A NEW PLACE

# Jellyfin Setup

I got rid of my previous Jellyfin docker container in favor of creating one in portainer. Here is the YAML config:

```
version: "3.5"
services:
  jellyfin:
    image: jellyfin/jellyfin
    container_name: jellyfin
    user: 1001:100
    network_mode: "host"
    volumes:
      - /share/jellyfin-app-data/config:/config
      - /share/jellyfin-app-data/cache:/cache
      - /share/Media:/media
      - /share/Public:/media2 #change this to Photography once ready
    restart: "unless-stopped"
    # Optional - alternative address used for autodiscovery
    environment:
      - JELLYFIN_PublishedServerUrl=http://jellyfin.milesgreawtood.com
      - HOST_HOSTNAME=jellyfin
```
