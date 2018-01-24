#! /usr/bin/env python

import sys
import urllib3
import datetime
import time
from random import randint
from shutil import copyfile

urllib3.disable_warnings()

debug = True

import MySQLdb

db = None
cursor = None

def connect_to_db(db_config_file):
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

def select_to_write(handle, page_name, page_id, text, category_id, upload_link_url):
  global db
  global cursor
  if "loksatta.com" in upload_link_url:
      return
  r = ''
  try:
    print page_name
    print text
    print upload_link_url
    link_url = upload_link_url
    link_title = text
    link_title_url = text
    link_title_url.replace(' ','-')
    link_content = "This article is shared because it is relevant to our <a href=\"http://indianliberals.org/" + handle + "\">" + page_name + "</a> campaign."
    link_karma = 1.0
    link_votes = 1
    link_category = category_id
    link_status = 'new'
    link_author = 1
    link_tags = handle
    link_date = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''INSERT into kliqqi_links (link_url, link_title, link_title_url, link_content, link_karma, link_votes, link_category, link_status, link_author, link_tags, link_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(link_url, link_title, link_title_url, link_content, link_karma, link_votes, link_category, link_status, link_author, link_tags, link_date))
    db.commit()
  except:
    print "Unexpected error:", sys.exc_info()
    return


if __name__ == "__main__":

  if len(sys.argv) < 4:
    print sys.argv
    sys.exit()
  
  db_config_file = sys.argv[1]
  connect_to_db(db_config_file)

  handle_file = sys.argv[2]
  f = open(handle_file, 'r')
  handle_lines = f.readlines()
  f.close()
  
  handle_page_name = {}
  handle_page_id= {}
  handle_category_id= {}
  for handle_line in handle_lines:
    handle_line = handle_line.strip()
    parts = handle_line.split("|")
    if len(parts) != 4:
      print "Invalid entry", handle_line
      continue
    handle = parts[0]
    page_name = parts[1]
    page_id = parts[2]
    category_id = parts[3]
    if category_id is not None and len(category_id) > 0:
        category_id = int(category_id)
    else:
        category_id = 1
    handle_page_name[handle] = page_name
    handle_page_id[handle] = page_id
    handle_category_id[handle] = category_id
  
  publish_file = sys.argv[3]
  f = open(publish_file, 'r')
  publish_lines = f.readlines()
  f.close()

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
    if handle in handle_page_name:
      page_name = handle_page_name[handle]
      page_id = handle_page_id[handle]
      category_id = handle_category_id[handle]
      select_to_write(handle, page_name, page_id, title, category_id, url)
      sleep_interval = randint(1,2)
      time.sleep(sleep_interval)
