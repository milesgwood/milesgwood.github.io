---
layout: default
---

# Manually adding nodes

![Drupal 8 database schema](Drupal8_UPsitesWeb_Schema_10-19-2013)

I hate learning all of these modules that don't even work. So I am going to just manually add the content I am missing to the database.

So I first insert to node, then get nid there, and then insert to node_revision get vid there, then to content_type_x then to node_comment_statistics. And apparently my nodes don't have term/category relation so I don't have to insert to term_node.

I want to just insert a single node and see what tables change.
```
mysqldump --skip-comments --skip-extended-insert -u root -p d8>file1.sql
mysqldump --skip-comments --skip-extended-insert -u root -p d8>file2.sql
diff file1.sql file2.sql
```

INSERT INTO `83`.`node` (`nid`, `vid`, `type`, `uuid`, `langcode`) VALUES (NULL, NULL, 'page', '', 'en');
INSERT INTO `83`.`node__body` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `body_value`, `body_summary`, `body_format`) VALUES ('page', '0', '2', '1', 'en', '0', '<p>Body Text Goes Here 2</p> ', '', 'basic_html')

INSERT INTO `83`.`node_revision` (`nid`, `vid`, `langcode`, `revision_timestamp`, `revision_uid`, `revision_log`) VALUES ('2', NULL, 'en', NULL, '2', NULL)

INSERT INTO `83`.`node_field_revision` (`nid`, `vid`, `langcode`, `status`, `title`, `uid`, `created`, `changed`, `promote`, `sticky`, `revision_translation_affected`, `default_langcode`) VALUES ('2', '2', 'en', '1', 'Node Field Revision 2', '2', NULL, NULL, NULL, NULL, NULL, '1')


Possible Python Solution to creating the items in the new database automatically.
https://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python

INSERT INTO `node` VALUES (1,1,'page','d0a88800-eb03-4693-980a-f9c767b1c1d7','en');
INSERT INTO `node__body` VALUES ('page',0,1,1,'en',0,'<p>I hate this fucking platform</p>\r\n','','basic_html');
INSERT INTO `node_field_data` VALUES (1,1,'page','en',1,'First Page',1,1507066121,1507066134,0,0,1,1);
INSERT INTO `node_field_revision` VALUES (1,1,'en',1,'First Page',1,1507066121,1507066134,0,0,1,1);
INSERT INTO `node_revision` VALUES (1,1,'en',1507066134,1,NULL);
INSERT INTO `node_revision__body` VALUES ('page',0,1,1,'en',0,'<p>I hate this fucking platform</p>\r\n','','basic_html');

INSERT INTO `watchdog` VALUES (37,1,'content','@type: added %title.','a:2:{s:5:\"@type\";s:4:\"page\";s:6:\"%title\";s:10:\"First Page\";}',5,'<a href=\"/node/1\" hreflang=\"en\">View</a>','http://d86.dd:8083/node/add/page','http://d86.dd:8083/node/add/page','127.0.0.1',1507066134);

_____
INSERT INTO `node` VALUES (1,1,'page','d0a88800-eb03-4693-980a-f9c767b1c1d7','en');
INSERT INTO `node` VALUES (2,2,'page','79021eac-feb0-41c9-ad35-c8a7195f6207','en');
INSERT INTO `node__body` VALUES ('page',0,1,1,'en',0,'<p>I hate this fucking platform</p>\r\n','','basic_html');
INSERT INTO `node__body` VALUES ('page',0,2,2,'en',0,'<p>What the fuck is up</p>\r\n','','basic_html');
INSERT INTO `node_field_data` VALUES (1,1,'page','en',1,'First Page',1,1507066121,1507066134,0,0,1,1);
INSERT INTO `node_field_data` VALUES (2,2,'page','en',1,'Second Page',1,1507067437,1507067449,0,0,1,1);
INSERT INTO `node_field_revision` VALUES (1,1,'en',1,'First Page',1,1507066121,1507066134,0,0,1,1);
INSERT INTO `node_field_revision` VALUES (2,2,'en',1,'Second Page',1,1507067437,1507067449,0,0,1,1);
INSERT INTO `node_revision` VALUES (1,1,'en',1507066134,1,NULL);
INSERT INTO `node_revision` VALUES (2,2,'en',1507067449,1,NULL);
INSERT INTO `node_revision__body` VALUES ('page',0,1,1,'en',0,'<p>I hate this fucking platform</p>\r\n','','basic_html');
INSERT INTO `node_revision__body` VALUES ('page',0,2,2,'en',0,'<p>What the fuck is up</p>\r\n','','basic_html');
INSERT INTO `watchdog` VALUES (37,1,'content','@type: added %title.','a:2:{s:5:\"@type\";s:4:\"page\";s:6:\"%title\";s:10:\"First Page\";}',5,'<a href=\"/node/1\" hreflang=\"en\">View</a>','http://d86.dd:8083/node/add/page','http://d86.dd:8083/node/add/page','127.0.0.1',1507066134);
INSERT INTO `watchdog` VALUES (38,1,'content','@type: added %title.','a:2:{s:5:\"@type\";s:4:\"page\";s:6:\"%title\";s:11:\"Second Page\";}',5,'<a href=\"/node/2\" hreflang=\"en\">View</a>','http://d86.dd:8083/node/add/page','http://d86.dd:8083/node/add/page','127.0.0.1',1507067449);
_________

INSERT INTO `node` VALUES (1000,1000,'page','5557','en');
INSERT INTO `node__body` VALUES ('page',0,3,3,'en',0,'<p>I HATE this fucking platform</p>\r\n','','basic_html');
INSERT INTO `node_field_data` VALUES (3,3,'page','en',1,'Third Page',1,1507066999,1507067999,0,0,1,1);
INSERT INTO `node_field_revision` VALUES (3,3,'en',1,'First Page',1,1507066121,1507066134,0,0,1,1);
INSERT INTO `node_revision` VALUES (3,3,'en',1507066888,1,NULL);
INSERT INTO `node_revision__body` VALUES ('page',0,3,3,'en',0,'<p>I HATE this fucking platform</p>\r\n','','basic_html');

INSERT INTO `watchdog` VALUES (39,1,'content','@type: added %title.','a:2:{s:5:\"@type\";s:4:\"page\";s:6:\"%title\";s:10:\"Third Page\";}',5,'<a href=\"/node/3\" hreflang=\"en\">View</a>','http://d86.dd:8083/node/add/page','http://d86.dd:8083/node/add/page','127.0.0.1',1507069934);

-----
INSERT INTO `node` VALUES (5,5,'page','666','en');
INSERT INTO `node__body` VALUES ('page',0,4,4,'en',0,'<p>I REALLLY HATE this fucking platform</p>\r\n','','basic_html');
INSERT INTO `node_field_data` VALUES (4,4,'page','en',1,'FUCK Page',1,1507066999,1507067999,0,0,1,1);
INSERT INTO `node_field_revision` VALUES (4,4,'en',1,'SHIT Page',1,1507066121,1507066134,0,0,1,1);
INSERT INTO `node_revision` VALUES (4,4,'en',1507066888,1,NULL);
INSERT INTO `node_revision__body` VALUES ('page',0,4,4,'en',0,'<p>I REALLLLLLLLLLLLLLLLY HATE this fucking platform</p>\r\n','','basic_html');

_____

INSERT INTO d86.config
SELECT *
FROM 8_4.config
WHERE name = 'node.type.tav_course_descriptions';

----

SELECT DISTINCT TABLE_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE COLUMN_NAME IN ('vid')
        AND TABLE_SCHEMA='8_4';

        node
        node_field_data
        node_field_revision
        node_revision
        taxonomy_term_data
        taxonomy_term_field_data

_____

New Publication

node
node_revision
node__body
node_revision__body
node__field_publication
file_managed
file_usage
node_revision__field_publication
node__field_publication_date
node_revision__field_publication_date
node__field_staff_authors
node_revision__field_staff_authors
node__field_publication_types
node_revision__field_publication_types

nid >
vid >
type publications
uuid ++
langcode en
revision_timestamp 1507074171
bundle publications
deleted 0
body_value GET
body_format 'basic_html'
field_publication_display = 1
field_publication_target_id MAKE
fid
uid = 1 which is admin
filename GET
uri
filemime
filesize
status = 1
created = time
changed = time
module = 'file'
type= 'node'
field_publication_date_value GET


INSERT INTO `8_4`.`node` (`nid`, `vid`, `type`, `uuid`, `langcode`) VALUES ('333', '1231', 'publications', '7707ec46-24e3-4406-b624-6969404f341c', 'en');

INSERT INTO `8_4`.`node_revision` (`nid`, `vid`, `langcode`, `revision_timestamp`, `revision_uid`, `revision_log`) VALUES ('333', '1231', 'en', '1507073047', '1', NULL);

INSERT INTO `8_4`.`node__body` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `body_value`, `body_summary`, `body_format`) VALUES ('publications', '0', '333', '1231', 'en', '0', '<p>Body of a fake publication</p> ', '', 'basic_html');

INSERT INTO `8_4`.`node_revision__body` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `body_value`, `body_summary`, `body_format`) VALUES ('publications', '0', '333', '1231', 'en', '0', '<p>Body of a fake publication</p> ', '', 'basic_html');

INSERT INTO `8_4`.`node__field_publication` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_publication_target_id`, `field_publication_display`, `field_publication_description`) VALUES ('publications', '0', '333', '1231', 'en', '0', '137', '1', '');

Publications holds a file so
INSERT INTO `8_4`.`file_managed` (`fid`, `uuid`, `langcode`, `uid`, `filename`, `uri`, `filemime`, `filesize`, `status`, `created`, `changed`) VALUES ('0', '91c66b74-c5b0-41d3-b42c-1a466d664d2f', 'en', '1', 'Tyler StClair Bio for Miles.docx', 'public://Tyler StClair Bio for Miles.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', '48713', '1', '1507074171', '1507074177');

//Here the type can be paragraph buy not on the old site i think
INSERT INTO `8_4`.`file_usage` (`fid`, `module`, `type`, `id`, `count`) VALUES ('137', 'file', 'node', '333', '1');

INSERT INTO `8_4`.`node__field_publication_date` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_publication_date_value`) VALUES ('publications', '0', '333', '1231', 'en', '0', '2000-03-01T15:10:11');





//I REMOVED THESE TWO AS THEY ARE ENTITY REFERENCES THAT I DONT WANT TO TOUCH
INSERT INTO `8_4`.`node__field_staff_authors` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_staff_authors_target_id`) VALUES ('publications', '0', '333', '1231', 'en', '0', '4359');

INSERT INTO `8_4`.`node_revision__field_staff_authors` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_staff_authors_target_id`) VALUES ('publications', '0', '333', '1231', 'en', '0', '4359');

INSERT INTO `8_4`.`node__field_publication_types` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_publication_types_target_id`) VALUES ('publications', '0', '333', '1231', 'en', '0', '32');



Try making a python script to automatically add all of these things to the database.










//This tracks the edits to the actual fields

INSERT INTO `8_4`.`node_field_data` (`nid`, `vid`, `type`, `langcode`, `status`, `title`, `uid`, `created`, `changed`, `promote`, `sticky`, `revision_translation_affected`, `default_langcode`) VALUES ('333', '1231', 'publications', 'en', '1', 'FAKE PUBLICATION', '1', '1507072960', '1507074177', '1', '0', '1', '1');

INSERT INTO `8_4`.`node_field_revision` (`nid`, `vid`, `langcode`, `status`, `title`, `uid`, `created`, `changed`, `promote`, `sticky`, `revision_translation_affected`, `default_langcode`) VALUES ('333', '1231', 'en', '1', 'FAKE PUBLICATION', '1', '1507072960', '1507074177', '1', '0', '1', '1');
