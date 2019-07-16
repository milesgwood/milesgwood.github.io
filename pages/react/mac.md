---
layout: default
---

# Setting up react environment on Mac

Current status

nvm - command not found
node v6.11.1
npm 3.10.10

Install nvm which is the node version manager.
```
brew install nvm
```

After this command I have a ~/.nvm folder but the command does nothing. I need to edit the `/.bash_profile` Add these lines.

```
source $(brew --prefix nvm)/nvm.sh
export NVM_DIR=~/.nvm
```

Now nvm is at version `0.34.0`

Run . ~/.bash_profile to apply the changes you made to your .bash_profile file

Node v6.11.1 seems to already be installed. It seems that the current version for OSX is 12.6.0 so I need to update it.

```
nvm install stable
```

Now node is at version `v12.6.0`, npm is at `v6.9.0` and we are ready to start.

Ending with
node --version v12.6.0
npm  --version v6.9.0
nvm  --version v0.34.0

[Facebook Getting Started Tutorial](https://facebook.github.io/create-react-app/docs/getting-started)

npx comes with npm versions 5.2 and higher. Running `nvm install stable` gave us the npm version 6.9.0.

```
npx create-react-app beheard-photos
```

I needed to delete my old node_modules folder in order fo rhte new one inside my new project to get used.
