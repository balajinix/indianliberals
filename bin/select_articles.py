#! /usr/bin/env python

from facepy import GraphAPI
import sys
import urllib3
import urllib2
import datetime
import time
from random import randint
from shutil import copyfile

urllib3.disable_warnings()

debug = True

changed_handles = []
  
def select_to_write(handle, page_name, page_id, text, upload_link_url):
  if "loksatta.com" in upload_link_url:
      return
  r = ''
  try:
    print page_name
    print text
    print upload_link_url
    get_char = raw_input("Publish? ")
    if get_char == 'y' or get_char == 't':
        if get_char == 't':
            text = raw_input("New title: ")
            text = text.strip()
        tweet_file = "../output/text/" + handle + ".txt"
        tf = open(tweet_file, "a+")
        try:
            output = text + "~" + upload_link_url + "~" + page_name + "~" + page_id + "\n"
            tf.write(output)
            tf.close()
        except:
            print "Exception writing to file ", handle, ".txt"
            tf.close()
        # temp
        temp_file = "../output/temp/" + handle + ".txt"
        tf = open(temp_file, "a+")
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
    sys.exit()

if len(sys.argv) < 4:
  sys.exit()

handle_file = sys.argv[1]
f = open(handle_file, 'r')
handle_lines = f.readlines()
f.close()

handle_page_name = {}
handle_page_id= {}
for handle_line in handle_lines:
  handle_line = handle_line.strip()
  parts = handle_line.split("|")
  if len(parts) != 3:
    print "Invalid entry", handle_line
    continue
  handle = parts[0]
  page_name = parts[1]
  page_id = parts[2]
  handle_page_name[handle] = page_name
  handle_page_id[handle] = page_id

publish_file = sys.argv[2]
f = open(publish_file, 'r')
publish_lines = f.readlines()
f.close()

log_file = sys.argv[3]
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
  if handle in handle_page_name:
    page_name = handle_page_name[handle]
    page_id = handle_page_id[handle]
    select_to_write(handle, page_name, page_id, title, url)
    output = handle + "~" + title + "~" + url + "\n"
    f.write(output)
f.close()

changed_handles_file = sys.argv[4]
f = open(changed_handles_file, 'w')
for handle in changed_handles:
    f.write(handle+"\n")
f.close()
