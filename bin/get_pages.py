#! /usr/bin/env python

from facepy import GraphAPI

access_token = ""
try:
  with open('../input/access_token.txt') as f:
    lines = f.readlines()
    access_token = lines[0].strip()
except:
  print "Error geting access token"
  sys.exit()

graph = GraphAPI(access_token)
response = graph.get("/264547013954814/accounts")
pages = response['data']
count = 0
for page in pages:
  page_name = page['name']
  page_id = page['id']
  output = page_name + "|" + page_id
  print output
