---
layout: default
---

# Need to install sass --watch

```
npm --version
6.13.4

npm install sass
```

I installed the sass library inside the milesgreatwood.com directory. I likely need to add the node_modules folder to the bash path. However it's likely not best to have the node modules folder inside specific site folders. I need to have them outside the specific folder.


```
echo $PATH

/home/ec2-user/.nvm/versions/node/v13.5.0/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/ec2-user/.local/bin:/home/ec2-user/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin

export PATH="$PATH:whatever/path/you/want"
```
