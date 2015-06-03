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
    host = 'http://www.apress.com/';
    
    def __init__(self):
        #parse all category
        res = get(self.host);
        soup = BeautifulSoup(res);
        ca = [];
        for ul in soup.find_all('ul', {'id': 'nav'}):
            for a in ul.find_all('a'):
                ca.append(a.get('href').strip());
        for link in ca:
            self.parse_category(link);

    def parse_category(self, link):
        page = 1;
        while 1:
            res = get(link + '?p=' + str(page));
            soup = BeautifulSoup(res);
            for ul in soup.find_all('ul', 'products-grid-cust-cat'):
                for li in ul.find_all('li'):
                    url = li.find_all('a')[0].get('href').strip();
                    self.parse_book(url);                   
                    
            page += 1;
            if self.end_category(soup):
                break;

    def end_category(self, soup):
        for p in soup.find_all('p', 'amount'):
            a = re.findall('Books \d+-(\d+?) of (\d+)', p.get_text());
            return a[0][0] == a[0][1];

    def parse_book(self, link):
        res = get(link);
        soup = BeautifulSoup(res);
        
        #title source link type toc
        book = {};
        book['title'] = soup.find_all('h1')[0].get_text().strip();        book['source'] = 'apress';
        book['link'] = link;
        book['type'] = 'book';
        

if __name__ == '__main__':
    hi = apress_parse();
    hi.parse_book('microsoft')
