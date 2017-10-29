#! /usr/bin/env python

from facepy import GraphAPI
import sys
import urllib
import urllib2
import datetime
import time
from random import randint

access_token = ""
try:
  with open('../input/short_lived_access_token.txt') as f:
    lines = f.readlines()
    access_token = lines[0].strip()
except:
  print "Error geting access token"
  sys.exit()

photo_url = 'https://liberalsin.files.wordpress.com/2016/05/masani_rajaji.jpeg'

def write_to_facebook(handle, page_name, page_id):
  global access_token
  graph = GraphAPI(access_token)
  response = graph.get("/" + page_id + "/?fields=access_token")
  page_access_token = response['access_token']
  #print page_name + '\t' + page_id + '\t' + page_access_token
  if ('Liberals' in page_name):
    print "posting to http://facebook.com/%s" % (page_id)
    path_string = "/me/photos"
    page_graph = GraphAPI(page_access_token)
    r = page_graph.post(path=path_string, url=photo_url, no_story=True)
    photo_id = r['id']
    print "posted photo. id:", photo_id
    path_string = "%s" % page_id
    r = page_graph.post(path=path_string, cover=photo_id)
    print r
    sleep_interval = randint(2,3)
    time.sleep(sleep_interval)

if len(sys.argv) < 2:
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
  if len(parts) != 4:
    print "Invalid entry", handle_line
    continue
  handle = parts[0]
  page_name = parts[1]
  page_id = parts[2]
  handle_page_name[handle] = page_name
  handle_page_id[handle] = page_id
  write_to_facebook(handle, page_name, page_id)
