---
layout: default
---

# Need to install sass --watch

```
npm --version
6.13.4

npm install -g sass
```

This installs the sass module within the `~/.nvm/versions/node/v13.5.0/bin/sass` folder which is already in the PATH as part of the node install.

With a global install you don't need to alter the PATH variable.

## If you wanted to edit the $PATH variable

Current path variable

```
echo $PATH

/home/ec2-user/.nvm/versions/node/v13.5.0/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/ec2-user/.local/bin:/home/ec2-user/bin:/home/ec2-user/.local/bin:/home/ec2-user/bin

export PATH="$PATH:whatever/path/you/want"
```
