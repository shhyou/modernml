#python 2.7.10

import httplib;
import subprocess;
import json;
import re;
import requests;
from time import sleep;
from bs4 import BeautifulSoup;

def insertToParse(objectName, data):
    val = -1;
    while val == -1:
        val = subprocess.call(['node', 'Parse.js', 'insert', objectName, json.dumps(data)]);

def get(url):
    sleep(5);
    return requests.get(url).text;

class apress_parse:
    
    pre_url = 'http://www.apress.com/';
    def __init__(self):
        #parse all category
        sleep(0);

    def parse_book(self, category):
        page = 1;
        while 1:
            res = get(self.pre_url + category + '?p=' + str(page));
            soup = BeautifulSoup(res);
            for ul in soup.find_all('ul', 'products-grid-cust-cat'):
                for li in ul.find_all('li'):
                    url = li.find_all('a')[0].get('href').strip();
                    print url;                    
                    
            page += 1;
            if self.end(soup):
                break;

    def end(self, soup):
        for p in soup.find_all('p', 'amount'):
            a = re.findall('Books \d+-(\d+?) of (\d+)', p.get_text());
            print a[0][0] + ' ' + a[0][1];
            return a[0][0] == a[0][1];

if __name__ == '__main__':
    hi = apress_parse();
    hi.parse_book('microsoft')
