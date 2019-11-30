import re
import requests
import os
import lxml
from bs4 import BeautifulSoup
import urllib
import urllib3
import threading
import socket
import socks
import concurrent
from concurrent.futures import ThreadPoolExecutor
import time


def gethtml(url):
    try:
        headers = {
            'Referer': 'http://www.manhuadb.com/manhua/1051',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
            'Host': 'www.manhuadb.com',
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r
    except:
        return None


def download(pageurl, path):
    html = None
    while(html == None): html = gethtml(pageurl)
    html = html.text
    jpgurl = re.findall(r'<img class="img-fluid show-pic" src="(.*?)" />', html)[0]
    print('Downloading',jpgurl)
    if not os.path.exists(path[0]):
        os.mkdir(path[0])
    path = '%s/%s' % (path[0], str(path[1])+'.jpg')
    if not os.path.exists(path):
        urllib.request.urlretrieve(jpgurl, path)
    else:
        print('file already exists!')

def main():
    url = input('请输入你要批量下载漫画的网址：')
    root = input('请输入下载目录（默认当前目录）：')
    if(root): os.chdir(root)

    socks.set_default_proxy(socks.SOCKS5, "localhost", 7891)
    socket.socket = socks.socksocket

    #url = 'http://www.manhuadb.com/manhua/1051'
    html = None
    while(html == None): html = gethtml(url)
    html = html.text
    urlslist = re.findall(' <a class="" href="(.*?)" title=".*">\d+</a>', html)
    print(urlslist)
    for url1 in urlslist:
        url = 'http://www.manhuadb.com'+url1
        html = None
        while(html == None): html = gethtml(url)
        html = html.text
        name1 = re.findall('<h2 class="h4 text-center">(.*?)</h2>', html)[0]
        pages = int(re.findall(r'共 (\d*) 页', html)[0])
        print(name1,pages)
        houzhui = '.html'
        list_page_urls = []
        list_path = []
        for page in range(1, pages+1):
            if page == 1:
                pageurl = url
            else:
                pageurl = url[0:-5] + '_p' + str(page) + houzhui
            #print(name1, '第', page, '页', pageurl)
            path = [name1, page]
            list_path.append(path)
            list_page_urls.append(pageurl)
        i=0
        threads = []
        for [page,path] in zip(list_page_urls,list_path):
            t = threading.Thread(target=download,args=(page,path))
            threads.append(t)
            time.sleep(0.3)
            threads[i].start()
            i = i + 1
        threads[-1].join()
main()
