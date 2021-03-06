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

def write_to_facebook(handle, page_name, page_id):
  #if 'dn_liberals' not in handle:
  #   return
  global access_token
  graph = GraphAPI(access_token)
  response = graph.get("/" + page_id + "/?fields=access_token")
  page_access_token = response['access_token']
  tf = open("../input/page_access_tokens", "a+")
  output = page_name + "|" + page_id + "|" + page_access_token + "\n"
  tf.write(output)
  tf.close()
  r = ''
  try:
        upload_link_url = "http://indianliberals.org/share/" + handle
        text = "We invite you to share blog posts and news articles on our webpage. " + upload_link_url
        #upload_link_url = "http://indianliberals.org/" + handle.strip() + ".html"
        #text = "We've improved our campaign web page. Checkout! " + upload_link_url 
        #upload_link_url = "http://facebook.com/%s" % (page_id)
        #text = "You are welcome to post your views and links on our facebook page."
        #upload_link_url = "http://indianliberals.org/books.html"
        #text = "We want to recommend a book reading list for Liberals. Send us your suggestions!"

        #response = graph.get("/" + page_id + "/?fields=link")
        #page_link = response['link']
        #upload_link_url = page_link
        #text = "Our Facebook page: " + page_link

        #upload_link_url = "https://www.newsgram.com/swarna-bharat-party-looking-for-candidates-to-fight-2019-elections/"
        #text = "Want to contest elections? Swarna Bharat Party is looking for candidates to fight 2019 Lok Sabha Elections."
    	print text
        print upload_link_url
        print "posting to %s at url http://facebook.com/%s" % (page_name, page_id)
        path_string = "%s/feed" % page_id
        page_graph = GraphAPI(page_access_token)
        r = page_graph.post(path=path_string, link=upload_link_url, message=text)
        #else:
        #  r = page_graph.post(path=path_string, name=text)
        link_id = r['id'] 
        print 'Posted http://facebook.com/' + link_id + ' to ' + page_name
        sleep_interval = randint(8,12)
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
  if len(parts) != 4:
    print "Invalid entry", handle_line
    continue
  handle = parts[0]
  page_name = parts[1]
  page_id = parts[2]
  handle_page_name[handle] = page_name
  handle_page_id[handle] = page_id
  write_to_facebook(handle, page_name, page_id)

