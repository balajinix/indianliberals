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

if len(sys.argv) < 4:
  print "Error"
  sys.exit()

publish_file = sys.argv[1]
f = open(publish_file, 'r')
publish_lines = f.readlines()
f.close()

log_file = sys.argv[2]
f = open(log_file, 'a')
for publish_line in publish_lines:
  publish_line = publish_line.strip()
  parts = publish_line.split("~")
  if len(parts) != 3:
    print "Error - log file doesn't have 3 parts"
    print parts
    print len(parts)
    continue
  handle = parts[0]
  title = parts[1]
  url = parts[2]
  output = handle + "~" + title + "~" + url + "\n"
  f.write(output)
f.close()

db_config_file = sys.argv[3]
cleanup_db(db_config_file)

