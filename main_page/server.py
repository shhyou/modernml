
import tornado.ioloop
import tornado.netutil
import tornado.process
import tornado.httpserver
import tornado.web
import tornado.websocket

import urlparse
import datetime
import json

s_flowchart = """
st=>start: Start:>http://www.google.com[blank]
e=>end:>http://www.google.com
op1=>operation: My Operation
sub1=>subroutine: My Subroutine
cond=>condition: Yes 
or No?:>http://www.google.com
io=>inputoutput: catch something...

st->op1->cond
cond(yes)->io->e
cond(no)->sub1(right)->op1
"""



I2A = {
	'keyword': 'algorithm',
	'noun': ['algorithm', 'sort', 'divide and conquer', 'heapsort', 'quicksort', 'median'
			, 'data structure', 'hash', 'hash table', 'binary search tree', 'red-black tree'
			, 'dynamic programming', 'greedy algorithm', 'amortized analysis', 'B tree'
			, 'fibonacci heap', 'minimum spanning tree'],
	'flowchart': s_flowchart,
	'link': [{'title': 'Introduction to Algorithms, third edition', 'href': 'https://mitpress.mit.edu/books/introduction-algorithms'}
			 , {'title': 'Introduction to Algorithms, 3rd Edition', 'href': 'http://www.amazon.com/Introduction-Algorithms-Edition-Thomas-Cormen/dp/0262033844'}
			 , {'title': 'Introduction to Algorithms', 'href': 'http://en.wikipedia.org/wiki/Introduction_to_Algorithms'}
			 , {'title': 'Algorithms (4th Edition)', 'href': 'http://www.amazon.com/gp/product/032157351X/ref=as_li_qf_sp_asin_il_tl?ie=UTF8&tag=algs4-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=032157351X'}],
};

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("./index.html")

class NoCacheStaticFileHandler(tornado.web.StaticFileHandler):
	def set_extra_headers(self, path):
		self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

class RandomKeywordHandler(tornado.web.RequestHandler):
	def get(self):
		self.write(json.dumps(I2A))

if __name__ == "__main__":
	httpsock = tornado.netutil.bind_sockets(7122)
	tornado.process.fork_processes(16)

	application = tornado.web.Application([
		(r"/", MainHandler),
		(r"/js/(.+)", NoCacheStaticFileHandler, {"path": "./js"}),
		(r"/stylesheets/(.+)", NoCacheStaticFileHandler, {"path": "./stylesheets"}),
		(r"/font/(.+)", NoCacheStaticFileHandler, {"path": "./font"}),
		(r"/random", RandomKeywordHandler),
	])

	httpsrv = tornado.httpserver.HTTPServer(application)
	httpsrv.add_sockets(httpsock)
	tornado.ioloop.IOLoop.instance().start()


