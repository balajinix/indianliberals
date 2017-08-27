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

has_twitter = ['indian_liberals']
has_list = ['indian_liberals']

handle_page_name = {}
handle_page_id= {}
handle_category_id= {}
for handle_line in handle_lines:
  handle_line = handle_line.strip()
  parts = handle_line.split("|")
  if len(parts) != 4:
    print "Invalid entry", handle_line
    continue
  handle = parts[0]
  page_name = parts[1]
  page_id = parts[2]
  category_id = parts[2]
  handle_page_name[handle] = page_name
  handle_page_id[handle] = page_id
  handle_category_id[handle] = category_id


# now we are reading the file
#files = [f for f in listdir(dirpath + "/text/") if isfile(join(dirpath + "/text/", f))]

for k,v in handle_page_name.iteritems():
#for filename in files:
    filename = k + ".txt"
    print filename
    page_str = "<html><br/>\n"
    page_str += "<body>\n"
    page_str += "<div id=\"fb-root\"></div>\n"
    page_str += "<script>(function(d, s, id) {\n"
    page_str += "  var js, fjs = d.getElementsByTagName(s)[0];\n"
    page_str += "  if (d.getElementById(id)) return;\n"
    page_str += "  js = d.createElement(s); js.id = id;\n"
    page_str += "  js.src = \"//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.9&appId=291986894191024\";\n"
    page_str += "  fjs.parentNode.insertBefore(js, fjs);\n"
    page_str += "}(document, 'script', 'facebook-jssdk'));</script>\n"
    page_str += "<script>window.twttr = (function(d, s, id) {"
    page_str += "  var js, fjs = d.getElementsByTagName(s)[0],"
    page_str += "    t = window.twttr || {};"
    page_str += "  if (d.getElementById(id)) return t;"
    page_str += "  js = d.createElement(s);"
    page_str += "  js.id = id;"
    page_str += "  js.src = \"https://platform.twitter.com/widgets.js\";"
    page_str += "  fjs.parentNode.insertBefore(js, fjs);"
    page_str += ""
    page_str += "  t._e = [];"
    page_str += "  t.ready = function(f) {"
    page_str += "    t._e.push(f);"
    page_str += "  };"
    page_str += ""
    page_str += "  return t;"
    page_str += "}(document, \"script\", \"twitter-wjs\"));</script>"
    page_str += "<table>\n"
    page_str += "<tr>"
    page_str += "<td align=\"center\" valign=\"top\">"
    if k != "indian_liberals":
        page_str += "<a href=\"" + "http://indianliberals.org" + "\">" + "Indian Liberals" + "</a><br/>\n"
        page_str += "<br/>\n"
    page_str += "<img src=\"https://liberalsin.files.wordpress.com/2016/05/liberals_logo.jpg\"></img><br/>\n"
    page_str += "<br/>\n"
    page_str += "<a href=\"" + "https://en.wikipedia.org/wiki/Swatantra_Party" + "\">" + "Swatantra Party Flag" + "</a><br/>\n"
    page_str += "<br/>\n"
    # table for campaigns start
    page_str += "<table>"
    page_str += "<tr><td align=\"left\" valign=\"top\">"
    page_str += "<br/>\n"
    page_str += "Our Campaigns:<br/><br/>\n"
    page_str += "</td></tr>"
    for k in sorted(handle_page_name):
        v = handle_page_name[k]
        #r = randint(2, 5)
        #if r > 3:
        #    continue
        page_str += "<tr><td align=\"left\">"
        page_str += "<a href=\"" + "http://indianliberals.org/" + k + ".html" + "\">" + v + "</a><br/>\n"
        page_str += "</td></tr>"
    page_str += "</td></tr>"
    page_str += "</table>"
    # table for campaigns end
    page_str += "</td>"
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
            parts = line.split("~")
            if len(parts) < 2:
                continue
            agenda = parts[0]
            parts = agenda.split("|")
            if len(parts) < 2:
                continue
            agenda_text += parts[1]
            agenda_text += "<br/>"

    handle = filename.replace('.txt','')
    page_name = handle_page_name[handle]
    page_id = handle_page_id[handle]

    # output file
    output_file_name = filename.replace('.txt', '.html')
    output_file_name = join(dirpath + "/html/", output_file_name)
    ofp = open(output_file_name,'w')

    # header
    # table for agenda etc begins
    page_str += "<table>\n"
    page_str += "<tr>\n"
    page_str += "<td>\n"
    page_str += "<h2>" + page_name + "</h2>\n"
    if len(base_text) > 0:
    	page_str += base_text
    if len(agenda_text) > 0:
    	page_str += "<h3>Liberal Agenda:</h3>\n"
    	page_str += agenda_text

    # if news articles exist, write them
    lines = []
    if isfile(join(dirpath + "/text/", filename)):
        fp = open(join(dirpath + "/text/",filename),'r')
        lines = fp.readlines()
        fp.close()
    if len(lines) > 0:
        page_str += "<h3>" + "Campaign news shared from <a href=\"http://www.indianliberals.org/share/" + handle + "\">http://www.indianliberals.org/share/" + handle + "</a>\n"
        page_str += "<br/>"
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
    # table for agenda etc ends
    page_str += "<br/>"
    page_str += "<br/>"
    page_str += "Follow us:<br/>\n"
    page_str += "<br/>\n"
    page_str += "Facebook Page: <a href=\"" + "http://facebook.com/" + page_id + "\">" + page_name + "</a><br/>\n"
    page_str += "Twitter: <a href=\"" + "http://twitter.com/" + handle  + "\">@" + handle + "</a><br/>\n "
    page_str += "URL: <a href=\"http://www.indianliberals.org/" + handle + ".html\">http://www.indianliberals.org/" + handle + "</a><br/>\n"
    page_str += "<br/>\n"
    page_str += "Contribute:<br/>\n"
    page_str += "<br/>\n"
    page_str += "Share news: <a href=\"http://www.indianliberals.org/share/" + handle + "\">http://www.indianliberals.org/share/" + handle + "</a><br/>\n"
    page_str += "Write on our blog: <a href=\"https://liberalsin.wordpress.com\">https://liberalsin.wordpress.com</a><br/>\n"
    page_str += "Join our group: <a href=\"https://www.facebook.com/groups/indianliberals.org\">https://www.facebook.com/groups/indianliberals.org</a><br/>\n"
    page_str += "Send a suggestion: liberals dot in at gmail.com<br/>\n"
    page_str += "<br/>"

    # search box
    page_str += "<br/>"
    page_str += "<br/>"
    page_str += "<script>"
    page_str += "  (function() {"
    page_str += "    var cx = '014907431480918052286:baul13jjegq';"
    page_str += "    var gcse = document.createElement('script');"
    page_str += "    gcse.type = 'text/javascript';"
    page_str += "    gcse.async = true;"
    page_str += "    gcse.src = 'https://cse.google.com/cse.js?cx=' + cx;"
    page_str += "    var s = document.getElementsByTagName('script')[0];"
    page_str += "    s.parentNode.insertBefore(gcse, s);"
    page_str += "  })();"
    page_str += "</script>"
    page_str += "<gcse:searchbox-only></gcse:searchbox-only>"
    page_str += "<hr/>"

    page_str += "</td>"
    page_str += "</tr>"
    page_str += "</table>\n"

    page_str += "</td>\n"
    page_str += "<td>\n"
    page_str += "</td>\n"
    page_str += "</tr>\n"
    page_str += "</table>\n"

    page_str += "<table width=\"100%\">\n"
    page_str += "<tr>\n"
    page_str += "<td valign=\"top\">\n"
    page_str += "<div style=\"width:390px;\">\n"
    page_str += "  <div class=\"fb-page\" data-href=\"https://www.facebook.com/" + page_id + "\" data-width=\"390\" data-height=\"2800\" data-tabs=\"timeline\"></div>\n"
    page_str += "</div>\n"
    page_str += "</td>\n"
    page_str += "<td valign=\"top\" width=\"32%\">\n"
    display_handle = "indian_liberals"
    display_page_name = "Indian Liberals"
    if handle in has_twitter:
        display_handle = handle
        display_page_name = page_name
    page_str += "<a class=\"twitter-timeline\" data-width=\"390\" data-height=\"2100\" href=\"https://twitter.com/" + display_handle + "\">Tweets by " + display_page_name + "</a> <script async src=\"//platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>\n"
    page_str += "</td>\n"
    page_str += "<td valign=\"top\" width=\"32%\">\n"
    display_handle = "indian_liberals"
    if handle in has_list:
        display_handle = handle
    page_str += "<a class=\"twitter-timeline\" data-width=\"390\" data-height=\"2100\" href=\"https://twitter.com/" + display_handle + "/lists/liberals\">Tweets by Liberals" + "</a> <script async src=\"//platform.twitter.com/widgets.js\" charset=\"utf-8\"></script>\n"
    page_str += "<script>\n"
    page_str += "twttr.widgets.createTimeline("
    page_str += "  {"
    page_str += "    sourceType: \"list\","
    page_str += "    ownerScreenName: \"indian_liberals\","
    page_str += "    slug: \"liberals\""
    page_str += "  },"
    page_str += "  document.getElementById(\"container\")"
    page_str += ");"
    page_str += "</script>\n"
    page_str += "</td>\n"
    page_str += "</tr>\n"
    page_str += "</table>\n"
    page_str += "<br/>"

    page_str += "<script>\n"
    page_str += "  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){\n"
    page_str += "  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\n"
    page_str += "  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\n"
    page_str += "  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');\n"
    page_str += "  ga('create', 'UA-70497326-2', 'auto');\n"
    page_str += "  ga('send', 'pageview');\n"
    page_str += "</script>\n"
    page_str += "</body>\n"
    page_str += "</html>\n"

    ofp.write(page_str)
    ofp.close()
