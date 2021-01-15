---
layout: default
---

# NVM is broken - reinstall

So here is my current broken setup. I need to update node to get sass modules working.

```
node --version
v4.8.7

which node
/home/uvacooper/.c9/node/bin/node
```

`npm --version` returns this error because node is too old.

```
SyntaxError: Block-scoped declarations (let, const, function, class) not yet supported outside strict mode
```

nvm is installed but not on the path. It's installed at `/home/uvacooper/.nvm`.

I want to reinstall nvm in bin folder which is already on the path.

```
export $PATH

bash: export: `/usr/local/ruby2.6/bin:/usr/local/php7.3/bin:/usr/local/drush8:/usr/local/bin:/usr/local/ruby2.6/bin:/usr/local/php7.3/bin:/usr/local/drush8:/usr/local/bin:/usr/local/ruby2.6/bin:/usr/local/php7.3/bin:/usr/local/drush8:/usr/local/bin:/mnt/gfs/uvacooperdev/livedev/node_modules:/home/uvacooper/.c9/bin:/home/uvacooper/.c9/node/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games': not a valid identifier
```

What's up with that invalid identifier?

`vim ~/.bashrc`

```
export PATH=$HOME/.c9/node/bin:$PATH
export PATH=$HOME/.c9/bin:$PATH
export PATH=/mnt/gfs/uvacooperdev/livedev/node_modules:$PATH

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

The parts after exporting the NVM_DIR variable are invalid.

I manually chaned it to the following. I can't execute nvm commands though even with ~/.nvm in the path.

```
export PATH=$HOME/.c9/node/bin:$PATH
export PATH=$HOME/.c9/bin:$PATH
export PATH=/mnt/gfs/uvacooperdev/livedev/node_modules:\$PATH

export NVM_DIR="$HOME/.nvm"
export PATH=$HOME/.nvm:\$PATH
```

I still can't execute any nvm commands. I have to run the following portion of the fresh install to get NVM working again. I check it's status with `nvm --version`.

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

# Reinstalling NVM

[Site to download NVM from](https://github.com/nvm-sh/nvm)

I moved the old `~/.nvm` hidden folder to `~/nvm-old` and ran the following:

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.36.0/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

Now I get a working version on nvm

```
nvm --version
0.36.0
```

# Installing new version of node

Get a list of node versions `nvm ls-remote`. The even releases are supported for longer. I want to upgrade form v4.8.7 to the latest in v14 so I run `nvm install v14.14.0`. Now I need to make the newer version of node the one that is actually used so I list out the installed versions with `nvm list` which outputs this:

```
nvm list
       v14.14.0
->       system
node -> stable (-> v14.14.0) (default)
stable -> 14.14 (-> v14.14.0) (default)
iojs -> N/A (default)
unstable -> N/A (default)
lts/* -> lts/erbium (-> N/A)
lts/argon -> v4.9.1 (-> N/A)
lts/boron -> v6.17.1 (-> N/A)
lts/carbon -> v8.17.0 (-> N/A)
lts/dubnium -> v10.22.1 (-> N/A)
lts/erbium -> v12.19.0 (-> N/A)
```

To switch the version I'm using run `nvm use v14.14.0`. I get an error output

```
nvm is not compatible with the npm config "prefix" option: currently set to "/mnt/gfs/home/uvacooper/.nvm/versions/node/v14.14.0"
Run `npm config delete prefix` or `nvm use --delete-prefix v14.14.0` to unset it.
```

I run the reccommended `nvm use --delete-prefix v14.14.0`.

```
nvm use --delete-prefix v14.14.0
Now using node v14.14.0 (npm v6.14.8)
```

Here is all of the current versions:

```
node --version
v14.14.0

nvm --version
0.36.0

npm --version
6.14.8

vim ~/.bashrc
export PATH=$HOME/.c9/node/bin:$PATH
export PATH=$HOME/.c9/bin:$PATH
export PATH=/mnt/gfs/uvacooperdev/livedev/node_modules:$PATH

export NVM_DIR="$HOME/.nvm"
export PATH=$HOME/.nvm:$PATH

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

Now I want to update npm as well but it seems `6.14.8` is the latest. Note that npm comes packaged with the version of node you are using. Look at where it is stored.

`/home/uvacooper/.nvm/versions/node/v14.14.0/bin/npm`

```
npm install npm@latest -g
npm update -g
```

# Getting SASS module working again in a fresh terminal

If you run `sass --watch scss:css` and get an error check which version of node you are running `node --version`. If it is v4, then you need to run the following.

```
source ~/.bashrc && nvm use --delete-prefix v14.14.0 && sass --watch scss:css
```
