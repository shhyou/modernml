#python 2.7.10

import httplib
import subprocess
import json
import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from urlparse import urlparse

def get(url):
    sleep(1)
    return requests.get(url).text.replace('\n', '').replace('\r', '')

class apress_parse:
    host = 'http://www.apress.com/'
    ca = []
    
    def __init__(self):
        #parse all category
        res = get(self.host)
        soup = BeautifulSoup(res)
        for ul in soup.find_all('ul', {'id': 'nav'}):
            for a in ul.find_all('a'):
                self.ca.append(a.get('href').strip())

    def autorun(self):
        for link in self.ca:
            self.parse_category(link)

    def parse_category(self, link):
        page = 1
        while 1:
            res = get(link + '?p=' + str(page))
            soup = BeautifulSoup(res)
            for ul in soup.find_all('ul', 'products-grid-cust-cat'):
                for li in ul.find_all('li'):
                    url = li.find_all('a')[0].get('href').strip()
                    self.parse_book(url, urlparse(link).path)                   
                    
            page += 1
            if self.end_category(soup):
                break

    def end_category(self, soup):
        for p in soup.find_all('p', 'amount'):
            r = re.findall('Books \d+-(\d+?) of (\d+)', p.get_text())
            if len(r) == 0:
                return True
            a = r[0]
            return a[0] == a[1]

    patt = '^Chapter .+[:\.]\s+|^\d+[:\.]\s+|^Ch\. \d+:\s+|^Chapter \d+ -\s+|\s+\d+\.\s+|\d+ - '
    def fixed_chapter(self, ch):
        return re.sub(self.patt, '', ch).strip()

    def is_chapter(self, ch):
        return len(re.findall(self.patt, ch)) > 0

    def parse_book(self, link, category):
        res = get(link)
        soup = BeautifulSoup(res)

        filename = re.findall('http://.+/(.+?)\?gtmf=c', link)[0]
        
        #title source link type toc
        book = {}
        book['title'] = soup.find_all('h1')[0].get_text().strip()
        book['href'] = link
        book['category'] = [category.replace('/', '')]
        book['toc'] = []

        for div in soup.find_all('div', {'class': 'tab-content'}):
            toc_flag = False;
            for h3 in div.find_all('h3'):
                if h3.get_text().strip() == 'Table of Contents':
                    toc_flag = True;

            if toc_flag:
                if len(re.findall('(</p>){2,}', str(div))) > 0 \
                    and str(div).find('<li>') < 0:
                    print 1
                    text = str(div)
                    text = re.sub('<h3>.*?</h3>|<div.*?>|</div>|</p>|<ol></ol>|<strong.*?/strong>', '', text)
                    for ch in re.split('<p><p>|<p>', text):
                        if self.is_chapter(ch.strip()):
                            book['toc'].append(self.fixed_chapter(ch.strip()))

                elif str(div).find('<br') >= 0:
                    print 2
                    text = str(div)
                    text = re.sub('<h3>.*?</h3>|<div.*?>|</div>|<p>|</p>|<strong.*?/strong>', '', text)
                    for ch in re.split('<br.*?>', text):
                        if self.is_chapter(ch.strip()):
                            book['toc'].append(self.fixed_chapter(ch.strip()))

                else:
                    print 3
                    for p in div.find_all('p'):
                        ch = p.get_text().strip()
                        if self.is_chapter(ch):
                            book['toc'].append(self.fixed_chapter(ch))

                    for li in div.find_all('li'):
                        ch = li.get_text().strip()
                        book['toc'].append(self.fixed_chapter(ch))

                    try:
                        for div in div.find_all('div')[0].find_all('div'):
                            ch = div.get_text().strip()
                            book['toc'].append(self.fixed_chapter(ch))
                    except:
                        None

                    break;

        if len(book['toc']) > 0:
            try:
                f = open(filename, 'r')
                book = json.loads(f.read())
                f.close()
                if category.replace('/', '') not in book['category']:
                    book['category'].append(category.replace('/', ''))
            except:
                None
            f = open(filename, 'w')
            f.write(json.dumps(book))

        print json.dumps(book)

if __name__ == '__main__':
    hi = apress_parse()
    hi.autorun()
    #hi.parse_book('http://www.apress.com/9781430235279?gtmf=c', 'test')

#unsolved http://www.apress.com/9781430235811?gtmf=c <p> without </p> in <div>. WTF