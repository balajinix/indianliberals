#! /usr/bin/env python

# Author - Balaji Ganesan
# Email - balajinix@gmail.com

import twitter

import datetime
import time
from shutil import copyfile
import sys
import time
from random import randint

def search_and_publish(handle, search_term, f, api):
    output_map = {}
    search = api.GetSearch(term=search_term, lang='en', result_type='recent', count=200, max_id='')
    append_url = " http://indianliberals.org"
    append_handle = " @joinLiberals"
    for t in search:
      #print t.user.screen_name + ' (' + t.created_at + ')'
      screen_name = t.user.screen_name
      tweet = t.text.encode('utf-8')
      if "RT @" in tweet:
          continue
      follower_count = int(t.user.followers_count)
      if follower_count < 2000:
          continue
      try:
          retweet = t["retweeted_status"]
          continue
      except:
          retweet = ""
      try:
          reply = t["in_reply_to_screen_name"]
          continue
      except:
          retweet = ""
      try:
          default_profile = t.user.default_profile
          if default_profile:
              continue
      except:
          default_profile = False
    
      #try:
      #   retweet_count = t["retweet_count"]
      #except:
          #continue
      tweet_url = "https://twitter.com/" + screen_name + "/status/" + t.id_str
      if tweet not in output_map:
          tweet = tweet.strip()
          tweet = tweet.replace("\n", " ")
          output_map[tweet] = handle
          try:
              f.write(handle + "~" + "RT @" + screen_name + " " + tweet + "~" + tweet_url + "\n")
          except:
              continue
      continue
    
      if screen_name in upload_hash:
        #print "Already tweeted to", screen_name, " with message ", upload_hash[screen_name]
        continue
    
      #Add the .encode to force encoding
      tweet = t.text.encode('utf-8')
    
      # lets see if there is any category
      tweet_category = ''
      for k, v in categories.iteritems():
        if k in tweet.lower():
          #tweet_category += v + '|'
          tweet_category = v
      if len(tweet_category) < 1:
        if debug is True:
          print "No tweet category for: ", tweet
        continue
    
      if tweet_category in messages:
        base_response = "@" + t.user.screen_name + " " + messages[tweet_category]
        response = base_response
        #if len(response) + len(append_url) < 140:
        response += append_url
        #if len(response) + len(append_handle) < 140:
        response += append_handle
        try:
          mention = "Tweet: @" + screen_name + " says: " + tweet
          print mention
          print "Category: ", tweet_category
          print "Response: ", response, "\n"
          if debug is False:
            status = api.PostUpdate(response)
        except Exception, e:
          short_response = base_response + append_handle
          try:
            print "Retry Response: ", short_response, len(response), len(short_response), "\n"
            if debug is False:
              status = api.PostUpdate(short_response)
          except Exception, e:
            "[Error] Could not tweet response %s" %(short_response)
        if debug is False:
          upload_hash[screen_name] = messages[tweet_category]
          sleep_interval = randint(5, 25)
          time.sleep(sleep_interval)

# main program starts here
if len(sys.argv) < 4:
  sys.exit()

url_file = sys.argv[1]
f = open(url_file,'r')
url_lines = f.readlines()
f.close()

log_file = sys.argv[2]
f = open(log_file, 'r')
log_lines = f.readlines()
f.close()

log_url = {}
log_title = {}
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

query_map = {}
for url_line in url_lines:
  url_line = url_line.strip()
  parts = url_line.split("|")
  handle = parts[0]
  keyword = parts[1]
  query_map[keyword] = handle

# make sure you run the script with debug set to True first
debug = False

categories = {
              #'footpath' : 'footpath',
             }

messages = {
             #'footpath' : 'some message'
           }

# we need to have proper credentials
consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''
try:
  with open('../input/twitter_access_token.txt') as f:
    lines = f.readlines()
    if len(lines) != 4:
      print "access_token file should have four lines. lines_count: ", len(lines)
      sys.exit()
    consumer_key = lines[0].strip().split('\t')[1]
    consumer_secret = lines[1].strip().split('\t')[1]
    access_token_key = lines[2].strip().split('\t')[1]
    access_token_secret = lines[3].strip().split('\t')[1]
except:
  print "Error geting access token"
  sys.exit()

output_file = sys.argv[3]
f = open(output_file, 'w')
# initialize the module
api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
for keyword, handle in query_map.items():
    search_and_publish(handle, keyword, f, api)
    sleep_interval = randint(2, 5)
    time.sleep(sleep_interval)
f.close() 
