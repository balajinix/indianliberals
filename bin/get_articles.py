import feedparser
# Author - Balaji Ganesan
# Email - balajinix@gmail.com
import sys
import codecs

def is_ascii(text):
    if isinstance(text, unicode):
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

if len(sys.argv) < 4:
  sys.exit()

# this is the google news urls to get articles from
url_file = sys.argv[1]
f = codecs.open(url_file, 'r', 'utf-8')
url_lines = f.readlines()
f.close()

# this file has the history of urls already considerd.
log_file = sys.argv[2]
f = codecs.open(log_file, 'r', 'utf-8')
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

log_file = sys.argv[2]
lf = codecs.open(log_file, 'a+', 'utf-8')

output_file = sys.argv[3]
f = codecs.open(output_file, 'w', 'utf-8')
for url_line in url_lines:
  url_line = url_line.strip()
  parts = url_line.split("|")
  keyword = parts[0]
  url = parts[1]
  d = feedparser.parse(url)
  for post in d.entries:
    if not is_ascii(post.title):
      continue
    if post.title in log_title.keys():
      #print post.title, "already present in log. Ignored."
      continue
    post_link = post.link.split("=")[-1]
    if post_link in log_url.keys():
      #print post_link, "already present in log. Ignored."
      continue
    #print post.title + ": " + post_link
    log_title[post.title] = 1
    log_url[post_link] = 1
    output = keyword + "~" + post.title + "~" + post_link + "\n"
    # log file is the set of all urls we have seen. we should never process the same url again
    lf.write(output.encode('utf8'))
    f.write(output.encode('utf8'))

lf.close()
f.close()
