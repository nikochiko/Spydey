
import urllib2
import re

#Defining a method to return source code of wanted page
def getPage(url):
    try:
        req = urllib2.urlopen(url)
    except:
        return None
    return req.read()


#Extracting links from a single page
def extractLinks(source, pre_list=None):
    #Taking a lowercase copy to find index of links and then taking the links from real source.
    source_lowercase = source.lower()
    if(r'<a ' not in source_lowercase):
        return []
    ls = []
    start_pos = 0
    while(start_pos >= 0 and start_pos < len(source_lowercase)):   
        start_pos = source_lowercase.find(r'<a ', start_pos)
        start_pos = source_lowercase.find(r'href', start_pos)
        start_pos = (source_lowercase.find(r'"', start_pos) + 1)
        end_pos = source_lowercase.find(r'"', start_pos)
        temp = source[start_pos:end_pos]
        if(pre_list):
            if(temp not in ls and temp not in pre_list):
                ls.append(temp)
        elif(temp not in ls):
            ls.append(temp)
        start_pos = source_lowercase.find(r'<a ', start_pos)
    return ls
def url_picker(url_list, base_url):
    res = []
    same_dir_pattern = "\.\/.*"
    prev_dir_pattern = "\.\.\/.*"
    email_pattern = "mailto\:.*"
    tel_pattern = "tel\:.*"
    next_dir_pattern = "\/.*"
    file_with_extension_pattern=".*\..*"
    same_dir = re.compile(same_dir_pattern)
    prev_dir = re.compile(prev_dir_pattern)
    email = re.compile(email_pattern)
    tel = re.compile(tel_pattern)
    next_dir = re.compile(next_dir_pattern)
    file_with_extension = re.compile(file_with_extension_pattern)
    for each_url in url_list:
        if(same_dir.match(each_url)):
            if(file_with_extension.match(base_url)):
                base_split = base_url.split(r'/')
                res.append("\/".join(base_split[:len(base_split)-1]) + each_url[2:])
            else:
                res.append(base_url+each_url[2:])
    ###INCOMPLETE###