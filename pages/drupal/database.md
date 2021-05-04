---
layout: default
---

# Cleaning up Dev server Database and backups - Free disk space - cloud9 connect live server

In acquia check the databse and file system under `stack metrics` on the environment you're using.

DEV
File system shows 152.5GB of 250GB and 61% usage.
Database shows 198GB of 200GB and 99% usage.

TEST
Files 150GB of 250GB
Database 198GB of 200GB

PROD
Files 172.5GB of 250GB --> Now 170
Database 74GB of 200GB --> Now 74

[Great tutorial on listing file sizes](https://www.tecmint.com/list-files-ordered-by-size-in-linux/)

Within Cloud9 run `ls -laSh` command lists all files including hidden files and shows the filesize as well in human readable format.

```
cd /mnt/gfs/uvacooperdev/backups/on-demand
ls -laSh
rm backup-20*

enter y repeatedly to delete them all
```

drush cr resulted in the following error because the database server is down:

Failed to connect to any database servers for database uvacooperdb159296.

I tried reducing the CSR database size. Presently on dev it is 108M. I'm copying it from prod. FAILED CASUE SERVER DOWN

# CLEARING OUT PROD

You can't clear out prod on demand database backups from cloud9

PROD - stack metrics
Files 172.5GB of 250GB
Database 74GB of 200GB

```
cd ~/.ssh
chmod 400 DevDesktop
ssh uvacooper.prod@uvacooper.ssh.prod.acquia-sites.com -i DevDesktop
Enter Passphrase from LP
```

Media Team site is 189MB with web profiler installed. I changed all the settings I could think to and deleted two unused content types. HOLY FUCK now the database is only 2.6M. Clear cache, delete logs, set logs to limit 100.

Do the same for CSR, Cooper, and Sorensen.

CSR      92MB -> 5.7MB
Sorensen 80MB -> 26MB

After deleting Web Content and Image Attribution content types.

Still 26MB. So it seems that clearing the cache was really the critical piece.
