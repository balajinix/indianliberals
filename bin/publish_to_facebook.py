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

access_token = ""
try:
  with open('../input/access_token.txt') as f:
    lines = f.readlines()
    access_token = lines[0].strip()
except:
  print "Error geting access token"
  sys.exit()

changed_handles = []

def write_to_facebook(handle, page_name, page_id):
  global access_token
  graph = GraphAPI(access_token)
  response = graph.get("/" + page_id + "/?fields=access_token")
  page_access_token = response['access_token']
  r = ''
  try:
    #print page_name + '\t' + page_id + '\t' + page_access_token
    tweet_file = "../output/temp/" + handle + ".txt"
    try:
        tf = open(tweet_file, "r")
    except:
        print "File not found?", tweet_file
        return
    write_lines = tf.readlines()
    tf.close()
    for line in write_lines:
        parts = line.split("~")
        if len(parts) < 2:
            continue
        text = parts[0]
        upload_link_url = parts[1]
    	print page_name
    	print text
    	print upload_link_url
        print "posting to %s at url http://facebook.com/%s" % (page_name, page_id)
        path_string = "%s/feed" % page_id
        page_graph = GraphAPI(page_access_token)
        r = page_graph.post(path=path_string, link=upload_link_url, name=text)
        link_id = r['id'] 
        print 'Success: posted link with id: ' + link_id
        sleep_interval = randint(5,30)
        time.sleep(sleep_interval)
  except:
    print "Unexpected error:", sys.exc_info()
    return

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
  if len(parts) != 3:
    print "Invalid entry", handle_line
    continue
  handle = parts[0]
  page_name = parts[1]
  page_id = parts[2]
  handle_page_name[handle] = page_name
  handle_page_id[handle] = page_id
  write_to_facebook(handle, page_name, page_id)

