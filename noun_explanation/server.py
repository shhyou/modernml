import tornado.ioloop
import tornado.netutil
import tornado.process
import tornado.httpserver
import tornado.web
import tornado.websocket

import datetime

from urlparse import urlparse
import re
import requests
import json
import urllib

def cutWithFirstDot(string):
	left = right = 0
	for i in range(0, len(string)):
		if string[i] == '<':
			left += 1
		elif string[i] == '>':
			right += 1
		elif string[i] == '.' and string[i - 3 : i + 1] != 'i.e.' and left == right and ((i + 1 < len(string) and string[i + 1] == ' ') or i + 1 >= len(string)):
			return string[0 : i + 1]
	return string

def fixedLink(string):
	links = re.findall('href=[\'\"](.+?)[\'\"]', string);
	for i in range(0, len(links)):
		print links[i]
		if links[i][0] == '/':
			string = string.replace('href=\'' + links[i] + '\'', 'href=\'http://en.wikipedia.org' + links[i] + '\'')
			string = string.replace('href=\"' + links[i] + '\"', 'href=\'http://en.wikipedia.org' + links[i] + '\'')
	return string

def getExplanationFromWiki(vocab):
	vocab = urllib.unquote(vocab)
	res = requests.get('http://en.wikipedia.org/wiki/' + vocab)
	content = res.text.replace('\n', '').replace('\r', '').replace('\t', '')
	content = re.sub(r'<table.+?</table>', '', content)
	if content.find('Wikipedia does not have an article with this exact name.') != -1:
		return '<b>Wikipedia</b> does not have an article with this exact name.'
	else:
		paragraphs = re.findall('<p>(.+?)</p>', content)
		title = re.findall('<h1.+?>(.+?)</h1>', content)[0]
		firstSentence = re.sub(r'<sup .+?>.+?</sup>', '', paragraphs[0])
		firstSentence = cutWithFirstDot(firstSentence)
		firstSentence = fixedLink(firstSentence)

		idx = 0
		if paragraphs[idx] == '':
			idx = 1

		if paragraphs[idx].find(' may refer to:') != -1:
			return 'This word may refer to many things. See <a href=\"http://en.wikipedia.org/wiki/' + vocab + '\">' + vocab + '</a>.'
		elif paragraphs[idx].find('may stand for:') != -1: 
			return 'This word may stand to many things. See <a href=\"http://en.wikipedia.org/wiki/' + vocab + '\">' + vocab + '</a>.'
		else:
			return '<h5><a href="https://en.wikipedia.org/wiki/' + vocab + '" target="_new">' + title + '</a></h5>' + firstSentence

def calculate_score(word, keywords):
	return 0 #score mode off
	score = 0
	for key in keywords:
		if word.lower().find(key.lower()) != -1:
			score += 1
	return score

def getExplanationFromWikiThroughGoogle(vocab, keyword):
	res = requests.get("https://www.google.com.tw/search?q=site:en.wikipedia.org+" + urllib.quote(vocab) + "&bav=on.2,or.&cad=b&fp=8d02688dbcaec00c&biw=808&bih=667&dpr=1&tch=1&ech=1&psi=1d6QVe-XHs798AW5kqnABg.1435557589508.3")
	content = res.text.split('/*""*/')[1]
	dic = json.loads(content)
	link_words = []
	origin_links = re.findall('/url\?q=https://en.wikipedia.org/%3Ftitle%3D(.+?)"|/url\?q=https://en.wikipedia.org/wiki/(.+?)"', dic['d'])
	for link in origin_links:
		if link[0] == '':
			link = link[1]
		else:
			link = link[0]
		if link.find('%23') == -1:
			link_words.append(link.split('&amp;')[0])
	keywords = keyword.split(' ')
	best_idx = 0
	for i in range(len(link_words)):
		if calculate_score(link_words[i], keywords) > calculate_score(link_words[best_idx], keywords):
			best_idx = i

	result = {}
	result['content'] = getExplanationFromWiki(link_words[best_idx])
	result['others'] = []
	for i in range(len(link_words)):
		if i != best_idx:
			result['others'].append(link_words[i])

	return result

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'Client IP:' + self.request.remote_ip + '(opened)'

    def on_message(self, message):
    	print message
    	dic = json.loads(message)
        self.write_message(getExplanationFromWikiThroughGoogle(dic['vocab'], dic['keyword']))

    def on_close(self):
        print 'Client IP:' + self.request.remote_ip + '(closed)'

    def check_origin(self, origin):
    	parsed_origin = urlparse(origin)
    	return parsed_origin.netloc.endswith('') # example: .csie.ntu.edu.tw

if __name__ == '__main__':
	httpsock = tornado.netutil.bind_sockets(8357)
	tornado.process.fork_processes(16)

	application = tornado.web.Application([
		(r'/', WebSocketHandler),
	])

	httpsrv = tornado.httpserver.HTTPServer(application)
	httpsrv.add_sockets(httpsock)
	tornado.ioloop.IOLoop.instance().start()
