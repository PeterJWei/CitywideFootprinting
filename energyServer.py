import web
import os
import dynamicPopulation
urls = (
	"/realtime", dynamicPopulation.doPopulation
	)

#initialization = dynamicPopulation.showDynamicPopulation()
#initialization.startup()

class MyApplication(web.application):
	def run(self, port=8080, *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, ('0.0.0.0', port))

def notfound():
	return web.notfound("404 not found")

def runDynamicPopulation():
	# run1 = showDynamicPopulation()
	# run1.startup()
	# run1.getBlocks2Occupancy(1)
	# run1.plotDynamic()
	# run1.getBlocks2Occupancy(2)
	# run1.plotDynamic()
	# run1.getBlocks2Occupancy(3)
	# run1.plotDynamic()
	# run1.getBlocks2Occupancy(4)
	# run1.plotDynamic()
	# run1.getBlocks2Occupancy(5)
	# run1.plotDynamic()
	# run1.getBlocks2Occupancy(6)
	# run1.plotDynamic()
	return

def run():
	app = MyApplication(urls, globals())
	app.notfound = notfound
	app.run(port=8000)