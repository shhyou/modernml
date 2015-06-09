import tornado.ioloop
import tornado.netutil
import tornado.process
import tornado.httpserver
import tornado.web
import tornado.websocket

import datetime

import httplib
import urllib
from urlparse import urlparse
import re

def getResponse(url):
	print url
	tmpurl = urlparse(url)
	conn = httplib.HTTPConnection(tmpurl.netloc)
	conn.request('GET', tmpurl.path)
	return conn.getresponse()

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
	res = getResponse('http://en.wikipedia.org/wiki/' + urllib.quote(vocab))
	if res.getheader('location', None) != None:
		res = getResponse(res.getheader('location'))
	content = res.read().replace('\n', '').replace('\r', '').replace('\t', '')
	content = re.sub(r'<table.+?</table>', '', content)
	if content.find('Wikipedia does not have an article with this exact name.') != -1:
		return '<b>Wikipedia</b> does not have an article with this exact name.'
	else:
		paragraphs = re.findall('<p>(.+?)</p>', content)
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
			return firstSentence


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'Client IP:' + self.request.remote_ip + '(opened)'

    def on_message(self, message):
        self.write_message(getExplanationFromWiki(message))

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
