---
layout: default
---

# Setting up Monero on Ledger Nano S

1. Follow [this tutorial on Windows](https://github.com/qubenix/monero-site/blob/7edf03f77d4c4e9fcd11bfd3de68440e5322279b/_i18n/en/resources/user-guides/verification-windows-beginner.md) to setup Kleopatra and the Monero keys from fluffypony.
2. Download your binary file you want to verify
3. Find the SHA256 hash you are going to compare to
4. In CMD (Not Bash or Liniux) run `certUtil -hashfile monero-gui-win-x64-v0.11.1.0.zip SHA256` and compare the output
5. Verify the signature against the signature for fluffypony in [the source code repository (/utils/gpg_keys).](https://github.com/monero-project/monero/tree/master/utils/gpg_keys)
6. [Use the monero gui to setup your device](https://monero.stackexchange.com/questions/8695/how-do-i-on-windows-generate-a-ledger-monero-wallet-with-the-cli-and-subsequen/)
7. From the decompressed folder with the gui.exe in it run `.\monero-wallet-cli.exe --generate-from-device MyMoneroWallet --restore-height 1585000 --subaddress-lookahead 3:200`
8. It says I generated a new wallet on the device and showed me a public view key
9. The GUI asks for the wallet file to be specified on startup.
10. It will synchronize your node with the network which downloads the node to `C:\ProgramData\bitmonero\lmdb`
11. To use a remote node go to settings and enter the info for a remote node. [Find node info.](https://getmonero.org/resources/user-guides/remote_node_gui.html)
12. If hitting the connect button doesn't work you can start a remote daemon using the CLI. `monero-wallet-cli.exe --daemon-address node.moneroworld.com:18089` The GUI should realize and start using the connection.

# Restore your Monero Wallet

Go through all of the above steps to verify the hashfile using fluffypony's key & also verifying the binaries by comparing the SHA256 to the confirmed hashes. Install the gui and click it to start. I'm using the 12.3.0 gui so it should support Ledger setup from the GUI. It was incredibly easy this time. I simply had to select the Ledger option, use the same lookahead of 3:200 I used before and a restore height of 162. It will take some time to sync the blockchain but I can let it run while I'm at work.

# Send Monero from wallet

Sending is as easy as entering the address and setting the fee. Since monero makes it hard to track who sent what coins, you sometimes have to include a message with the transaction to make it clear who you sent the coins to.
