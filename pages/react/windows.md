---
layout: default
---

# Setting up env on Windows linux subsystem

[Tutorial](https://gist.github.com/noygal/6b7b1796a92d70e24e35f94b53722219)

Pre check
npm 3.10.10
nvm not found
node v6.14.1

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.5/install.sh | bash
```

Close and restart shell
Mid Check
npm 3.10.10
nvm 0.33.5
node v6.17.1

```
nvm install stable
nvm use stable
npx create-react-app beheard-photos
```

Post check
npm 6.10.0
nvm 0.33.5
node v12.7.0

Succes!!!
