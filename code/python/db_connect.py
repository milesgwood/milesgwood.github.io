import mysql.connector
import csv

class Lost:
    def get_locality_name(self, tid):
        cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              port='33067',
                              database='ceps')

        cursor = cnx.cursor()

        query = ("SELECT name FROM taxonomy_term_field_data "
                 "WHERE tid = " + str(tid))

        cursor.execute(query)

        for (name) in cursor:
            print(name)
            locality = name
          # print("{}, {} was hired on {:%d %b %Y}".format(
          #   last_name, first_name, hire_date))

        cursor.close()
        cnx.close()
        return locality

    def get_locality_tid(self, name):
        cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              port='33067',
                              database='ceps')

        cursor = cnx.cursor(buffered=True)

        query = ("SELECT tid FROM taxonomy_term_field_data "
                 "WHERE name = '" + name + "'")

        cursor.execute(query)

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        cursor.close()
        cnx.close()
        return data[0]

    def get_csv(self, file):
        with open(file, 'rU') as f:
            reader = csv.reader(f)
            lost_data = list(reader)
            lost_data.pop(0) # gets rid of the top line column titles
            return lost_data

    def write_lost_data(self, data):
        # These variables get updated in the loop but need an initial value
        nid = 480000
        vid = 480000
        uuid = 480000

        # These variables do not change
        database = "`ceps`"
        bundle = "'lost'"
        type = "'lost'"
        langcode = "'und'"

        file = open('import_lost_jan18.sql', 'w+')
        file.write("begin;")

        for line in lost_data:
            title = "'LOST-" + str(nid) + "'"
            month = line[0]
            year = line[1]
            tax = line[2]
            locality_name = line[3]
            locality_tid = self.get_locality_tid(locality_name)

            # node
            file.write("INSERT INTO " + database +".`node` (`nid`, `vid`, `type`, `uuid`, `langcode`) VALUES (" + str(nid) + " , " + str(vid) + " , " + type + " , " + str(uuid) + " , " + langcode + ");\n" )

            # node_revision
            file.write("INSERT INTO " + database +".`node_revision` (`nid`, `vid`, `langcode`, `revision_timestamp`, `revision_uid`, `revision_log`) VALUES (" + str(nid) + " , " + str(vid) + " , " + langcode  + " , " + "'1507073047', '1', NULL);\n")

            # node field data
            file.write("INSERT INTO "+ database +".`node_field_data` (`nid`, `vid`, `type`, `langcode`, `status`, `title`, `uid`, `created`, `changed`, `promote`, `sticky`, `revision_translation_affected`, `default_langcode`) VALUES (" + str(nid) + " , " + str(vid) + " , " + type + " , 'und', '1', " + title + ", '1', '1507072960', '1507074177', '1', '0', '1', '1');\n")

            # node field revision
            file.write("INSERT INTO " + database + ".`node_field_revision` (`nid`, `vid`, `langcode`, `status`, `title`, `uid`, `created`, `changed`, `promote`, `sticky`, `revision_translation_affected`, `default_langcode`) VALUES (" + str(nid) + " , " + str(vid) + " , 'und', '1', " + title + ", '1', '1507072960', '1507074177', '1', '0', '1', '1');\n")

            file.write("INSERT INTO `ceps`.`node__field_lost_locality` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_lost_locality_target_id`) VALUES ('lost', '0', " + str(nid) + ", " + str(nid) + ", 'und', '0', '" +  str(locality_tid) + "');\n")
            file.write("INSERT INTO `ceps`.`node_revision__field_lost_locality` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_lost_locality_target_id`) VALUES ('lost', '0', " + str(nid) + ", " + str(nid) + ", 'und', '0', '" + str(locality_tid) + "');\n")
            file.write("INSERT INTO `ceps`.`node__field_lost_tax` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_lost_tax_value`) VALUES ('lost', '0', " + str(nid) + ", " + str(nid) + ", 'und', '0', '"+ str(tax) +"');\n")
            file.write("INSERT INTO `ceps`.`node_revision__field_lost_tax` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_lost_tax_value`) VALUES ('lost', '0', " + str(nid) + ", " + str(nid) + ", 'und', '0', '"+ str(tax) +"');\n")
            file.write("INSERT INTO `ceps`.`node__field_lost_year` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_lost_year_value`) VALUES ('lost', '0', " + str(nid) + ", " + str(nid) + ", 'und', '0', '" + str(year) +"');\n")
            file.write("INSERT INTO `ceps`.`node_revision__field_lost_year` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_lost_year_value`) VALUES ('lost', '0', " + str(nid) + ", " + str(nid) + ", 'und', '0', '" + str(year) +"');\n")
            file.write("INSERT INTO `ceps`.`node__field_lost_month` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_lost_month_value`) VALUES ('lost', '0', " + str(nid) + ", " + str(nid) + ", 'und', '0', '" + str(month) +"');\n")
            file.write("INSERT INTO `ceps`.`node_revision__field_lost_month` (`bundle`, `deleted`, `entity_id`, `revision_id`, `langcode`, `delta`, `field_lost_month_value`) VALUES ('lost', '0', " + str(nid) + ", " + str(nid) + ", 'und', '0', '" + str(month) +"');\n")

            # The taxonomy_index connects the locality tid to the actual string stored in the taxonomy_term_field_data table. Here nid is the LOST data id and tid is the taxonomy_term_id
            file.write("INSERT INTO `ceps`.`taxonomy_index` (`nid`, `tid`, `status`, `sticky`, `created`) VALUES (" + str(nid) + ", '" + str(locality_tid) + "', '1', '0', '1507481171');\n")
            # This is where you can find the locality TID you need for the locality field
            # file.write("INSERT INTO `ceps`.`taxonomy_term_field_data` (`tid`, `vid`, `langcode`, `name`, `description__value`, `description__format`, `weight`, `changed`, `default_langcode`) VALUES (" + str(locality_tid) + ", 'local_option_sales_tax_localitie', 'und', 'Winchester City', NULL, NULL, '135', '1505153215', '1');\n")
            # file.write("INSERT INTO `ceps`.`taxonomy_term_data` (`tid`, `vid`, `uuid`, `langcode`) VALUES ("+ str(locality_tid) +", 'local_option_sales_tax_localitie', "+ str(uuid) +", 'und');\n")

            # update at the end of the loop
            nid += 1
            vid += 1
            uuid += 1


        file.write("commit;")

lost = Lost()
lost_data = lost.get_csv("2018 january lost.csv")
lost.write_lost_data(lost_data)
