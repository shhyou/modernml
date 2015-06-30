
import tornado.ioloop
import tornado.netutil
import tornado.process
import tornado.httpserver
import tornado.web
import tornado.websocket

import urlparse
import datetime
import json
import random

from retrieval.item_search import search as item_search
from retrieval.keyword import generate as keyword_generate
#from retrieval.flow import generate as flow_generate

I2A = {
	'keyword': 'algorithm',
	'terms': ['algorithm', 'sort', 'divide and conquer', 'heapsort', 'quicksort', 'median'
			, 'data structure', 'hash', 'hash table', 'binary search tree', 'red black tree'
			, 'dynamic programming', 'greedy algorithm', 'amortized analysis', 'B tree'
			, 'fibonacci heap', 'minimum spanning tree'],
	'toc' : [ { 'topic': 'Dynamic Programming',
            	'item': [{'title': 'Introduction to Algorithms, third edition',
                  	 	'href': 'http://example.com',
                      'topic': 'DP'},
                     {'title': 'Algorithms (4th Edition)',
                      'href': 'http://example.com',
                      'topic': 'Dynamic Programming'},
                     {'title': 'Data structure and Algorithms',
                      'href': 'http://example.com',
                      'topic': 'Dontaiguhua'},
                    ]
	          },
	          { 'topic': 'binary search tree',
	            'item': [{'title': 'Introduction to Algorithms, third edition',
	                      'href': 'http://example.com',
	                      'topic': 'binary search tree'},
	                     {'title': 'Algorithms (4th Edition)',
	                      'href': 'http://example.com',
	                      'topic': 'binary tree Introduction to Algorithms Introduction to Algorithms Introduction to Algorithms'},
	                    ]
	          },
	        ]
};

random_keywords = ['algorithm', 'graph', 'machine learning', 'information retrieval', 'linear algebra']

def generate_result(key):
	res = {}
	res['keyword'] = key
	try:
		ids = item_search(key)
	except:
		self.set_status(404)
		print 'item_search(key) error.'
	try:
		res['terms'] = keyword_generate(ids, limit=50)
	except:
		self.set_status(404)
		print 'keyword_generate(ids) error.'
	return res

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('./http/index.html')

class SubmitHandler(tornado.web.RequestHandler):
	def get(self):
		try:
			key = self.get_argument('q')
			self.write(json.dumps(generate_result(key)))
		except:
			self.set_status(404)
			self.write('no parameter "q".')

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
	def set_extra_headers(self, path):
		self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

class RandomKeywordHandler(tornado.web.RequestHandler):
	def get(self):
		try:
			random.shuffle(random_keywords)
			key = random_keywords[0]
			self.write(json.dumps(generate_result(key)))
		except:
			self.set_status(404)
			self.write('no parameter "q".')

if __name__ == '__main__':
	httpsock = tornado.netutil.bind_sockets(9971)
	tornado.process.fork_processes(16)

	application = tornado.web.Application([
		(r'/', MainHandler),
		(r'/submit', SubmitHandler),
		(r'/js/(.+)', NoCacheStaticFileHandler, {'path': './http/js'}),
		(r'/stylesheets/(.+)', NoCacheStaticFileHandler, {'path': './http/stylesheets'}),
		(r'/font/(.+)', NoCacheStaticFileHandler, {'path': './http/font'}),
		(r'/random', RandomKeywordHandler),
	])

	httpsrv = tornado.httpserver.HTTPServer(application)
	httpsrv.add_sockets(httpsock)
	tornado.ioloop.IOLoop.instance().start()
