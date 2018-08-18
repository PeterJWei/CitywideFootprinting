import web
import os
import dataFeeds
urls = ()

D = dataFeeds.dataFeeds()

class MyApplication(web.application):
	def run(self, port=8080, *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, ('0.0.0.0', port))

def notfound():
	return web.notfound("404 not found")

def run():
	app = MyApplication(urls, globals())
	app.notfound = notfound
	app.run(port=8000)