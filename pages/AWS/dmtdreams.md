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
cd /
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

# Installing nodejs 
