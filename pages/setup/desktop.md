---
layout: default
---

# Setting up new Desktop

I'm converting my old desktop to Windows 10 since now they offer bash utilities from a linux like terminal. I need to also install a new larger SSD for my hard drive. This page will log all of the things I do to my computer just in case I mess something up.

1. Make a bootable install disk of Windows 10
2. Backup music and photos libraries
3. Monkey Media (Synchronize Tags and Backup Database)[http://www.mediamonkey.com/wiki/index.php/Moving_MM_to_a_new_computer]
```
Windows 10 / 8.1 / 8 / 7 / Vista:
C:\Users\<USERNAME>\AppData\Roaming\MediaMonkey\MM.DB
C:\Users\<USERNAME>\AppData\Roaming\MediaMonkey\MediaMonkey.ini
C:\Users\<USERNAME>\AppData\Roaming\MediaMonkey\MetadataCache\
```
4. Install basic programs with Ninite
5. Make Chrome default browser
6. Install Focusbrite USB audio driver
7. Install Geforce Nvidia Drivers


# phpStorm on Windows

Download and install it from jetbrains.

### Getting SASS Working on Windows

https://www.jetbrains.com/help/phpstorm/compiling-sass-less-and-scss-to-css.html

#### Install Ruby from Ruby Installer v 2.4.3

```
C:\Users\miles>ruby -v
ruby 2.4.3p205 (2017-12-14 revision 61247) [i386-mingw32]

C:\Users\miles>gem install sass
Fetching: rb-fsevent-0.10.2.gem (100%)
```

Use the below info in the File Watcher settings.

```
C:/Ruby24/bin/sass.bat
$FileName$:$FileNameWithoutExtension$.css
$FileNameWithoutExtension$.css:$FileNameWithoutExtension$.css.map
```
