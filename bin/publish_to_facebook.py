#! /usr/bin/env python

from facepy import GraphAPI
import sys
#import urllib3
import urllib2
import datetime
import time
from random import randint
from shutil import copyfile


#urllib3.disable_warnings()

debug = True

access_token = ""
try:
  with open('../input/short_lived_access_token.txt') as f:
    lines = f.readlines()
    access_token = lines[0].strip()
except:
  try:
    with open('../input/access_token.txt') as f:
      lines = f.readlines()
      access_token = lines[0].strip()
  except:
    print "Error geting access token"
    sys.exit()

changed_handles = []

def load_liberal_agenda(handle):
    return_agenda = ""
    agenda_file = "../input/agenda/" + handle + ".txt"

    if '_liberals' not in handle:
        return ""

    try:
        tf = open(agenda_file, "a+")
    except:
        print "Error opening file for append", agenda_file
        return ""

    tf_lines = tf.readlines()
    tf.close()
    cf_lines = []
    try:
        # refresh liberal agenda file
        cf = open("../input/agenda/liberal_agenda.txt")
        cf_lines = cf.readlines()
    except:
        print "Error opening liberal agenda file"

    agenda_map = {}
    if len(cf_lines) > len(tf_lines):
        for line in cf_lines:
            agenda = line.strip()
            time_count = "0"
            agenda_map[agenda] = time_count

    agenda_list = [] # used to randomly pick

    for line in tf_lines:
        line = line.strip()
        parts = line.split("~")
        if len(parts) < 2:
            continue
        agenda = parts[0]
        time_count = parts[1]
        agenda_map[agenda] = time_count

    for k, v in agenda_map.items():
        if v == "0":
            agenda_list.append(k)

    # this is where we choose the return agenda
    return_agenda_index = randint(0,len(agenda_list)-1)
    return_agenda = agenda_list[return_agenda_index]
    if return_agenda_index >= len(agenda_map):
        print "agenda map corruption?"
        return ""
    agenda_map[return_agenda] = "1"

    # write updated file
    tf = open(agenda_file, "w")
    for k, v in agenda_map.items():
        output = k + "~" + v + "\n"
        tf.write(output)
    tf.close()

    return return_agenda

def write_to_facebook(handle, page_name, page_id):
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
    #print page_name + '\t' + page_id + '\t' + page_access_token
    tweet_file = "../output/temp/" + handle + ".txt"
    write_lines = []
    try:
        tf = open(tweet_file, "r")
        write_lines = tf.readlines()
        tf.close()
    except:
        #print "File not found?", tweet_file
        liberal_agenda = load_liberal_agenda(handle)
        parts = liberal_agenda.split("|")
        if len(parts) == 2:
            text = "#LiberalAgenda " + parts[1]
            upload_link_url = "http://indianliberals.org/" + parts[0] + ".html"
            liberal_agenda = text + "~" + upload_link_url
            write_lines.append(liberal_agenda)

    for line in write_lines:
        parts = line.split("~")
        if len(parts) < 2:
            continue
        text = parts[0]
        upload_link_url = parts[1]
    	print text
        print upload_link_url
        print "posting to %s at url http://facebook.com/%s" % (page_name, page_id)
        path_string = "%s/feed" % page_id
        page_graph = GraphAPI(page_access_token)
        r = page_graph.post(path=path_string, link=upload_link_url, message=text)
        link_id = r['id'] 
        print 'Posted http://facebook.com/' + link_id + ' to ' + page_name
        sleep_interval = randint(2,3)
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

