---
layout: default
---

## Ubuntu on Virtual Machine

Installing Virtual Box on my Windows 10 machine so I can install Ubuntu.
https://www.lifewire.com/install-ubuntu-linux-windows-10-steps-2202108

Set the size of the VM to 200GB so it can store the blockchain. Simply follow these instructions and replace the git repository with the Bitcoin Diamond repo. `https://github.com/eveybcd/BitcoinDiamond.git`

Before gcc could run make, I had to run `apt install libevent-dev` package

Once it is all compiled run the qt client ./bitcoindiamond-qt
