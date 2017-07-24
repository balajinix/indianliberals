from os import listdir
from os.path import isfile, join
import sys
from random import randint

dirpath = sys.argv[1]
handle_file = sys.argv[2]
base_text_dirpath = sys.argv[3]
agenda_text_dirpath = sys.argv[4]

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


# now we are reading the file
files = [f for f in listdir(dirpath + "/text/") if isfile(join(dirpath + "/text/", f))]

for filename in files:
    print filename
    page_str = "<html><br/>\n"
    page_str += "<body>\n"
    page_str += "<table>\n"
    page_str += "<tr>"
    page_str += "<td align=\"center\" valign=\"top\">"
    page_str += "<img src=\"https://liberalsin.files.wordpress.com/2016/05/liberals_logo.jpg\"></img><br/>\n"
    page_str += "<a href=\"" + "http://indianliberals.org" + "\">" + "Indian Liberals" + "</a><br/>\n"
    page_str += "<table>"
    page_str += "<tr><td align=\"left\" valign=\"top\">"
    page_str += "Our Campaigns:<br/>\n"
    page_str += "</td></tr>"
    for k,v in handle_page_name.iteritems():
        r = randint(2, 5)
        if r > 3:
            continue
        page_str += "<tr><td align=\"left\">"
        page_str += "<a href=\"" + "http://indianliberals.org/" + k + ".html" + "\">" + v + "</a><br/>\n"
        page_str += "</td></tr>"
    page_str += "</td></tr>"
    page_str += "</table>"
    page_str += "</td><td></td>"
    page_str += "<td valign=\"top\">"

    base_text = ""
    if isfile(join(base_text_dirpath, filename)):
        bfp = open(join(base_text_dirpath,filename),'r')
        base_text_lines = bfp.readlines()
        bfp.close()
        for line in base_text_lines:
            base_text += line
            base_text += "<br/>"

    agenda_text = ""
    if isfile(join(agenda_text_dirpath, filename)):
        afp = open(join(agenda_text_dirpath,filename),'r')
        agenda_lines = afp.readlines()
        afp.close()
        for line in agenda_lines:
            agenda_text += line
            agenda_text += "<br/>"

    fp = open(join(dirpath + "/text/",filename),'r')
    handle = filename.replace('.txt','')
    page_name = handle_page_name[handle]
    page_id = handle_page_id[handle]

    # output file
    output_file_name = filename.replace('.txt', '.html')
    output_file_name = join(dirpath + "/html/", output_file_name)
    ofp = open(output_file_name,'w')

    # header
    page_str += "<table>\n"
    page_str += "<tr>\n"
    page_str += "<td>\n"
    page_str += "<h2>" + page_name + "</h2>\n"
    if len(base_text) > 0:
    	page_str += base_text
    if len(agenda_text) > 0:
    	page_str += "<h3>Liberal Agenda:</h3>\n"
    	page_str += agenda_text
    page_str += "<h3>" + "News relevant to this Campaign:" + "</h3>\n"

    lines = fp.readlines()
    fp.close()
    i = 0
    for line in reversed(lines):
        i += 1
        if i > 9:
            break
        line = line.strip()
        parts = line.split('~')
        page_str += "<tr>\n"
        page_str += "<td>\n"
        page_str += "<a href=\"" + parts[1] + "\">" + parts[0] + "</a><br/>\n"
        page_str += "</td>\n"
        page_str += "</tr>\n"
    page_str += "</table>\n"
    page_str += "<br/>"
    page_str += "Follow us: "
    page_str += "Twitter: <a href=\"" + "http://twitter.com/" + handle  + "\">@" + handle + "</a> "
    page_str += "Facebook Page: <a href=\"" + "http://facebook.com/" + page_id + "\">" + page_name + "</a><br/>\n"
    page_str += "</td>"
    page_str += "</tr>"
    page_str += "</table>\n"
    page_str += "</body>\n"
    page_str += "</html>\n"
    ofp.write(page_str)
    ofp.close()
