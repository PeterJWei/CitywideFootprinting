import web
import os
#import dynamicPopulation
import time
#from dynamicPopulation import showDynamicPopulation
import CarCounting.getDOTstream as D
import graphBackend
import staticData.foursquareCheckinData as FS
import staticData.staticTaxiData as TD
import staticData.staticCensusData as CD
import streamDaemon
import dynamicData.subwayData as SD
import dynamicData.GPSendpoint as GPSendpoint
import DBMgr
import dynamicData.loadBuildingData as LBD

db = DBMgr.DBMgr()
db.pullCoordinates("45458C82-9CE4-412F-8BD7-0D45CA175508")
S = streamDaemon.streams()
LBuildings = LBD.loadBuildings()
#Stream = streamDaemon.S
print("Assigned stream")
urls = (
	#"/(.*)", 'Service',
#	"/realtime", dynamicPopulation.doPopulation,
	"/camera", D.DOTstream,
	"/foursquareData", FS.foursquareData,
	"/taxiData", TD.taxiData,
	"/censusData", CD.censusData,
	"/graph", graphBackend.G,
	"/subway", SD.subwayData,
	"/GPSdata", GPSendpoint.GPSreport,
	"/", "baseURL"
	)



#initialization = dynamicPopulation.showDynamicPopulation()
#initialization.startup()

class baseURL:
	def GET(self):
		return "200 OK"
	def POST(self):
		return "200 OK"

class Service:
	def GET(self, name):
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		return {'message': 'GET OK!'}
	def POST(self, name):
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		data = web.data()
		return {'message': "POST OK! %s" % data}

class MyApplication(web.application):
	def run(self, port=8080, *middleware):
		self.runDynamicPopulation()
		#self.runTrafficCount()
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, ('0.0.0.0', port))

	#def runTrafficCount(self):
	def startDaemon(self):
		t=Thread(target=self._loopCheckStreams, args=())
		t.setDaemon(True)
		t.start()
	
	
	
	def runDynamicPopulation(self):
		#run1 = dynamicPopulation.showDynamicPopulation(1)
		while True:
			print("\n\nRunning dynamic\n\n")
			#print("Number of building changes" + str(len(energyServer.S.buildingChangesList)))
			for (borough, block, lot, diff) in S.buildingChangesList:
				print(borough)
				print(block)
				print(lot)
				break
				#convert borough block lot to BBL
			#LBuildings.loadBuildingChanges(S.buildingChangesList)
			
			#run1.getBlocks2Occupancy(20)
			#run1.startup()
			#run1.plotBuildings()
			#run1.plotRealtime()
			time.sleep(30)


		return

def notfound():
	return web.notfound("404 not found")

def run():
	app = MyApplication(urls, globals())
	app.notfound = notfound
	app.run(port=8001)