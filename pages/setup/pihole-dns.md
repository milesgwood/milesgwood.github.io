---
layout: default
---

UBlock removes content on your browser after it reaches your computer. A Pi-Hole blocks ads as a DNS sync hole. My goal is to setup the pihole and route individual devices through it using DNS server settings on individual devices.

# Equipment

I already have a rasberry Pi 2011.12 which is either a `Model A Revision 2` or a `Model B Revision 2.0`. They have 256 and 512 MB of ram respectivley.

- `5.1V power` supply
- `Micro USB` cable
- `8GB SD` card 20MB/s 14.8 Effective speed - write failed the first time
- `8GB USB2 Bird USB` Drive 2-5MB/s speed

# Turtorials

[Linux Tech Tips Video Tutorial](https://www.youtube.com/watch?v=KBXTnrD_Zs4)

[Written Tech Tips Tutorial](https://linustechtips.com/main/topic/1094810-pi-hole-setup-tutorial/)

[Longest but most detailed for individual device setups - Eli the computer guy](https://www.youtube.com/watch?v=KiJ8JFR_y1w)

The Linus tutorial seems to only turn on the pihole for specific devices. That is what I'll start with.

# Attempt 1

[Recent 2020 Tutorial](https://www.youtube.com/watch?v=4X6KYN1cQ1Y&t=61s)

This tutorial uses the Diet Pi Distro x32 version. It logs to Ram instead of the SD card. He uses a Pi4. Let's see if it works on this old Pi with an old SD card. If I'm able to get this working I'll setup a better second one.

Use `Etcher` to write the image to the 8GB SD card. It changed it to FAT32 format and writes as expected at 20MB/s. The distro is only 1.06GB.

Before this I have 12 devices on my network.

After plugging in the Pi I get a red light and eventually a green light but no new decives on my Google Wifi app.

I'm attempting to flash the image onto a flash drive as well. It succeeded. The SD card seemed to fail.

After flashing the SD card a second time, on boot up I get more than the single red light. I get a link light as well which I assume is the wired ethernet connection.

Diet Pi appeared in the Google Wifi App!!!

IP address is `192.168.86.45`. Open a hyper terminal and ssh into the device.

```
ssh root@192.168.86.45 -p
dietpi
```

The removing of files is taking forever greater than 30 minutes. Possibly because of the slow SD card.

After if finishes running its setup, you can install the pure image by selecting `install` in the DietPi software dialog (it's at the bottom). After that runs we can actually install the pi-hole software. The two installs took about an hour on this crummy hardware.

```
curl -sSL https://install.pi-hole.net | bash

of if that fails...

wget -O basic-install.sh https://install.pi-hole.net
sudo bash basic-install.sh
```

This pi-hole started installing taking 12 minutes.

IP address is `192.168.86.45/24`
Gateway is `192.168.86.1`

Within the Google Wifi app I reserved the .45 IP address listed above. The PiHole software reccomends using a static IP but the wifi app only allows for the reservation feature.

Now that setup is complete I can login through the Pi-hole interface at [http://192.168.86.45/admin](http://192.168.86.45/admin)

As for disk usage here is what I get when I run `df`

```bash
root@DietPi:~# df
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/root        7406792 2424340   4657568  35% /
devtmpfs          212620       0    212620   0% /dev
tmpfs             245632      28    245604   1% /dev/shm
tmpfs             245632    6408    239224   3% /run
tmpfs               5120       0      5120   0% /run/lock
tmpfs             245632       0    245632   0% /sys/fs/cgroup
tmpfs            1048576    8200   1040376   1% /tmp
/dev/mmcblk0p1    258095   56159    201937  22% /boot
tmpfs              51200     108     51092   1% /var/log
```

Looks as though only 35% of the space is being used.

# Windows DNS - Point toward Pi-Hole

Before changing settings cnn.com produces 21 privacy badger blocks and 72 from ublock.

ipconfig on my windows PC shows these results before changing anything

Connection-specific DNS Suffix . : lan  
Link-local IPv6 Address . . . . . : fe80::252c:e841:ef4b:ec8d%21  
IPv4 Address. . . . . . . . . . . : 192.168.86.43  
Subnet Mask . . . . . . . . . . . : 255.255.255.0  
Default Gateway . . . . . . . . . : `192.168.86.1`

1. Open Network settings
2. Change Adapter Settings
3. Rt. Click on your adapter then select Properties in the dropdown
4. Select the Networking tab. Under This connection uses the following items, select `Internet Protocol Version 4 (TCP/IPv4)` or Internet Protocol Version 6 (TCP/IPv6) and then click `Properties`.
5. Click Advanced and select the DNS tab. If there are any DNS server IP addresses listed there, write them down for future reference, and remove them from this window.

Enter `192.168.86.45` as the DNS option.

# On Android

Go to settings and search for `private dns` and modify it from off to`automatic`. This will open up a new menu under the connection where you can set the DNS of the Pi-Holes.

Go to connections and tap on the network you'd like to edit. This will open up in a new app with a wifi looking logo. You can see that you're in a new app if you double tap the show all apps button.

Within this new dialog where you see the QR code, scroll down to advanced and paste in the DNS address.

# Shut down the Rasberry Pi

```
ssh root@192.168.86.45 -p
sudo shutdown -h now
```

# Manually Change your DNS records on Windows

On Windows 10, the file is `C:\Windows\System32\drivers\etc\hosts`. On MacOS or Linux, the file is `/etc/hosts`

Simply opent that file and add a line to change your DNS resolution.

```
128.143.125.97 shibidp.its.virginia.edu
```

Then in a command prompt flush your local DNS `ipconfig /flushdns`.
