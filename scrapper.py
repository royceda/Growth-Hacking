from goose import Goose
from goose.utils import FileHelper
from goose.parsers import Parser
from goose.parsers import ParserSoup

import os
from os import listdir
from os.path import isfile, join

# Create csv file

f = open('result.csv', 'w')
f.write('name,description,contact name,contact role,site\n')
f.close()


data        = ''
parser      = Parser
url         = 'https://betalist.com'
url_exemple = url+'/startups/use-together'
url_list    = url+'/regions/france'
cmd         = "wget "+url_list

# get list page
print "wget : site : "+url_list
os.system(cmd);

# All startups
with open('startups.html', 'r') as myfile:
    data = myfile.read().replace('\n', '')

doc = parser.fromstring(data)
items_result = parser.css_select(doc, "*[class=startupCard__details__name]");

# get pages of startup
for item in items_result:
    print item.text
    print "site : "+url+item.get("href")
    cmd = "cd ./startups; wget "+url+item.get("href")
    os.system(cmd)


# all filename of saved file
path = "./startups"
files = [f for f in listdir(path) if isfile(join(path, f))]
print files


# get data from every startup
for i in range(0, len(files)):
    data = ''
    line = ''
    with open("./startups/"+files[i], 'r') as myfile:
        data = myfile.read().replace('\n', '')

    doc = parser.fromstring(data)
    # Name
    items_result = parser.css_select(doc, "*[class=startup__summary__name]");
    if len(items_result):
        print "Name : ", items_result[0].text
        line += items_result[0].text+','
    # Description
    items_result = parser.css_select(doc, "*[class=startup__summary__pitch]");
    if len(items_result):
        print "Description : ", items_result[0].text
        line += items_result[0].text+','

    p = parser.getElementsByTag(doc, tag='title')
    # print "Description1 : ", p[0].text
    # print dir(parser)
    # Contact
    items_result = parser.css_select(doc, "*[class=maker__name]");
    if len(items_result):
        print "Contact : ", items_result[0].text
        line += items_result[0].text+','
    # Role
    items_result = parser.css_select(doc, "*[class=maker__role]");
    if len(items_result):
        print "Role : ", items_result[0].text+'\n'
        line += items_result[0].text+'\n'

    # Site
    import string
    printable = set(string.printable)
    print filter(lambda x: x in printable, line)


    f = open('result.csv', 'a')
    f.write(filter(lambda x: x in printable, line))
    f.close()
