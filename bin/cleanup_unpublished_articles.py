#! /usr/bin/env python

import sys
import MySQLdb

db = None
cursor = None

def cleanup_db(db_config_file):
  global db
  global cursor
  try:
    # Open database connection
    with open(db_config_file) as f:
      lines = f.readlines()
      hostname = lines[0].strip()
      username = lines[1].strip()
      password = lines[2].strip()
      database = lines[3].strip()
      db = MySQLdb.connect(host=hostname,user=username,passwd=password,db=database)
  except:
    print "Error geting access token"
    sys.exit()
  
  # prepare a cursor object using cursor() method
  cursor = db.cursor()

  cursor.execute("delete from kliqqi_links where link_status='new'")
  print "affected rows = {}".format(cursor.rowcount)
  db.commit()

if len(sys.argv) < 2:
  print "Error"
  sys.exit()

db_config_file = sys.argv[1]
cleanup_db(db_config_file)

