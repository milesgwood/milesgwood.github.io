---
layout: default
---


[Link to current server release](https://www.minecraft.net/en-us/download/server)
[Video Tutorial](https://www.youtube.com/watch?v=MScc0spQpmc)
[Modded Tutorial](https://medium.com/exampro/2018-modded-minecraft-server-on-aws-part-1-run-a-modded-minecraft-server-on-aws-ec2-instance-b37290462d8d)



[AWS Spot Request](https://console.aws.amazon.com/ec2sp/v1/spot/launch?region=us-east-1)
Amazon Linux 2 AMI
minecraft pem key
m3.medium instance type
1vCPU 3.75GB
Capacity optimized fleet

Created custom minecraft security group with ssh traffic from my IP and custom TCP traffic from anywhere on port 25565.

Vanilla Install
```
cd ~/.ssh
chmod 400 minecraft.pem
ssh -i "minecraft.pem" ec2-user@ec2-54-158-199-175.compute-1.amazonaws.com
sudo yum update -y
sudo yum -y install java-1.8.0
sudo mkdir /minecraft
sudo chown -R ec2-user:ec2-user /minecraft
cd /minecraft
wget https://launcher.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar

java -Xmx1024M -Xms1024M -jar server.jar nogui
java -Xmx4G -Xms2G -jar server.jar nogui

echo '#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).
#Mon Aug 06 18:11:14 UTC 2018
eula=true' > eula.txt
```

modded install
```
java -jar forge-1.12.2-14.23.4.2756-installer.jar --installServer
```


Created new policy to allow copying to s3 bucket. Go to IAM then Policy.

```
{
   "Version": "2019-12-26",
   "Statement": [
       {
           "Effect": "Allow",
           "Action": ["s3:ListBucket"],
           "Resource": ["arn:aws:s3:::picard2020"]
       },
       {
           "Effect": "Allow",
           "Action": [
               "s3:ListBucket",
               "s3:GetObject",
               "s3:GetBucketLocation",
               "s3:PutObject",
               "s3:PutObjectAcl",
               "s3:DeleteObject"
           ],
           "Resource": ["arn:aws:s3:::picard2020/*"]
       }
   ]
}
```

Next I created a new role that allows s3 access through the ec2 instnace.


To copy the world you have to grant access to the s3 bucket picard2020 to the ec2 instance and then run. Go to the instance settings on the ec2 dashboard and then attach the IAM role that has the policy we created above. The role is called `Minecraft_S3Bucket_Access_Role`.

Backing up
```
cd /minecraft
mkdir backup
cp server.properties backup/server.properties
cp whitelist.json backup/whitelist.json
zip -r world.zip world
cp world.zip backup/world.zip
zip -r Home.zip Home
cp Home.zip backup/Home.zip
aws s3 cp --recursive backup s3://picard2020/backups/20200204


or you can zip all the files into one stoarge
zip -r backup.zip backup
aws s3 cp backup.zip s3://picard2020/backups/20190104/
```

Restoring
```
cd /minecraft
aws s3 cp s3://picard2020/backups/20191226-1/Home.zip .
unzip Home.zip
vim server.properties
screen -S "Minecraft server"
screen –ls
screen –r <screen_id>

20191231
aws s3 cp s3://picard2020/backups/20191231/server.properties .
aws s3 cp s3://picard2020/backups/20191231/whitelist.json .
aws s3 cp s3://picard2020/backups/20200204/world.zip .
aws s3 cp s3://picard2020/backups/20200204/Home.zip .
java -Xmx7G -Xms5G -jar server.jar nogui
```

# Domain setup

I created a subdomain `mc.dilatory.fun` which points to the server IP. All you need to do is add an A record in cloudflare that points to the server and doesn't proxy traffic through cloudflare (meaning you uncheck the cloud icon). The A record gets entered as just the subdomain `mc` not the whole domain.

# See how you can restore EC2 instance from EBS volume that was saved 20GiB.

Login and reattach volume. You must put the instance in the same Availability Zone.

`lsblk` to show disks

NAME          MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
nvme0n1       259:0    0  20G  0 disk
 nvme0n1p1   259:1    0  20G  0 part /
 nvme0n1p128 259:2    0   1M  0 part
nvme1n1       259:3    0  20G  0 disk
 nvme1n1p1   259:4    0  20G  0 part
 nvme1n1p128 259:5    0   1M  0 part

Check if there are files on a partition
```
sudo file -s /dev/nvme1n1p1
/dev/nvme1n1p1: SGI XFS filesystem data (blksz 4096, inosz 512, v2 dirs)

This means there is data on there.
```

The device you want to mount is 20G and doesn't have a mountpoint.

```
sudo mount -t xfs -o nouuid /dev/nvme1n1p1 /new
sudo umount -d /dev/nvme1n1p1
```

3.230.118.222

# Change your launch template to avoid making too many EBS volumes saved.
