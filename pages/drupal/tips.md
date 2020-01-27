---
layout: default
---

# Connecting to prod site with ssh

You can get the ssh address in acquia. For home computer connection here's the command lacking the keyfile name. You have to update the permissions to 400 from within the ~/.ssh folder.

```
cs ~/.ssh
chmod 400 keyfile
ssh -i keyfile uvacooper.prod@uvacooper.ssh.prod.acquia-sites.com
```

# Copying files to prod server

```
scp -i keyfile /mnt/c/Users/miles/Downloads/filename.csv uvacooper.prod@uvacooper.ssh.prod.acquia-sites.com:/home/uvacooper/prod/sites/demographics/files/subfolder/
```
