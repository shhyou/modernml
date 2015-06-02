#python 2.7.10
#usage: python crawl.py <category>, e.x. python crawl.py microsoft
import httplib;
import subprocess;
import json;
import sys;
import re;
from time import sleep;
from bs4 import BeautifulSoup;
from urlparse import urlparse;

host = "http://www.apress.com/";

def getResponse(url):
    par = urlparse(url);
    conn = httplib.HTTPConnection(par.netloc);
    conn.request("GET", par.path + "?" + par.query);
    res = conn.getresponse();
    try:
        return res.read().replace("\t","").replace("\n","").replace("\r","");
    except:
        return None;
    sleep(5);

def insertToParse(objectName, data):
    val = -1;
    while val == -1:
        val = subprocess.call(["node", "Parse.js", "insert", objectName, json.dumps(data)]);

def checkEnd(soup):
    pList = soup.find_all('p', {'class' : 'amount'});
    s = pList[0].get_text();
    print s;
    a = re.findall("Books \d+-(\d+?) of (\d+)", s);
    return a[0][0] == a[0][1];    

def getCategory(name):
    page = 1;
    while page:
        content = getResponse(host + name + "?p=" + str(page));
        soup = BeautifulSoup(content);
        ulList = soup.find_all('ul', {'class' : 'products-grid-cust-cat'});
        for i in range(0, len(ulList)):
            aList = BeautifulSoup(str(ulList[i])).find_all('a');
            for j in range(0, len(aList), 2):
                id = re.findall("http://.+/(.+?)\?gtmf=c", aList[j].get("href"))[0];
                print id;
        page += 1;
        if checkEnd(soup):
            break;
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: python crawl.py <category name>";
    else:
        getCategory(sys.argv[1]);
