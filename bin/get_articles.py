import feedparser
import sys

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


output_file = sys.argv[3]
f = open(output_file, 'w')
for url_line in url_lines:
  url_line = url_line.strip()
  parts = url_line.split("|")
  keyword = parts[0]
  url = parts[1]
  d = feedparser.parse(url)
  for post in d.entries:
    post_link = post.link.split("=")[-1]
    if post.title in log_title.keys():
      print post.title, "already present in log. Ignored."
      continue
    if post_link in log_url.keys():
      print post_link, "already present in log. Ignored."
      continue
    #print post.title + ": " + post_link
    output = keyword + "~" + post.title + "~" + post_link + "\n"
    f.write(output.encode('utf8'))

f.close()
