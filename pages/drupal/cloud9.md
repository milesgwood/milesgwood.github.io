---
layout: default
---

Enable Live development to edit code directly on your Dev environment. Access your code in the `~/dev/livedev` directory on the staging-17490.prod.hosting.acquia.com server. After editing the code on your Dev environment you will need to commit any changes. 

Cloud 9 Public Key needs to be added to Acquia so we can ssh to the acquia instance

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDXVbG/1E/m2SpHX2b48hRiXGvzf7jEWHw1racGOAmvtVWxv617n1lRXIzsj+41UZ+R7oK8K+XJ8f/kvlWnDugF6XHi1MSHevfFlzKy+C2Ep60iObgY1t2nY13jEuoXj+Of7wY8Kah5IdeEKKRIAJ5Sd7C59ucPQBwc2YwJ8Py9E40OmM/gIEVr+zCNzQZJ56+8eExwEXjpFLIM9B+bLOlCuiiUYMsQ54BlWl08dQ9fXo0FSHVihPkO9+nxVN4wgZE7/jjkKikGKQ4KC2GAoU0wiS+Ur3sOMKBAHHzPXpqcxPnn9Mz6zRFWhJN7KJyWe5HQacCI5voaS8HLcQWjHPgQwsUDVDo132A2drRPoKmz3v6mo3mrSDIs0vmL5Z8c1D4neu+bsmi3XvVpvnQWgoJx4olRAA7MVMn9E92GFwQxG04ZRfaqr9piWynvSO9kdz326+zZXqI6M8LaoT1c+bZuG3BtKX9nvXNfItFh7Xd01qnTGVaR4Cglsp/OGaHTqBkkIKFp5sCT6tX2SDKS079t9tf11wSFCh/MVnmI2hVngw/06egXq1ewp1J6enw3FrCzCmSt2C4NpXGDre8AHqDzWJe7wemW3qG3kaB3BS+Gyo2ZLKTV5WiKyXFFhtOI2Thcfce6dlVHWFURpa0NXKGxDSoywkLcBEavEuSnFb/saw== root+873929913536@cloud9.amazon.com
```

ssh into dev environment from your local machine

Username: uvacooper.dev

Host: staging-17490.prod.hosting.acquia.com

[Install Cloud 9 and node js](https://community.c9.io/t/how-to-use-c9-with-acquia-cloud/18410)

```bash
curl -L https://raw.githubusercontent.com/c9/install/master/install.sh | bash
echo 'export PATH=$HOME/.c9/node/bin:$PATH' >> ~/.bashrc
. ~/.bashrc
```

![Cloud9 Settings](../../images/cloud9settings.png)

```
echo 'export PATH=$HOME/.c9/node/bin:$PATH' >> ~/.bashrc
. ~/.bashrc
```