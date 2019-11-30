import re
import requests
import os
import lxml
from bs4 import BeautifulSoup
import urllib
import urllib3
import threading

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


def download(jpgurl, path):
    print(jpgurl)
    if not os.path.exists(path[0]):
        os.mkdir(path[0])
    path = '%s/%s' % (path[0], str(path[1])+'.jpg')
    with open(path,"wb") as f:
        f.write(urllib.request.urlopen(jpgurl).read())
    f.close()


def main():
    url = 'http://www.manhuadb.com/manhua/1051'
    html = gethtml(url).text
    urlslist = re.findall(' <a class="" href="(.*?)" title=".*">\d+</a>', html)
    print(urlslist)
    for url1 in urlslist:
        url = 'http://www.manhuadb.com'+url1
        html = gethtml(url).text
        name1 = re.findall('<h2 class="h4 text-center">(.*?)</h2>', html)[0]
        print(name1)
        #pagelist = re.findall('<option value="(.*?)".*?>(.*?)</option>', html)
        #print(pagelist)
        pages = int(re.findall(r'共 (\d*) 页', html)[0])
        print(pages)
        houzhui = '.html'
        for page in range(1,pages):
            if page == 1:
                pageurl = url
            else:
                pageurl = url[0:-5] + '_p' + str(page) + houzhui
            print(name1,'第',page,'页',pageurl)
            path = [name1, page]
            html = gethtml(pageurl).text
            jpgurl = \
                re.findall(
                    r'<img class="img-fluid show-pic" src="(.*?)" />', html)[0]
            download(jpgurl, path)

main()

