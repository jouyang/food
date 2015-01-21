import urllib2
import urlparse
from bs4 import BeautifulSoup

def getAllUrl(url):
    try:
        page = urllib2.urlopen( url ).read()
    except:
        return []
    urlList = []
    try:
        soup = BeautifulSoup(page)
        soup.prettify()
        for anchor in soup.findAll('a', href=True):
            if not 'http://' in anchor['href']:
                if urlparse.urljoin(url, anchor['href']) not in urlList:
                    urlList.append(urlparse.urljoin(url, anchor['href']))
            else:
                if anchor['href'] not in urlList:
                    urlList.append(anchor['href'])

        length = len(urlList)

        return urlList
    except urllib2.HTTPError, e:
        print e

def listAllUrl(urls):
    for x in urls:
        print x
        urls.remove(x)
        urls_tmp = getAllUrl(x)
        for y in urls_tmp:
            urls.append(y)


if __name__ == "__main__":
    urls = ['http://allrecipes.com/']
    while(urls.count>0):
        urls = getAllUrl('http://allrecipes.com/')
        listAllUrl(urls)