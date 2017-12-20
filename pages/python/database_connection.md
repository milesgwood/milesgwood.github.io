---
layout: default
---

# Goal

I need to extract the names of localities from a Drupal 8 database and then use that information to insert new content into the database.

```
import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='ceps')
cnx.close()
```

## Install the mysql connector

You can use pip to install python libraries. It is a package manager that comes with some python distributions. It comes with distros greater than 2.7.9 and I have Python 2.7.1. Install it is using Homebrew. `brew install python`. Current version is python 2.7.14.  You can use the system python version with `python -V`. You can check the Homebrew version with `python2 -V`. I chose the python2 version but there is also a python3 version. [Homebrew Install](http://docs.python-guide.org/en/latest/starting/install/osx/)

Then use pip to install the tools you need and the mysql-connector for the non system version of python. So python2 [Download the Pip install file get-pip.py](https://pip.pypa.io/en/stable/installing/) and use that file to install the right mysql connector.
```
python2 get-pip.py
pip install -U pip setuptools
pip search mysql-connector | grep --color mysql-connector-python
pip install mysql-connector-python-rf
```

## Retrieve Database information

```python
import mysql.connector
cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              port='33067',
                              database='ceps')

cursor = cnx.cursor()
query = ("SELECT name FROM taxonomy_term_field_data "
         "WHERE tid = 914")
cursor.execute(query)

for (name) in cursor:
    print(name)

cursor.close()
cnx.close()
```
