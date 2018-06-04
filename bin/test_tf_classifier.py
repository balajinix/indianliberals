#! /usr/bin/env python

import sys
import urllib3
import datetime
import time
from random import randint
from shutil import copyfile
import feedparser
import pickle
from tld import get_tld


urllib3.disable_warnings()

debug = True

import pymysql
import nltk
import tflearn
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import json

from facepy import GraphAPI
import sys
import datetime
import time
from random import randint
from shutil import copyfile


#urllib3.disable_warnings()

debug = True

access_token = ""
short_lived_access_token = ""
try:
  with open('../input/short_lived_access_token.txt') as f:
    lines = f.readlines()
    short_lived_access_token = lines[0].strip()
except:
    print("Error geting access token")

try:
  with open('../input/access_token.txt') as f:
    lines = f.readlines()
    access_token = lines[0].strip()
except:
  print("Error geting access token")
  sys.exit()

def write_to_facebook(handle, page_name, page_id, text, upload_link_url):
  if 'indian_liberals' == handle:
    return
  global access_token
  global short_lived_access_token
  page_access_token = ""
  try:
    graph = GraphAPI(short_lived_access_token)
    response = graph.get("/" + page_id + "/?fields=access_token")
    page_access_token = response['access_token']
  except:
    try:
      graph = GraphAPI(access_token)
      response = graph.get("/" + page_id + "/?fields=access_token")
      page_access_token = response['access_token']
    except:
      return
  tf = open("../input/page_access_tokens", "a+")
  output = page_name + "|" + page_id + "|" + page_access_token + "\n"
  tf.write(output)
  tf.close()
  r = ''
  try:
    print("posting to " + page_name + " at url http://facebook.com/" + page_id)
    path_string = "%s/feed" % page_id
    page_graph = GraphAPI(page_access_token)
    r = page_graph.post(path=path_string, link=upload_link_url, message=text)
    link_id = r['id'] 
    print('Posted http://facebook.com/' + link_id + ' to ' + page_name)
    sleep_interval = randint(40,60)
    time.sleep(sleep_interval)
  except:
    print("Unexpected error:" + sys.exc_info())
    return

log_url = {}
log_title = {}
words = []
#synapse_file = "../data/synapses.json"
#with open(synapse_file) as f:
#    synapse = json.load(f)
#    words = np.asarray(synapse['words'])
#    classes = np.asarray(synapse['classes'])
#print("test")
#print(len(words))

training_data = pickle.load(open( "../data/training_data", "rb" ) )
words = training_data['words']
classes = training_data['classes']
#print(len(words))

net = tflearn.input_data(shape=[None, len(words)])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 2, activation='softmax')
net = tflearn.regression(net)
model = tflearn.DNN(net, tensorboard_dir='../logs/tflearn_logs')
# load our saved model
model.load('../data/model.tflearn')

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

ERROR_THRESHOLD = 0.25
def classify(sentence):

    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

#output = classify('Kamal Nath could be Congress CM face in MP with Digvijaya Singh backing - ThePrint')
#print(output)

db = None
cursor = None

keywords_map = {}

def is_ascii(text):
    if isinstance(text, str):
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
      db = pymysql.connect(host=hostname,user=username,passwd=password,db=database)
  except:
    print("Error geting access token")
    sys.exit()
  
  # prepare a cursor object using cursor() method
  cursor = db.cursor()

  cursor.execute("select link_url, link_title, link_title_url, link_category, link_author, link_tags, link_id, link_votes from kliqqi_links where link_status='new'")
 
  results = cursor.fetchall()
  for result in results:
    link_url = result[0]
    link_title = result[1]
    link_title_url = result[2]
    link_category = result[3]
    link_author = result[4]
    link_tags = result[5]
    link_id = result[6]
    link_votes = result[7]

    if not is_ascii(link_title):
      cursor.execute("update kliqqi_links set link_status='discard' where link_id=" + str(link_id))
      cursor.execute("update kliqqi_links set link_published_date = link_modified where link_id=" + str(link_id))
      db.commit()
      continue

    tld = get_tld(link_url)
    last_d = tld.split('.')[-1]
    if last_d != 'com' and last_d != 'in':
      cursor.execute("update kliqqi_links set link_status='discard' where link_id=" + str(link_id))
      cursor.execute("update kliqqi_links set link_published_date = link_modified where link_id=" + str(link_id))
      db.commit()
      continue
    flag = True
    #if link_tags in keywords_map.keys():
    #  keywords = keywords_map[link_tags]
    #  for keyword in keywords:
    #    parts = keyword.split('+')
    #    title = link_title.lower()
    #    for part in parts:
    #      if part not in title:
    #        flag = False
    #        break
    # custom
    title = link_title.lower()
    if title in log_title.keys() or link_url in log_url.keys():
      cursor.execute("update kliqqi_links set link_status='discard' where link_id=" + str(link_id))
      cursor.execute("update kliqqi_links set link_published_date = link_modified where link_id=" + str(link_id))
      db.commit()
      continue
    else:
      log_title[title] = link_votes
      log_url[link_url] = link_votes
      if link_votes == 0 or link_votes == 2:
        continue
    if 'siddaramaiah' in title:
      if 'bjp' in title or 'yeddyurappa' in title or 'gowda' in title or 'kumaraswamy' in title:
        flag = False
    if 'chidambaram' in title:
      if 'karti' in title:
        flag = False
    if 'kashmir' in title:
      if 'army' in title or 'kill' in title or 'snow' in title or 'temperature' in title:
        flag = False
    if 'kill' in title:
      flag = False
    if flag == False:
      cursor.execute("update kliqqi_links set link_votes=0 where link_id=" + str(link_id))
      cursor.execute("update kliqqi_links set link_published_date = link_modified where link_id=" + str(link_id))
      db.commit()
      continue
    if flag == True:
      print(link_title)
      output = classify(link_title)
      print(output)
      if len(output) < 1:
        continue
      if len(output) == 1:
        output_tuple = output[0]
        if 'discard' in output_tuple:
          cursor.execute("update kliqqi_links set link_votes=0 where link_id=" + str(link_id))
          cursor.execute("update kliqqi_links set link_published_date = link_modified where link_id=" + str(link_id))
          db.commit()
          continue
      print("published\n")
      cursor.execute("update kliqqi_links set link_votes=2 where link_id=" + str(link_id))
      cursor.execute("update kliqqi_links set link_published_date = link_modified where link_id=" + str(link_id))
      db.commit()
      write_to_facebook(link_tags, 'Liberal news', '170857546946396', link_title, link_url)

if len(sys.argv) < 4:
  sys.exit()

handle_file = sys.argv[3]
f = open(handle_file, 'r')
handle_lines = f.readlines()
f.close()

keywords_file = sys.argv[5]
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

db_config_file = sys.argv[4]
read_articles(db_config_file)
db.close()
