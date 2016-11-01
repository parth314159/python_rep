import requests
from bs4 import BeautifulSoup
from Queue import Queue
import urllib
import time
from FileHandling import FileHandling
import re

class spider:
    def __init__(self,url,maximumcount=1000):
        self.mainurl = url
        self.mcount = maximumcount
        self.depth = 5
        self.constraint=["index",":","Main_Page"]
        self.required = ["wiki"]
        self.base = "https://en.wikipedia.org"
        self.imgbase = "https://www.wikipedia.org/"
        self.imageout = "wiki/"

    def filter(self, url):
        if any(x in url for x in self.constraint):
            return ""
        elif (x in url for x in self.required):
            if url.startswith("/"):
                return self.base+url
            elif url.startswith("//en"):
                return "https:"+url
            elif url.startswith("http"):
                return url
            else:
                return ""
        else:
            return ""

    def imgfilter(self, url):
            if url.startswith("//"):
                return "http:"+url
            elif url.startswith("/"):
                return self.base+url
            elif url.startswith("http"):
                return url
            else:
                return ""

    def crawl(self):
        f = FileHandling("crawl_all_links.txt")
        q = Queue()
        count = 0
        depth = 0
        q.enqueue(self.mainurl)
        while not q.isEmpty():
            cURL = q.dequeue()
            time.sleep(1)
            source = requests.get(cURL)
            soup = BeautifulSoup(source.text,'html.parser')
            #print(cURL)
            count += 1
            for link in soup.findAll("a"):
                #print(link.get("href"))
                ln = link.get("href")
                if ln is not None:
                    full_url=self.filter(link.get("href"))
                    if full_url != "":
                        print(full_url)
                        f.log_msg(full_url)
                        q.enqueue(full_url)
                        count+=1
            depth+=1
            if depth >= self.depth or count >= self.mcount:
                break
        print("Number of URL crawled:",count,"Depth of crawled data:",depth)

    def crawl_word(self,word):
        f = FileHandling("crawl_"+word+".txt")
        q = Queue()
        count = 0
        depth = 0
        q.enqueue(self.mainurl)
        while not q.isEmpty():
            cURL = q.dequeue()
            #time.sleep(1)
            source = requests.get(cURL)
            soup = BeautifulSoup(source.text,'html.parser')
            if soup.find(text=re.compile(word, re.I)) is not None:
                print(cURL)
                f.log_msg(cURL)
                count+=1
            for link in soup.findAll("a"):
                #print(link.get("href"))
                ln = link.get("href")
                if ln is not None:
                    #print(ln)
                    full_url=self.filter(link.get("href"))
                    if full_url != "":
                        q.enqueue(full_url)
            if count > self.mcount:
                    break
        print("Number of URL crawled:",count,"Depth of crawled data:",depth)

    def crawl_images(self,number):
        #f = FileHandling("crawl_all_links.txt")
        q = Queue()
        count = 0
        q.enqueue(self.mainurl)
        while not q.isEmpty():
            cURL = q.dequeue()
            time.sleep(1)
            source = requests.get(cURL)
            soup = BeautifulSoup(source.text,'html.parser')
            #print(cURL)
            for im in soup.findAll("img"):
                im_ln = im.get("src")
                if im_ln is not None:
                    print(self.imgfilter(im_ln))
                    IMAGE = im_ln.rsplit('/',1)[1]
                    try:
                        urllib.request.urlretrieve(self.imgfilter(im_ln), self.imageout+IMAGE)
                        count+=1
                    except:
                        print("Invalid url...Ignoring")
            for link in soup.findAll("a"):
                #print(link.get("href"))
                ln = link.get("href")
                if ln is not None:
                    #print(ln)
                    full_url=self.filter(link.get("href"))
                    if full_url != "":
                        q.enqueue(full_url)
            if count > number:
                break
        print("Number of Images crawled:",count)


sp = spider("https://en.wikipedia.org/")
sp.crawl_word("batman")