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
upload_history_file = "../logs/dumping_saaku.txt"
log_file = "../logs/post_line.log"
upload_link_url = 'http://timesofindia.indiatimes.com/city/bengaluru/The-way-out-Dumping-saaku-segregation-beku/articleshow/44831867.cms'

upload_hash = {}
def dump_file():
  timestamp = datetime.datetime.now().time().isoformat()
  new_file = log_file + "_" + timestamp
  f = open(new_file, 'w')
  for k, v in upload_hash.iteritems():
    f.write(k + '\t' + v + '\n')
  f.close()
  return new_file

access_token = ""
try:
  with open('../input/access_token.txt') as f:
    lines = f.readlines()
    access_token = lines[0].strip()
except:
  print "Error geting access token"
  sys.exit()

try:
  # we need to provide a file name to keep track of link ids
  with open(upload_history_file) as f:
    lines = f.readlines()
    for line in lines:
      line = line.strip()
      parts = line.split('\t')
      if len(parts) != 2:
        print "Error reading upload history file"
        print line
        continue
      page_id = parts[0]
      link_id = parts[1]
      if page_id not in upload_hash:
        upload_hash[page_id] = link_id
  f.close()
except:
  print "File not found: %s" % (upload_history_file)
        
  
def write_to_facebook(handle, page_name, page_id, text, upload_link_url):
  global access_token
  graph = GraphAPI(access_token)
  #response = graph.get("/264547013954814/accounts")
  #pages = response['data']
  #print pages
  count = 0
  #for page in pages:
  #if (page_name != page['name']):
  #  continue
  #page_id = page['id']
  #if page_id in upload_hash:
    #continue
  response = graph.get("/" + page_id + "/?fields=access_token")
  page_access_token = response['access_token']
  #print page_name + '\t' + page_id + '\t' + page_access_token
  #if debug is True and page_name != 'LSPK Media Team':
  #    continue
  r = ''
  try:
    #print page_name + '\t' + page_id + '\t' + page_access_token
    print page_name
    print text
    print upload_link_url
    get_char = raw_input("Publish? ")
    if get_char == 'y' or get_char == 't':
        if get_char == 't':
            text = raw_input("New title: ")
            text = text.strip()
        print "posting to %s at url http://facebook.com/%s" % (page_name, page_id)
        path_string = "%s/feed" % page_id
        page_graph = GraphAPI(page_access_token)
        r = page_graph.post(path=path_string, link=upload_link_url, name=text)
        link_id = r['id'] 
        print 'Success: posted link with id: ' + link_id
        # write to a file as well
        tweet_file = "../output/" + handle + ".txt"
        tf = open(tweet_file, "a+")
        try:
            output = text + "~" + upload_link_url + "\n"
            tf.write(output)
            tf.close()
        except:
            print "Exception writing to file ", handle, ".txt"
            tf.close()
        count += 1
        sleep_interval = randint(1,3)
        time.sleep(sleep_interval)
        if (count > 200):
          return
    #upload_hash[page_id] = link_id
  except:
    print "Unexpected error:", sys.exc_info()
    sys.exit()
    #dump_file()

  #copyfile(upload_history_file, upload_history_file + ".bk")
  #new_file = dump_file()
  #copyfile(new_file, upload_history_file)

if len(sys.argv) < 3:
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
    write_to_facebook(handle, page_name, page_id, title, url)
    output = handle + "~" + title + "~" + url + "\n"
    f.write(output)
f.close()
