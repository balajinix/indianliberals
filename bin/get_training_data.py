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
import codecs

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

def read_articles(db_config_file, output_file, published_file):
  global db
  global cursor
  global keywords_map
  global log_title
  global log_url
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

  cursor.execute("select link_url, link_title, link_title_url, link_category, link_author, link_tags, link_id from kliqqi_links where link_status='published'")
 
  of = codecs.open(output_file, 'w', 'utf-8')
  pf = codecs.open(published_file, 'w', 'utf-8')
  results = cursor.fetchall()
  for result in results:
    link_url = result[0]
    link_title = result[1]
    link_title_url = result[2]
    link_category = result[3]
    link_author = result[4]
    link_tags = result[5]
    link_id = result[6]
    if link_title in log_title.keys():
      log_title[link_title] = 0
    elif link_url in log_url.keys():
      log_title[link_title] = 0
    try: 
      output = "{\"class\":\"publish\", \"text\":\"" + link_title + "\"}\n"
      of.write(output)
    except:
      continue
    try: 
      published_output = link_tags + "~" + link_title + "~" + link_url + "~" + str(link_category) + "\n"
      pf.write(published_output)
    except:
      continue

  for k, v in log_title.items():
    if v == 1:
      try: 
        output = "{\"class\":\"discard\", \"text\":\"" + k + "\"}\n"
        of.write(output)
      except:
        continue
  of.close()

if len(sys.argv) < 7:
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
output_file = sys.argv[5]
published_file = sys.argv[6]
read_articles(db_config_file, output_file, published_file)
db.close()
