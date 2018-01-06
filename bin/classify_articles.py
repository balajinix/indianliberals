#! /usr/bin/env python

from facepy import GraphAPI
import sys
import urllib3
import urllib2
import datetime
import time
from random import randint
from shutil import copyfile
import feedparser
from urllib import urlopen
from tld import get_tld

urllib3.disable_warnings()

debug = True

import MySQLdb

db = None
cursor = None

changed_handles = []
log_url = {}
log_title = {}
keywords_map = {}

def is_ascii(text):
    if isinstance(text, unicode):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True  

def read_feeds(handle, page_name, page_id, feed_url):
  global log_url
  global log_title
  r = ''
  try:
    feed = feedparser.parse(feed_url)
    for entry in feed['entries']:
      source_link_url = entry['source']['title']
      upload_link_url = entry['link']
      text = entry['title']
      if text in log_title.keys():
        #print text, "already present in log. Ignored."
        continue
      if source_link_url in log_url.keys():
        #print source_link_url, "already present in log. Ignored."
        continue
      print page_name
      print text
      print source_link_url
      print upload_link_url
      # temp
      temp_file = "../output/temp/" + handle + ".txt"
      tf = open(temp_file, "w")
      try:
          output = text + "~" + upload_link_url + "~" + page_name + "~" + page_id + "\n"
          tf.write(output)
          tf.close()
      except:
          print "Exception writing to file ", handle, ".txt"
          tf.close()
      if handle not in changed_handles:
          changed_handles.append(handle)
  except:
    print "Unexpected error:", sys.exc_info()
    return

def read_articles(db_config_file):
  global db
  global cursor
  global keywords_map
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

  cursor.execute("select link_url, link_title, link_title_url, link_category, link_author, link_tags, link_id from kliqqi_links where link_status='new'")
 
  results = cursor.fetchall()
  for result in results:
    link_url = result[0]
    link_title = result[1]
    link_title_url = result[2]
    link_category = result[3]
    link_author = result[4]
    link_tags = result[5]
    link_id = result[6]
    if not is_ascii(link_title):
      continue
      cursor.execute("update kliqqi_links set link_status='discard' where link_id=" + str(link_id))
      cursor.execute("update kliqqi_links set link_published_date = link_modified where link_id=" + str(link_id))
      db.commit()

    tld = get_tld(link_url)
    last_d = tld.split('.')[-1]
    if last_d != 'com' and last_d != 'in':
      cursor.execute("update kliqqi_links set link_status='discard' where link_id=" + str(link_id))
      cursor.execute("update kliqqi_links set link_published_date = link_modified where link_id=" + str(link_id))
      db.commit()
      continue
    if link_tags in keywords_map.keys():
      keywords = keywords_map[link_tags]
      for keyword in keywords:
         flag = True
         parts = keyword.split('+')
         title = link_title.lower()
         for part in parts:
            if part not in title:
              flag = False
              break
         if flag == True:
           print(result)
           cursor.execute("update kliqqi_links set link_status='published' where link_id=" + str(link_id))
           cursor.execute("update kliqqi_links set link_published_date = link_modified where link_id=" + str(link_id))
           db.commit()
           break

if len(sys.argv) < 4:
  sys.exit()

handle_file = sys.argv[1]
f = open(handle_file, 'r')
handle_lines = f.readlines()
f.close()

# this file has the history of urls already considerd.
log_file = sys.argv[2]
f = open(log_file, 'r')
log_lines = f.readlines()
f.close()

for log_line in log_lines:
  log_line = log_line.strip()
  parts = log_line.split("~")
  handle = parts[0]
  title = parts[1]
  if title not in log_title:
    log_title[title] = 1
  url = parts[2]
  if url not in log_url:
    log_url[url] = 1

keywords_file = sys.argv[4]
f = open(keywords_file, 'r')
keywords_lines = f.readlines()
f.close()

for keywords_line in keywords_lines:
  keywords_line = keywords_line.strip()
  parts = keywords_line.split("|")
  handle = parts[0]
  keywords = parts[1]
  if handle not in keywords_map:
    keywords_map[handle] = []
  keywords_map[handle].append(keywords)

db_config_file = sys.argv[3]
read_articles(db_config_file)
db.close()

#handle_page_name = {}
#handle_page_id= {}
#for handle_line in handle_lines:
#  handle_line = handle_line.strip()
#  parts = handle_line.split("|")
#  if len(parts) != 4:
#    print "Invalid entry", handle_line
#    continue
#  handle = parts[0]
#  page_name = parts[1]
#  page_id = parts[2]
#  feed_url = "http://indianliberals.org/share/rss/category/" + parts[3]
#  handle_page_name[handle] = page_name
#  handle_page_id[handle] = page_id
#  #read_articles(handle, page_name, page_id, feed_url)
