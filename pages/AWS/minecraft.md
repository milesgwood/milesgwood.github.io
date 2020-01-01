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
wget https://launcher.mojang.com/v1/objects/4d1826eebac84847c71a77f9349cc22afd0cf0a1/server.jar

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
aws s3 cp --recursive backup s3://picard2020/backups/20191231
```

Restoring
```
cd /minecraft
aws s3 cp s3://picard2020/backups/20191226-1/Home.zip .
unzip Home.zip
vim server.properties

aws s3 cp s3://picard2020/backups/20191231/server.properties .
aws s3 cp s3://picard2020/backups/20191231/whitelist.json .
aws s3 cp s3://picard2020/backups/20191231/world.zip .
aws s3 cp s3://picard2020/backups/20191231/Home.zip .
java -Xmx7G -Xms5G -jar server.jar nogui
```

# See how you can restore EC2 instance from EBS volume that was saved 20GiB.

# Change your launch template to avoid making too many EBS volumes saved.