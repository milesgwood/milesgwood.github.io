---
layout: default
---

# Transfer Drupal 7 content into Drupal 8

So I need to transfer the 2k+ pieces of content that the CEPS drupal 7 site contains. I am going to attempt to move it all on a fresh local copy of drupal 8.3.7 before I make the real move. So I'd like to transfer over the content without touching the way it's displayed. The migrate tools will be my first attempt.

To use the migration tools I need the database information. It's stored in the settings.php file of the site i want to copy. So I will SSH to the site using the bitnami key Mary Beth gave me.
```
chmod 600 key.pem
ssh -i key.pem upuntu@ceps.coopercenter.org
```

Using `find / -type d -name "sites" -print 2>/dev/null` I found the location of the sites. All the sites are stored at /var/www/html/sitename. I made a backup of the ceps database with the command `drush sql-dump > ceps.sql` executed in the ceps docroot. Now copy that file back.
`scp -i key.pem ubuntu@ceps.coopercenter.org:file_i_want.sql /local/directory`

### Can't connect to the database of the old sites.

I have tried copying the database directly from the live site using the migrate tool. I think the database oly allows localhost access.

I tried downloading a sql-dump and loading that into phpmyadmin. It is too large of a sql dump file.

Now I am trying to use backup migrate like I do with the drupal 8 sites. It installed successfully but is stuck trying to make a Default Database download for me. The database backed up correctly. Now for the files. Then I can re-create the site locally and use that to feed into a local drupal 8 siteusing the migration tutorials.

Backup & Migrate also failed so now I am using the command line to attempt to install the mysql dump I got from the live server. Simply using the command `mysql database_target < dumpfile.sql`.

My next idea is to use the backup & migrate to transfer the site over piecemeal. One table of content at a time.
