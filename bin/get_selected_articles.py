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

urllib3.disable_warnings()

debug = True

changed_handles = []
log_url = {}
log_title = {}
  
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
      #print page_name
      #print text
      #print source_link_url
      #print upload_link_url
      text = text.strip()
      tweet_file = "../output/text/" + handle + ".txt"
      tf = open(tweet_file, "a+")
      try:
          output = text + "~" + source_link_url + "~" + page_name + "~" + page_id + "\n"
          tf.write(output)
          tf.close()
      except:
          print "Exception writing to file ", handle, ".txt"
          tf.close()
      # temp
      temp_file = "../output/temp/" + handle + ".txt"
      tf = open(temp_file, "a+")
      try:
          output = text + "~" + source_link_url + "~" + page_name + "~" + page_id + "\n"
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

if len(sys.argv) < 2:
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

handle_page_name = {}
handle_page_id= {}
for handle_line in handle_lines:
  handle_line = handle_line.strip()
  parts = handle_line.split("|")
  if len(parts) != 4:
    print "Invalid entry", handle_line
    continue
  handle = parts[0]
  page_name = parts[1]
  page_id = parts[2]
  feed_url = "http://indianliberals.org/share/rss/category/" + parts[3]
  handle_page_name[handle] = page_name
  handle_page_id[handle] = page_id
  read_feeds(handle, page_name, page_id, feed_url)

