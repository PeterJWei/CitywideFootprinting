import web
import os
import dynamicPopulation
import time
#from dynamicPopulation import showDynamicPopulation
import CarCounting.getDOTstream as D


urls = (
	"/realtime", dynamicPopulation.doPopulation,
	"/camera", D.DOTstream
	)

#initialization = dynamicPopulation.showDynamicPopulation()
#initialization.startup()

class MyApplication(web.application):
	def run(self, port=8080, *middleware):
		#self.runDynamicPopulation()
		#self.runTrafficCount()
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, ('0.0.0.0', port))

	#def runTrafficCount(self):


	def runDynamicPopulation(self):
		run1 = dynamicPopulation.showDynamicPopulation(1)
		while True:
			print("\n\nRunning dynamic\n\n")
			run1.getBlocks2Occupancy(20)
			run1.startup()
			#run1.plotBuildings()
			#run1.plotRealtime()
			time.sleep(30)
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

def notfound():
	return web.notfound("404 not found")

def run():
	app = MyApplication(urls, globals())
	app.notfound = notfound
	app.run(port=8000)