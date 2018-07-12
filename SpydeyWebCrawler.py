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

    file_with_extension_pattern=".*\.{3-4}"

    same_dir = re.compile(same_dir_pattern)

    prev_dir = re.compile(prev_dir_pattern)

    email = re.compile(email_pattern)

    tel = re.compile(tel_pattern)

    next_dir = re.compile(next_dir_pattern)

    file_with_extension = re.compile(file_with_extension_pattern)

    base_split = base_url.split(r'/')

    for each_url in url_list:

        if(same_dir.match(each_url)):

            if(file_with_extension.match(base_url)):

                res.append(r"/".join(base_split[:len(base_split)-1]) + each_url[2:])  

            else:

                res.append(base_url+each_url[2:])

            continue

        if(prev_dir.match(each_url)):

            if(file_with_extension.match(base_url)):

                res.append(r"/".join(base_split[:len(base_split)-2]) + each_url[3:])

            else:

                res.append(r'/'.join(base_split[:len(base_split)-1])+each_url[3:])
            continue
        if(email.match(each_url) or tel.match(each_url)):
            continue
        if(next_dir.match(each_url)):
            if(file_with_extension.match(base_url)):
                res.append(r"/".join(base_split)[:len(base_split)-1] + each_url[1:])
            else:
                res.append(base_url+each_url[1:])
            continue
        if(r'/' not in each_url and file_with_extension.match(each_url)):
            res.append(base_url+each_url)
            continue
        if((r'/' in each_url and r':' not in each_url)):
            res.append(base_url+each_url)
            continue
        else:
            res.append(each_url)
            continue
    return res
###INCOMPLETE###
