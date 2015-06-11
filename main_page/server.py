
import tornado.ioloop
import tornado.netutil
import tornado.process
import tornado.httpserver
import tornado.web
import tornado.websocket

import urlparse
import datetime
import json

I2A = {
	'keyword': 'algorithm',
	'terms': ['algorithm', 'sort', 'divide and conquer', 'heapsort', 'quicksort', 'median'
			, 'data structure', 'hash', 'hash table', 'binary search tree', 'red-black tree'
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

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('./index.html')

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
	def set_extra_headers(self, path):
		self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

class RandomKeywordHandler(tornado.web.RequestHandler):
	def get(self):
		self.write(json.dumps(I2A))

if __name__ == '__main__':
	httpsock = tornado.netutil.bind_sockets(9971)
	tornado.process.fork_processes(16)

	application = tornado.web.Application([
		(r'/', MainHandler),
		(r'/js/(.+)', NoCacheStaticFileHandler, {'path': './js'}),
		(r'/stylesheets/(.+)', NoCacheStaticFileHandler, {'path': './stylesheets'}),
		(r'/font/(.+)', NoCacheStaticFileHandler, {'path': './font'}),
		(r'/random', RandomKeywordHandler),
	])

	httpsrv = tornado.httpserver.HTTPServer(application)
	httpsrv.add_sockets(httpsock)
	tornado.ioloop.IOLoop.instance().start()


