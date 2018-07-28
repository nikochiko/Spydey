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
    if( not source):
        return []
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

    same_dir_pattern = "\./.*"

    prev_dir_pattern = "\.\.\/.*"

    email_pattern = "mailto\:.*"

    tel_pattern = "tel\:.*"

    next_dir_pattern = "\/.*"

    file_with_extension_pattern=".*\.{3,4}"

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
        if((r'/' not in each_url and file_with_extension.match(each_url)) and r'www.' not in each_url):
            res.append(base_url+each_url)
            continue
        if(((r'/' in each_url and r':' not in each_url)) and r'www.' not in each_url):
            res.append(base_url+each_url)
            continue
        else:
            res.append(each_url)
            continue
    return res
def subdir_splitter(refined_url_list, pre_list=None):
    http_pattern=r'http://.*'
    https_pattern=r'https://.*'
    http = re.compile(http_pattern)
    https = re.compile(https_pattern)
    res = []
    selected_res = []
    for each_url in refined_url_list:
        if(http.match(each_url)):
            refined_url = each_url[each_url.find(r'/',7):]
        elif(https.match(each_url)):
            refined_url = each_url[each_url.find(r'/',8):]
        else:
            refined_url = each_url
        temp_split = refined_url.split(r'/')
        temp_str = ""
        i = 0
        while(i < len(temp_split)):
            temp_str += r"/"+temp_split[i]
            if(temp_str not in res):
                res.append(temp_str)
            else:
                i+=1 
                continue
            i += 1
        del temp_str
        for url in res:
            if(pre_list):
                if(url not in pre_list):
                    selected_res.append(url)
            else:
                selected_res.append(url)
    return (list(set(pre_list+selected_res)) if pre_list else list(set(selected_res)))
def crawl_each_url(url, extract_func=extractLinks):
    pre_list = extract_func(getPage(url))
    refined_pre_list = url_picker(pre_list, url)
    return url_picker(subdir_splitter(refined_pre_list), url)
def crawl_engine(url, option=None):
    if( not (url[-1]==r'/')):
        url += r'/'
    if(option == "all"):
        pre_list=extract_all_links(url)
    else:
        pre_list = extractLinks(getPage(url))    
    refined_pre_list = url_picker(pre_list, url)
    to_crawl = url_picker(subdir_splitter(refined_pre_list), url)
    crawled = [url]
    while(to_crawl):
        temp_url = to_crawl.pop()
        if(temp_url not in crawled):
            if(option=="all"):
                temp_url_crawl=crawl_each_url(temp_url, extract_all_links)
            else:
                temp_url_crawl = crawl_each_url(temp_url)
            for each in temp_url_crawl:
                if(each not in crawled and each not in to_crawl):
                    to_crawl.append(each)
        crawled.append(temp_url)
    return crawled
def extract_all_links(source, pre_list=None):
    ls=[]
    if( not source):
        return []
    if(r"<" not in source):
        return []
    source_lowercase = source.lower()
    start_pos = 0
    lt_pos=0
    gt_pos=0
    while((lt_pos<len(source_lowercase) and gt_pos<len(source_lowercase)) and ((lt_pos>=0) and gt_pos>=0)):
        lt_pos=source_lowercase.find(r'<', gt_pos)
        gt_pos=source_lowercase.find(r'>', lt_pos)
        #THIS WILL EVEN CATCH SRC AND HREF LINKS IN COMMENTS!!!
        if(lt_pos>=0 and gt_pos >=0):
            src_pos=source_lowercase.find("src", lt_pos, gt_pos)
            src_start_pos=(source_lowercase.find(r'"', src_pos, gt_pos)+1) #AVOIDING SEARCHING FOR LINKS OUT OF <> IN SOURCE    
            src_end_pos=(source_lowercase.find(r'"', src_start_pos, gt_pos))
            if(src_end_pos > src_start_pos):
                temp=source[src_start_pos:src_end_pos]
            else:
                continue
            if(pre_list):
                if(temp not in ls and temp not in pre_list):
                    ls.append(temp)
            elif(temp not in ls):
                ls.append(temp)
            href_pos=source_lowercase.find(r'href',lt_pos, gt_pos)
            href_start_pos=(source_lowercase.find(r'"', href_pos, gt_pos)+1)
            href_end_pos=(source_lowercase.find(r'"', href_start_pos,gt_pos))
            if(href_end_pos > href_start_pos):
                temp=source[href_start_pos:href_end_pos]
            else:
                continue
        else:
            return []
        
        return ls
