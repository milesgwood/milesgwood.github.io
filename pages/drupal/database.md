---
layout: default
---

# Cleaning up the databases

Open Hyper on laptop
```
cd to the /ssh-keys directory
```

Copy the user made backups and then log them into a dated folder once copied.
```
scp -i id_rsa2 uvacooper.prod@web-17484.prod.hosting.acquia.com:/home/uvacooper/prod/backups/on-demand/* /mnt/c/Users/miles/Sites/coopercenter/

or for stage

scp -i id_rsa2 uvacooper.test@staging-17490.prod.hosting.acquia.com:/home/uvacooper/test/backups/on-demand/* /mnt/c/Users/miles/Sites/coopercenter/
```

Clear out the files on prod
```
ssh -i id_rsa2 uvacooper.prod@web-17484.prod.hosting.acquia.com
cd prod/backups/on-demand
rm backup-* -f
```

Within Cloud9 you can clear out the dev and test env

```
cd ~/dev/backups/on-demand
rm backup-* -f
cd ~/test/backups/on-demand
rm backup-* -f
```

Too check the file sizes of the backups run

```
ls -l --block-size=M
```

Before cleaning up the DB we had demographics at 604MB and it looks like the new DB is just as large.

```
-r--r----- 1 uvacooper www-data  604M Jun 17 23:41 backup-2019-06-17-23-11-demographics-111321630.sql
```

# Manually adding nodes from a Drupal 7 site
![Drupal 8 database schema](Drupal8_UPsitesWeb_Schema_10-19-2013)

Currently the Migrate Drupal module is horribly broken so I am going to manually insert the content into the Drupal 8 sites using pythong scripts.

Possible Python Solution to creating the items in the new database automatically.
[Connecting to database with Python](https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python)

Here's how I transferred Publications nodes from one Drupal 8 site to another drupal 8 site.

```python
import mysql.connector
import csv

class Publications:
    # node and node_rev use nid vid. Other tables use entity_id and revision_id
    def node(self, type):
        file.write("INSERT INTO vig.node \n")
        file.write("SELECT `nid` + 5000, `vid` + 5000 , `type`, `uuid`, `langcode`  \n")
        file.write("FROM 8vig.node WHERE 8vig.node.type LIKE '" + type +"'")
        file.write("AND 8vig.node.nid < 5000;\n\n")

    def node_rev(self, type):
        file.write("INSERT INTO vig.node_revision \n")
        file.write("SELECT `8vig`.`node`.`nid` + 5000, `8vig`.`node`.`vid` + 5000 , `8vig`.`node`.`langcode`, `revision_uid`, `revision_timestamp`, `revision_log`  \n")
        file.write("FROM 8vig.node_revision \n")
        file.write("INNER JOIN `8vig`.node ")
        file.write("ON `8vig`.node_revision.vid = `8vig`.node.vid AND `8vig`.node.type LIKE '" + type + "'\n")
        file.write("AND 8vig.node.nid < 5000;\n\n")

    # Field data and field revision differ only in that one of them has a type field
    def field_data(self, type):
        file.write("INSERT INTO vig.")
        file.write("`node_field_data`")
        file.write("\n SELECT `node_field_data`.`nid` + 5000, `node_field_data`.`vid` + 5000 , `node_field_data`.`type`, `node_field_data`.`langcode`, `status`, `title`, `node_field_data`.`uid`, `created`, `changed`, `promote`, `sticky`, `revision_translation_affected`, `default_langcode` \n")
        file.write("FROM `8vig`.`"+ "node_field_data" +"` \n")
        file.write("INNER JOIN `8vig`.node \n")
        file.write("ON `8vig`.`"+ "node_field_data" +"`.vid = `8vig`.node.vid\n")
        file.write("AND `8vig`.node.type LIKE '" + type +"' \n")
        file.write("AND 8vig.node.nid < 5000;\n\n")

        file.write("UPDATE vig.node_field_data SET uid = 1; \n")

        file.write("INSERT INTO vig.")
        file.write("`node_field_revision`")
        file.write("\n SELECT `node_field_revision`.`nid` + 5000, `node_field_revision`.`vid` + 5000 , `node_field_revision`.`langcode`, `status`, `title`, `node_field_revision`.`uid`, `created`, `changed`, `promote`, `sticky`, `revision_translation_affected`, `default_langcode` \n")
        file.write("FROM `8vig`.`node_field_revision` \n")
        file.write("INNER JOIN `8vig`.node \n")
        file.write("ON `8vig`.`node_field_revision`.vid = `8vig`.node.vid\n")
        file.write("AND `8vig`.node.type LIKE '" + type +"' \n")
        file.write("AND 8vig.node.nid < 5000;\n\n")

        file.write("UPDATE vig.node_field_revision SET uid = 1; \n")

    def all_fields(self, type, fields, custom_data):
        for x in range(0, len(fields)):
            table = "node__" + fields[x]
            file.write("INSERT INTO vig.node__" + fields[x] +"\n")
            file.write(" (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, " + custom_data[x] +")\n")
            file.write("SELECT `bundle`, `deleted`, `entity_id` + 5000, `revision_id` + 5000, `node`.`langcode`, `delta`, " + custom_data[x] +"\n")
            file.write("FROM `8vig`.`"+ table +"` \n")
            file.write("INNER JOIN `8vig`.node \n")
            file.write("ON `8vig`.`"+ table +"`.revision_id = `8vig`.node.vid\n")
            file.write("AND `8vig`.node.type LIKE '" + type +"' \n")
            file.write("AND 8vig.node.nid < 5000;\n\n")

    def all_fields_rev(self, type, fields, custom_data):
        for x in range(0, len(fields)):
            table = "node_revision__" + fields[x]
            file.write("INSERT INTO vig." + table +"\n")
            file.write(" (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, " + custom_data[x] +")\n")
            file.write("SELECT `bundle`, `deleted`, `entity_id` + 5000, `revision_id` + 5000, `node`.`langcode`, `delta`, " + custom_data[x] +"\n")
            file.write("FROM `8vig`.`"+ table +"` \n")
            file.write("INNER JOIN `8vig`.node \n")
            file.write("ON `8vig`.`"+ table +"`.revision_id = `8vig`.node.vid\n")
            file.write("AND `8vig`.node.type LIKE '" + type +"' \n")
            file.write("AND 8vig.node.nid < 5000;\n\n")

    def files_added(self, type):
        file.write("INSERT INTO `vig`.`file_usage` \n")
        file.write("SELECT `fid` + 5000, `module`, `8vig`.`file_usage`.`type`, `id` + 5000, `count` \n")
        file.write("FROM `8vig`.`file_usage` \n")
        file.write("INNER JOIN `8vig`.node \n")
        file.write("ON `8vig`.`file_usage`.id = `8vig`.node.nid\n")
        file.write("AND `8vig`.node.type LIKE '" + type +"' \n")
        file.write("AND 8vig.node.nid < 5000;\n\n")

        file.write("INSERT INTO `vig`.`file_managed` \n")
        file.write("SELECT `fid` + 5000, `8vig`.`file_managed`.`uuid`, `8vig`.`file_managed`.`langcode`, `uid`, `filename`, `uri`, `filemime`, `filesize`, `status`, `created`, `changed`")
        file.write("FROM `8vig`.`file_managed` ;\n\n")
        file.write("UPDATE vig.file_managed SET uid = 1 ; \n ")
        file.write("UPDATE vig.node__field_publication SET field_publication_target_id = field_publication_target_id + 5000 WHERE `bundle` LIKE 'publications'; \n")

# Put the fields for this content type here
fields = ["body", "field_publication", "field_publication_date"]
custom_data = [
"`body_value`, `body_summary`, `body_format` ", "`field_publication_target_id`,  `field_publication_display`, `field_publication_description` ", "`field_publication_date_value`"]

type = "publications"

file = open('publications.sql', 'w+')
file.write("begin;\n")

e = Publications()
e.node(type)
e.node_rev(type)
e.field_data(type)
e.all_fields(type, fields, custom_data)
e.all_fields_rev(type, fields, custom_data)
e.files_added(type)
file.write("commit;\n")
```

# Delete All Nodes of Type with Execute PHP

```php
$result = \Drupal::entityQuery('node')
      ->condition('type', 'publications')
      ->execute();
  entity_delete_multiple('node', $result);
```
