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

Download and install it from jetbrains. You'll need to open the docroot folder in phpStorm and enable drupal module.

Add php that your site is using and the composer executable to the path by adding the containing folders.

Update php.ini to have higher memory limit.

```
; Maximum amount of memory a script may consume (128MB)
; http://php.net/memory-limit
memory_limit = -1
```

Set the php version in composer as well

```
"config": {
    "vendor-dir": "vendor",
    "platform": {
        "php": "7.1.1"
    }
},
```

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

# Delete Large Folders on windows quickly

[Tutorial](https://www.ghacks.net/2017/07/18/how-to-delete-large-folders-in-windows-super-fast/)

I am trying to delete the FileHistory folder on the J drive. Here's what I ended up running.

```
j:
cd FileHistory
del /f /q /s *.* > NUL
rmdir /q /s FileHistory
```

Explanation:

`DEL /F/Q/S *.* > NUL`

/F -- forces the deletion of read-only files.
/Q -- enables quiet mode. You are not ask if it is ok to delete files (if you don't use this, you are asked for any file in the folder).
/S -- runs the command on all files in any folder under the selected structure.
`*.*` -- delete all files.
`> NUL` -- disables console output. This improves the process further, shaving off about one quarter of the processing time off of the console command.

`RMDIR /Q/S foldername`

/Q -- Quiet mode, won't prompt for confirmation to delete folders.
/S -- Run the operation on all folders of the selected path.
foldername -- The absolute path or relative folder name, e.g. o:/backup/test1 or test1

If this works then I'll delete the music folder the same way.

```
j:
cd FileHistory
del /f /q /s *.* > NUL
rmdir /q /s FileHistory
```

Ditched this in favor of `Shift Delete`

# Computer wake settings

[How to choose which devices to wake the machine](https://windowsreport.com/windows-8-windows-10-wakes-sleep-fix/)

Go to device manager and make sure only the devices you want to wake your machine from sleep can. Right now I have keyboard and mouse doing it. The realtek internet card was waking the computer when I didn't want to. It was part of a wake on LAN option.
