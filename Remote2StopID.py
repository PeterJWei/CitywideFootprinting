import time
import csv
import datetime
import matplotlib.pyplot as plt
class remoteDictionary:
	def __init__(self):
		print("Initializing Remote Dictionary.")
		print("Creating Station Name Translation...")
		start = time.time()
		self.createLegend()
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")
		print("Creating Booth to Station Dictionary...")
		start = time.time()
		self.loadRemote2Station("TurnstileData/Remote-Booth-Station-3.csv")
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")
		print("Creating Station to Latitude/Longitude Dictionary...")
		start = time.time()
		self.loadStation2Coordinates("SubwayStations/SubwayStationCoordinates.csv")
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")
		print("Loading Turnstile Data...")
		start = time.time()
		self.loadTurnstile('TurnstileData/turnstile_180811.csv')
		end = time.time()
		print("Finished: " + str(end-start) + " s\n")

	def loadRemote2Station(self, remoteKeyFile):
		self.remote2station = {}
		with open (remoteKeyFile, 'rb') as csvfile:
			data = [row for row in csv.reader(csvfile.read().splitlines())]
			reader = data
			i = True
			total = 0
			errors = 0
			for row in reader: 
				total += 1
				if i: #skip the first line
					i = False
					continue
				else:
					remote = row[0]
					booth = row[1]
					stationName = row[2]
					lineName = row[3]
					key = stationName + "," + lineName
					if key in self.Remote2StopID:
						self.remote2station[booth + remote] = self.Remote2StopID[key]
					else:
						errors += 1
						continue
			print(str(errors) + "/" + str(total) + " station names not found.")

	def loadStation2Coordinates(self, coordinatesFile):
		self.coordinates = {}
		with open (coordinatesFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader: 
				if i: #skip the first line
					i = False
					continue
				else:
					GTFSStopID = row[2]
					GTFSLatitude = float(row[9])
					GTFSLongitude = float(row[10])
					self.coordinates[GTFSStopID] = (GTFSLatitude, GTFSLongitude)

	def loadTurnstile(self, turnstileFile):
		self.timeSeriesDataEntries = {}
		self.timeSeriesDataExits = {}
		with open (turnstileFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			total = 0
			errors = 0
			for row in reader: 
				total += 1
				if i: #skip the first line
					i = False
					continue
				else:
					booth = row[0]
					unit = row[1]
					#stationName = row[3]
					date = row[6]
					ds = date.split("/")
					t = row[7]
					ts = t.split(":")
					newDate = ""
					for n in ds:
						if len(n) == 1:
							newDate += "0" + n
							newDate += "/"
						else:
							newDate += n
							newDate += "/"
					date = newDate[:-1]
					if len(ts[0]) == 1:
						t = "0" + t
					try:
						d = datetime.datetime.strptime(date + "," + t, "%m/%d/%y,%H:%M:%S")
					except ValueError:
						print(date + "," + t)
						continue
					diff = d - datetime.datetime(2018, 8, 4, 0, 0, 0)
					#print(d)
					#print(diff.days)
					#print(diff.seconds/3600)
					index = (diff.days * 24 + diff.seconds / 3600) / 4
					entries = row[9]
					exits = row[10]
					key = booth + unit
					if key not in self.remote2station:
						errors += 1
						#print("Key " + booth + " " + unit + " not found")
						continue
					station = self.remote2station[key]

					if station not in self.timeSeriesDataEntries:
						self.timeSeriesDataEntries[station] = [0] * 42
						self.timeSeriesDataExits[station] = [0] * 42
						#boothNTAs[booth] = nta
					self.timeSeriesDataEntries[station][index] += int(entries)
					self.timeSeriesDataExits[station][index] += int(exits)
			for station in self.timeSeriesDataEntries:
				for i in range(1, len(self.timeSeriesDataEntries[station])):
					if self.timeSeriesDataEntries[station][i] > self.timeSeriesDataEntries[station][i-1] + 100000:
						if i == len(self.timeSeriesDataEntries[station])-1:
							self.timeSeriesDataEntries[station][i] = self.timeSeriesDataEntries[station][i-1]
						else:
							self.timeSeriesDataEntries[station][i] = (self.timeSeriesDataEntries[station][i-1] + self.timeSeriesDataEntries[station][i+1])/2
			dp = False
			if (dp):
				print(self.timeSeriesDataEntries[station])
				x = [datetime.datetime(2018, 8, i, j, 0, 0) + datetime.timedelta(hours=4) for i in range(4, 11) for j in range(0,24,4)]
				self.fig = plt.figure()
				self.ax = plt.axes()
				plt.scatter(x, self.timeSeriesDataEntries[station])
				plt.xlabel("Time")
				plt.ylabel("People Count")
				plt.title(station + " station")
				plt.axis([datetime.datetime(2018,8,4,0,0,0),datetime.datetime(2018,8,11,0,0,0),19290000,19360000])
				plt.show()
			print("Missing Keys: " + str(errors) + "/" + str(total))

		#for booth in timeSeriesDataEntries:
		#	nta = boothNTAs[booth]
		#	for n in nta:
		#		if n not in ntaDictionary:
		#			ntaDictionary[n] = [0] * 41
		#		for i in range(len(timeSeriesDataEntries[booth])-1):
		#			ntaDictionary[n][i] += (int(timeSeriesDataEntries[booth][i+1]) - int(timeSeriesDataEntries[booth][i]))/len(nta)
		#			ntaDictionary[n][i] -= (int(timeSeriesDataExits[booth][i+1]) - int(timeSeriesDataExits[booth][i]))/len(nta)
		#return ntaDictionary

	def createLegend(self):
		self.Remote2StopID = {}
		self.Remote2StopID['DITMARS BL-31 S,NQ'] = 'R01' #Astoria - Ditmars BLVD
		self.Remote2StopID['HOYT ST-ASTORIA,NQ'] = 'R03' #Astoria BLVD
		self.Remote2StopID['GRAND-30 AVE,NQ'] = 'R04' #30 AV
		self.Remote2StopID['BROADWAY-31 ST,NQ'] = 'R05' #BROADWAY
		self.Remote2StopID['WASHINGTON-36 A,NQ'] = 'R06' #36 AV
		self.Remote2StopID['BEEBE-39 AVE,NQ'] = 'R08' #39 AV
		self.Remote2StopID['LEXINGTON AVE,456NQR'] = 'R11' #Lexington AV/59 ST
		self.Remote2StopID['5 AVE-59 ST,NQR'] = 'R13' #5 AV/59 ST
		self.Remote2StopID['57 ST-7 AVE,NQR'] = 'R14' #57 ST- 7AV
		self.Remote2StopID['49 ST-7 AVE,NQR'] = 'R15' #49 ST
		self.Remote2StopID['42 ST-TIMES SQ,1237ACENQRS'] = 'R16' #TIMES SQ 42 ST
		self.Remote2StopID['34 ST-HERALD SQ,BDFMNQR'] = 'R17' #34 ST Herald Sq
		self.Remote2StopID['28 ST-BROADWAY,NR'] = 'R18' #28 ST
		self.Remote2StopID['23 ST-5 AVE,NR'] = 'R19'
		self.Remote2StopID['14 ST-UNION SQ,LNQR456'] = 'R20'
		self.Remote2StopID['14 ST-UNION SQ,LNRQ456'] = 'R20'
		self.Remote2StopID["8 ST-B'WAY NYU,NR"] = 'R21'
		self.Remote2StopID["PRINCE ST-B'WAY,NR"] = 'R22'
		self.Remote2StopID['CANAL ST,JNQRZ6'] = 'R23'
		#self.Remote2StopID['BOROUGH HALL/CT'] = 'R24'
		self.Remote2StopID['CORTLANDT ST,R'] = 'R25'
		self.Remote2StopID['RECTOR ST,R'] = 'R26'
		self.Remote2StopID['WHITEHALL ST,R1'] = 'R27'
		self.Remote2StopID['BOROUGH HALL/CT,2345R'] = 'R28'
		self.Remote2StopID['JAY ST-METROTEC,R'] = 'R29'
		self.Remote2StopID['DEKALB AVE,BDNQR'] = 'R30'
		self.Remote2StopID['ATLANTIC AVE,2345BDNQR'] = 'R31'
		self.Remote2StopID['UNION ST,R'] = 'R32'
		self.Remote2StopID['9 ST,DFGMNR'] = 'R33'
		self.Remote2StopID['PROSPECT AVE,R'] = 'R34'
		self.Remote2StopID['25 ST,R'] = 'R35'
		self.Remote2StopID['36 ST,DNR'] = 'R36'
		self.Remote2StopID['45 ST,R'] = 'R39'
		self.Remote2StopID['53 ST,R'] = 'R40'
		self.Remote2StopID['59 ST,NR'] = 'R41'
		self.Remote2StopID['BAY RIDGE AVE,R'] = 'R42'
		self.Remote2StopID['77 ST,R'] = 'R43'
		self.Remote2StopID['86 ST,R'] = 'R44'
		self.Remote2StopID['BAY RIDGE-95 ST,R'] = 'R45'
		self.Remote2StopID['ATLANTIC AVE,2345BDNQR'] = 'D24'
		self.Remote2StopID['7 AVE,BQ'] = 'D25'
		self.Remote2StopID['PROSPECT PARK,BQS'] = 'D26'
		self.Remote2StopID['PARKSIDE AVE,BQ'] = 'D27'
		self.Remote2StopID['CHURCH AVE,BQ'] = 'D28'
		self.Remote2StopID['BEVERLEY ROAD,BQ'] = 'D29'
		self.Remote2StopID['CORTELYOU ROAD,BQ'] = 'D30'
		self.Remote2StopID['NEWKIRK AVE,BQ'] = 'D31'
		self.Remote2StopID['AVE H,BQ'] = 'D32'
		self.Remote2StopID['AVE J,BQ'] = 'D33'
		self.Remote2StopID['AVE M,BQ'] = 'D34'
		self.Remote2StopID['KINGS HIGHWAY,BQ'] = 'D35'
		self.Remote2StopID['AVE U,BQ'] = 'D37'
		self.Remote2StopID['NECK ROAD,BQ'] = 'D38'
		self.Remote2StopID['SHEEPSHEAD BAY,BQ'] = 'D39'
		self.Remote2StopID['BRIGHTON BEACH,BQ'] = 'D40'
		self.Remote2StopID['OCEAN PARKWAY,Q'] = 'D41'
		self.Remote2StopID['W 8 ST-AQUARIUM,FQ'] = 'D42'
		self.Remote2StopID['STILLWELL AVE,DFNQ'] = 'D43'
		self.Remote2StopID['9 AVE,D'] = 'B12'
		self.Remote2StopID['FT HAMILTON PKY,D'] = 'B13'
		self.Remote2StopID['50 ST,D'] = 'B14'
		self.Remote2StopID['55 ST,D'] = 'B15'
		#self.Remote2StopID['AVE H'] = 'B16'
		self.Remote2StopID['71 ST,D'] = 'B17'
		self.Remote2StopID['79 ST,D'] = 'B18'
		self.Remote2StopID['18 AVE,D'] = 'B19'
		self.Remote2StopID['20 AVE,D'] = 'B20'
		self.Remote2StopID['BAY PARKWAY,D'] = 'B21'
		self.Remote2StopID['25 AVE,D'] = 'B22'
		self.Remote2StopID['BAY 50 ST,D'] = 'B23'
		self.Remote2StopID['8 AVE,N'] = 'N02'
		self.Remote2StopID['FT HAMILTON PKY,N'] = 'N03'
		self.Remote2StopID['NEW UTRECHT AVE,ND'] = 'N04'
		self.Remote2StopID['18 AVE,N'] = 'N05'
		self.Remote2StopID['20 AVE,N'] = 'N06'
		self.Remote2StopID['BAY PKY-22 AVE,N'] = 'N07'
		self.Remote2StopID['KINGS HIGHWAY,N'] = 'N08'
		self.Remote2StopID['AVE U,N'] = 'N09'
		self.Remote2StopID['86 ST,N'] = 'N10'
		self.Remote2StopID['121 ST,JZ'] = 'J12'
		self.Remote2StopID['111 ST,J'] = 'J13'
		self.Remote2StopID['104 ST,JZ'] = 'J14'
		self.Remote2StopID['WOODHAVEN BLVD,JZ'] = 'J15'
		self.Remote2StopID['FOREST PARKWAY,J'] = 'J16'
		self.Remote2StopID['ELDERTS LANE,JZ'] = 'J17'
		self.Remote2StopID['CYPRESS HILLS,J'] = 'J19'
		self.Remote2StopID['CRESCENT ST,JZ'] = 'J20'
		self.Remote2StopID['NORWOOD AVE,JZ'] = 'J21'
		self.Remote2StopID['CLEVELAND ST,J'] = 'J22'
		self.Remote2StopID['VAN SICLEN AVE,JZ'] = 'J23'
		self.Remote2StopID['ALABAMA AVE,J'] = 'J24'
		self.Remote2StopID['BROADWAY-ENY,ACJLZ'] = 'J27'
		self.Remote2StopID['CHAUNCEY ST,JZ'] = 'J28'
		self.Remote2StopID['HALSEY ST,J'] = 'J29'
		self.Remote2StopID['GATES AVE,JZ'] = 'J30'
		self.Remote2StopID['KOSCIUSZKO ST,J'] = 'J31'
		self.Remote2StopID['MYRTLE AVE,JMZ'] = 'M11'
		self.Remote2StopID['FLUSHING AVE,JM'] = 'M12'
		self.Remote2StopID['LORIMER ST,JM'] = 'M13'
		self.Remote2StopID['HEWES ST,JM'] = 'M14'
		self.Remote2StopID['MARCY AVE,JMZ'] = 'M16'
		self.Remote2StopID['ESSEX ST,FJMZ'] = 'M18'
		self.Remote2StopID['BOWERY,JZ'] = 'M19'
		self.Remote2StopID['CANAL ST,JNQRZ6'] = 'M20'
		self.Remote2StopID['CHAMBERS ST,456JZ'] = 'M21'
		self.Remote2StopID['FULTON ST,ACJZ2345'] = 'M22'
		self.Remote2StopID['BROAD ST,JZ'] = 'M23'
		self.Remote2StopID['METROPOLITAN AV,M'] = 'M01'
		self.Remote2StopID['FRESH POND ROAD,M'] = 'M04'
		self.Remote2StopID['FOREST AVE,M'] = 'M05'
		self.Remote2StopID['SENECA AVE,M'] = 'M06'
		self.Remote2StopID['MYRTLE AVE,LM'] = 'M08'
		self.Remote2StopID['KNICKERBOCKER,M'] = 'M09'
		self.Remote2StopID['CENTRAL AVE,M'] = 'M10'
		self.Remote2StopID['8 AVE,ACEL'] = 'L01'
		self.Remote2StopID['14 ST-6 AVE,FLM123'] = 'L02'
		self.Remote2StopID['6 AVE,FLM123'] = 'L02'
		self.Remote2StopID['14 ST-UNION SQ,LNQR456'] = 'L03'
		self.Remote2StopID['3 AVE,L'] = 'L05'
		self.Remote2StopID['1 AVE,L'] = 'L06'
		self.Remote2StopID['BEDFORD AVE,L'] = 'L08'
		self.Remote2StopID['LORIMER ST,GL'] = 'L10'
		self.Remote2StopID['GRAHAM AVE,L'] = 'L11'
		self.Remote2StopID['GRAND ST,L'] = 'L12'
		self.Remote2StopID['MONTROSE AVE,L'] = 'L13'
		self.Remote2StopID['MORGAN AVE,L'] = 'L14'
		self.Remote2StopID['JEFFERSON ST,L'] = 'L15'
		self.Remote2StopID['DEKALB AVE,L'] = 'L16'
		self.Remote2StopID['MYRTLE AVE,LM'] = 'L17'
		self.Remote2StopID['HALSEY ST,L'] = 'L19'
		self.Remote2StopID['WILSON AVE,L'] = 'L20'
		self.Remote2StopID['BUSHWICK AVE,L'] = 'L21'
		self.Remote2StopID['BROADWAY-ENY,ACJLZ'] = 'L22'
		self.Remote2StopID['ATLANTIC AVE,L'] = 'L24'
		self.Remote2StopID['SUTTER AVE,L'] = 'L25'
		self.Remote2StopID['LIVONIA AVE,L'] = 'L26'
		self.Remote2StopID['NEW LOTS AVE,L'] = 'L27'
		self.Remote2StopID['EAST 105 ST,L'] = 'L28'
		self.Remote2StopID['ROCKAWAY PKY,L'] = 'L29'
		self.Remote2StopID['FRANKLIN AVE,ACS'] = 'S01'
		self.Remote2StopID['BOTANIC GARDEN,S2345'] = 'S04'
		self.Remote2StopID['PARK PLACE,S'] = 'S03'
		self.Remote2StopID['INWOOD-207 ST,A'] = 'A02'
		self.Remote2StopID['DYCKMAN-200 ST,A'] = 'A03'
		self.Remote2StopID['190 ST,A'] = 'A05'
		self.Remote2StopID['181 ST,A'] = 'A06'
		self.Remote2StopID['175 ST,A'] = 'A07'
		self.Remote2StopID['168 ST-BROADWAY,1AC'] = 'A09'
		self.Remote2StopID['163 ST-AMSTERDM,C'] = 'A10'
		self.Remote2StopID['155 ST,C'] = 'A11'
		self.Remote2StopID['145 ST,ABCD'] = 'A12'
		self.Remote2StopID['135 ST,BC'] = 'A14'
		self.Remote2StopID['125 ST,ABCD'] = 'A15'
		self.Remote2StopID['125 ST,ACBD'] = 'A15'
		self.Remote2StopID['116 ST,BC'] = 'A16'
		self.Remote2StopID['CATHEDRL-110 ST,BC'] = 'A17'
		self.Remote2StopID['103 ST,BC'] = 'A18'
		self.Remote2StopID['96 ST,BC'] = 'A19'
		self.Remote2StopID['86 ST,BC'] = 'A20'
		self.Remote2StopID['81 ST-MUSEUM,BC'] = 'A21'
		self.Remote2StopID['72 ST,BC'] = 'A22'
		self.Remote2StopID['59 ST-COLUMBUS,1ABCD'] = 'A24'
		self.Remote2StopID['50 ST,CE'] = 'A25'
		self.Remote2StopID['42 ST-PA BUS TE,ACENQRS1237'] = 'A27'
		self.Remote2StopID['34 ST-PENN STA,123ACE'] = 'A28'
		self.Remote2StopID['34 ST-PENN STA,ACE'] = 'A28'
		self.Remote2StopID['23 ST,CE'] = 'A30'
		self.Remote2StopID['14 ST,ACEL'] = 'A31'
		self.Remote2StopID['W 4 ST-WASH SQ,ABCDEFM'] = 'A32'
		#self.Remote2StopID['BOTANIC GARDEN'] = 'D20'
		self.Remote2StopID['SPRING ST,CE'] = 'A33'
		self.Remote2StopID['CANAL ST,ACE'] = 'A34'
		self.Remote2StopID['CHAMBERS ST,ACE23'] = 'A36'
		self.Remote2StopID['WORLD TRADE CTR,23ACE'] = 'E01'
		self.Remote2StopID['FULTON ST,2345ACJZ'] = 'A38'
		self.Remote2StopID['HIGH ST,AC'] = 'A40'
		self.Remote2StopID['JAY ST-METROTEC,ACF'] = 'A41'
		self.Remote2StopID['HOYT/SCHERMER,ACG'] = 'A42'
		self.Remote2StopID['LAFAYETTE AVE,C'] = 'A43'
		self.Remote2StopID['CLINTON-WASH AV,C'] = 'A44'
		self.Remote2StopID['FRANKLIN AVE,ACS'] = 'A45'
		self.Remote2StopID['NOSTRAND AVE,AC'] = 'A46'
		self.Remote2StopID['KINGSTON-THROOP,C'] = 'A47'
		self.Remote2StopID['UTICA AVE,AC'] = 'A48'
		self.Remote2StopID['RALPH AVE,C'] = 'A49'
		self.Remote2StopID['ROCKAWAY AVE,C'] = 'A50'
		self.Remote2StopID['BROADWAY-ENY,ACJLZ'] = 'A51'
		self.Remote2StopID['LIBERTY AVE,C'] = 'A52'
		self.Remote2StopID['VAN SICLEN AVE,C'] = 'A53'
		self.Remote2StopID['SHEPHERD AVE,C'] = 'A54'
		self.Remote2StopID['EUCLID AVE,AC'] = 'A55'
		self.Remote2StopID['GRANT AVE,A'] = 'A57'
		self.Remote2StopID['HUDSON-80 ST,A'] = 'A59'
		self.Remote2StopID['BOYD-88 ST,A'] = 'A60'
		self.Remote2StopID['ROCKAWAY BLVD,A'] = 'A61'
		self.Remote2StopID['OXFORD-104 ST,A'] = 'A63'
		self.Remote2StopID['GREENWOOD-111,A'] = 'A64'
		self.Remote2StopID['LEFFERTS BLVD,A'] = 'A65'
		self.Remote2StopID['AQUEDUCT TRACK,A'] = 'H01'
		self.Remote2StopID['AQUEDUCT-N CNDT,A'] = 'H02'
		self.Remote2StopID['HOWARD BCH-JFK,A'] = 'H03'
		self.Remote2StopID['BROAD CHANNEL,AS'] = 'H04'
		#self.Remote2StopID['BEACH 90 ST,AS'] = 'H19'
		self.Remote2StopID['BEACH 90 ST,AS'] = 'H12'
		self.Remote2StopID['BEACH 98 ST,AS'] = 'H13'
		self.Remote2StopID['BEACH 105 ST,AS'] = 'H14'
		self.Remote2StopID['ROCKAWAY PK 116,AS'] = 'H15'
		self.Remote2StopID['BEACH 67 ST,A'] = 'H06'
		self.Remote2StopID['BEACH 60 ST,A'] = 'H07'
		self.Remote2StopID['BEACH 44 ST,A'] = 'H08'
		self.Remote2StopID['BEACH 36 ST,A'] = 'H09'
		self.Remote2StopID['BEACH 25 ST,A'] = 'H10'
		self.Remote2StopID['FAR ROCKAWAY,A'] = 'H11'
		self.Remote2StopID['NORWOOD-205 ST,D'] = 'D01'
		self.Remote2StopID['BEDFORD PARK BL,BD'] = 'D03'
		self.Remote2StopID['KINGSBRIDGE RD,BD'] = 'D04'
		self.Remote2StopID['FORDHAM ROAD,BD'] = 'D05'
		self.Remote2StopID['182-183 ST,BD'] = 'D06'
		self.Remote2StopID['TREMONT AVE,BD'] = 'D07'
		self.Remote2StopID['174-175 ST,BD'] = 'D08'
		self.Remote2StopID['170 ST,BD'] = 'D09'
		self.Remote2StopID['167 ST,BD'] = 'D10'
		self.Remote2StopID['161 ST-YANKEE,BD4'] = 'D11'
		self.Remote2StopID['155 ST,BD'] = 'D12'
		self.Remote2StopID['21 ST,F'] = 'B04'
		self.Remote2StopID['ROOSEVELT IS,F'] = 'B06'
		self.Remote2StopID['LEXINGTON AVE,F'] = 'B08'
		self.Remote2StopID['57 ST,F'] = 'B10'
		self.Remote2StopID['47-50 ST-ROCK,BDFM'] = 'D15'
		self.Remote2StopID['42 ST-BRYANT PK,BDFM7'] = 'D16'
		self.Remote2StopID['34 ST-HERALD SQ,BDFMNQR'] = 'D17'
		self.Remote2StopID['23 ST-6 AVE,FM'] = 'D18'
		self.Remote2StopID['14 ST-6 AVE,FLM123'] = 'D19'
		self.Remote2StopID['BROADWAY/LAFAY,BDFQ6'] = 'D21'
		self.Remote2StopID['GRAND ST,BD'] = 'D22'
		self.Remote2StopID['2 AVE,F'] = 'F14'
		self.Remote2StopID['DELANCEY ST,FJMZ'] = 'F15'
		self.Remote2StopID['EAST BROADWAY,F'] = 'F16'
		self.Remote2StopID['YORK ST,F'] = 'F18'
		self.Remote2StopID['BERGEN ST,FG'] = 'F20'
		self.Remote2StopID['CARROLL ST,FG'] = 'F21'
		self.Remote2StopID['SMITH-9 ST,FG'] = 'F22'
		self.Remote2StopID['4 AVE,DFGMNR'] = 'F23'
		self.Remote2StopID['7 AV-PARK SLOPE,FG'] = 'F24'
		self.Remote2StopID['15 ST-PROSPECT,FG'] = 'F25'
		self.Remote2StopID['FT HAMILTON PKY,FG'] = 'F26'
		self.Remote2StopID['CHURCH AVE,FG'] = 'F27'
		self.Remote2StopID['DITMAS AVE,F'] = 'F29'
		self.Remote2StopID['18 AVE,F'] = 'F30'
		self.Remote2StopID['AVE I,F'] = 'F31'
		self.Remote2StopID['22 AVE-BAY PKY,F'] = 'F32'
		self.Remote2StopID['AVE N,F'] = 'F33'
		self.Remote2StopID['AVE P,F'] = 'F34'
		self.Remote2StopID['KINGS HIGHWAY,F'] = 'F35'
		self.Remote2StopID['AVE U,F'] = 'F36'
		self.Remote2StopID['AVE X,F'] = 'F38'
		self.Remote2StopID['NEPTUNE AVE,F'] = 'F39'
		self.Remote2StopID['JAMAICA-179 ST,F'] = 'F01'
		self.Remote2StopID['169 ST,F'] = 'F02'
		self.Remote2StopID['PARSONS BLVD,F'] = 'F03'
		self.Remote2StopID['SUTPHIN BLVD,F'] = 'F04'
		self.Remote2StopID['VAN WYCK BLVD,EF'] = 'F05'
		self.Remote2StopID['UNION TPK-KEW G,EF'] = 'F06'
		self.Remote2StopID['75 AVE,EF'] = 'F07'
		self.Remote2StopID['FOREST HILLS-71,EFMR'] = 'G08'
		self.Remote2StopID['67 AVE,MR'] = 'G09'
		self.Remote2StopID['63 DR-REGO PARK,MR'] = 'G10'
		self.Remote2StopID['WOODHAVEN BLVD,MR'] = 'G11'
		self.Remote2StopID['GRAND AV-NEWTOWN,MR'] = 'G12'
		self.Remote2StopID['GRAND AV-NEWTON,MR'] = 'G12'
		self.Remote2StopID['ELMHURST AVE,MR'] = 'G13'
		self.Remote2StopID['ROOSEVELT AVE,EFMR7'] = 'G14'
		self.Remote2StopID['65 ST,MR'] = 'G15'
		self.Remote2StopID['NORTHERN BLVD,MR'] = 'G16'
		self.Remote2StopID['46 ST,MR'] = 'G18'
		self.Remote2StopID['STEINWAY ST,MR'] = 'G19'
		self.Remote2StopID['36 ST,MR'] = 'G20'
		self.Remote2StopID['QUEENS PLAZA,EMR'] = 'G21'
		self.Remote2StopID['COURT SQ,EMG'] = 'F09'
		self.Remote2StopID['COURT SQ-23 ST,EMG'] = 'F09'
		self.Remote2StopID['LEXINGTON-53 ST,EM6'] = 'F11'
		self.Remote2StopID['5 AVE-53 ST,EM'] = 'F12'
		self.Remote2StopID['7 AVE-53 ST,BDE'] = 'D14'
		self.Remote2StopID['JAMAICA CENTER,EJZ'] = 'G05'
		self.Remote2StopID['SUTPHIN BLVD,EJZ'] = 'G06'
		self.Remote2StopID['JAMAICA-VAN WYC,E'] = 'G07'
		self.Remote2StopID['COURT SQ-23 ST,EMG'] = 'G22'
		self.Remote2StopID['COURT SQ,EMG'] = 'G22'
		self.Remote2StopID['VAN ALSTON-21ST,G'] = 'G24'
		self.Remote2StopID['GREENPOINT AVE,G'] = 'G26'
		self.Remote2StopID['NASSAU AV,G'] = 'G28'
		self.Remote2StopID['METROPOLITAN AV,G'] = 'G29'
		self.Remote2StopID['METROPOLITAN AV,GL'] = 'G29'
		self.Remote2StopID['BROADWAY,G'] = 'G30'
		self.Remote2StopID['FLUSHING AVE,G'] = 'G31'
		self.Remote2StopID['MYRTLE-WILLOUGH,G'] = 'G32'
		self.Remote2StopID['BEDFORD/NOSTRAN,G'] = 'G33'
		self.Remote2StopID['CLASSON AVE,G'] = 'G34'
		self.Remote2StopID['CLINTON-WASH AV,G'] = 'G35'
		self.Remote2StopID['FULTON ST,G'] = 'G36'
		self.Remote2StopID['242 ST,1'] = '101'
		self.Remote2StopID['238 ST,1'] = '103'
		self.Remote2StopID['231 ST,1'] = '104'
		self.Remote2StopID['MARBLE HILL-225,1'] = '106'
		self.Remote2StopID['215 ST,1'] = '107'
		self.Remote2StopID['207 ST,1'] = '108'
		self.Remote2StopID['DYCKMAN ST,1AC'] = '109'
		self.Remote2StopID['DYCKMAN ST,1'] = '109'
		self.Remote2StopID['191 ST,1'] = '110'
		self.Remote2StopID['181 ST,1'] = '111'
		self.Remote2StopID['168 ST-BROADWAY,1AC'] = '112'
		self.Remote2StopID['157 ST,1'] = '113'
		self.Remote2StopID['145 ST,1'] = '114'
		self.Remote2StopID['137 ST-CITY COL,1'] = '115'
		self.Remote2StopID['125 ST,1'] = '116'
		self.Remote2StopID['116 ST-COLUMBIA,1'] = '117'
		self.Remote2StopID['110 ST-CATHEDRL,1'] = '118'
		self.Remote2StopID['103 ST,1'] = '119'
		self.Remote2StopID['96 ST,123'] = '120'
		self.Remote2StopID['86 ST,1'] = '121'
		self.Remote2StopID['79 ST,1'] = '122'
		self.Remote2StopID['72 ST,123'] = '123'
		self.Remote2StopID['66 ST-LINCOLN,1'] = '124'
		self.Remote2StopID['59 ST-COLUMBUS,1ABCD'] = '125'
		self.Remote2StopID['50 ST,1'] = '126'
		self.Remote2StopID['42 ST-TIMES SQ,1237ACENQRS'] = '127'
		self.Remote2StopID['34 ST-PENN STA,123'] = '128'
		self.Remote2StopID['28 ST,1'] = '129'
		self.Remote2StopID['23 ST,1'] = '130'
		self.Remote2StopID['18 ST,1'] = '131'
		self.Remote2StopID['14 ST,123FLM'] = '132'
		self.Remote2StopID['CHRISTOPHER ST,1'] = '133'
		self.Remote2StopID['HOUSTON ST,1'] = '134'
		self.Remote2StopID['CANAL ST,1'] = '135'
		self.Remote2StopID['FRANKLIN ST,1'] = '136'
		self.Remote2StopID['CHAMBERS ST,123'] = '137'
		self.Remote2StopID['CORTLANDT ST,1'] = '138'
		self.Remote2StopID['RECTOR ST,1'] = '139'
		self.Remote2StopID['SOUTH FERRY,R1'] = '142'
		self.Remote2StopID['PARK PLACE,23ACE'] = '228'
		self.Remote2StopID['FULTON ST,2345ACJZ'] = '229'
		self.Remote2StopID['WALL ST,23'] = '230'
		self.Remote2StopID['CLARK ST,23'] = '231'
		self.Remote2StopID['BOROUGH HALL/CT,2345R'] = '232'
		self.Remote2StopID['HOYT ST,23'] = '233'
		self.Remote2StopID['NEVINS ST,2345'] = '234'
		self.Remote2StopID['ATLANTIC AVE,2345BDNQR'] = '235'
		self.Remote2StopID['PACIFIC ST,BDNQR2345'] = '235'
		self.Remote2StopID['BERGEN ST,23'] = '236'
		self.Remote2StopID['GRAND ARMY PLAZ,23'] = '237'
		self.Remote2StopID['EASTERN PKWY,23'] = '238'
		self.Remote2StopID['FRANKLIN AVE,2345S'] = '239'
		self.Remote2StopID['NOSTRAND AVE,3'] = '248'
		self.Remote2StopID['KINGSTON AVE,3'] = '249'
		self.Remote2StopID['CROWN HTS-UTICA,34'] = '250'
		self.Remote2StopID['SUTTER AVE,3'] = '251'
		self.Remote2StopID['SARATOGA AVE,3'] = '252'
		self.Remote2StopID['ROCKAWAY AVE,3'] = '253'
		self.Remote2StopID['JUNIUS ST,3'] = '254'
		self.Remote2StopID['PENNSYLVANIA AV,3'] = '255'
		self.Remote2StopID['VAN SICLEN AVE,3'] = '256'
		self.Remote2StopID['NEW LOTS AVE,3'] = '257'
		self.Remote2StopID['PRESIDENT ST,25'] = '241'
		self.Remote2StopID['STERLING ST,25'] = '242'
		self.Remote2StopID['WINTHROP ST,25'] = '243'
		self.Remote2StopID['CHURCH AVE,25'] = '244'
		self.Remote2StopID['BEVERLY ROAD,25'] = '245'
		self.Remote2StopID['NEWKIRK AVE,25'] = '246'
		self.Remote2StopID['FLATBUSH AVE,25'] = '247'
		self.Remote2StopID['PELHAM BAY PARK,6'] = '601'
		self.Remote2StopID['BUHRE AVE,6'] = '602'
		self.Remote2StopID['MIDDLETOWN ROAD,6'] = '603'
		self.Remote2StopID['WESTCHESTER SQ,6'] = '604'
		self.Remote2StopID['ZEREGA AVE,6'] = '606'
		self.Remote2StopID['CASTLE HILL AVE,6'] = '607'
		self.Remote2StopID['E 177 ST-PARKCH,6'] = '608'
		self.Remote2StopID['ST LAWRENCE AVE,6'] = '609'
		self.Remote2StopID['MORRISON AVE,6'] = '610'
		self.Remote2StopID['ELDER AVE,6'] = '611'
		self.Remote2StopID['WHITLOCK AVE,6'] = '612'
		self.Remote2StopID['HUNTS POINT AVE,6'] = '613'
		self.Remote2StopID['LONGWOOD AVE,6'] = '614'
		self.Remote2StopID['E 149 ST,6'] = '615'
		self.Remote2StopID['E 143 ST,6'] = '616'
		self.Remote2StopID['CYPRESS AVE,6'] = '617'
		self.Remote2StopID['BROOK AVE,6'] = '618'
		self.Remote2StopID['138 ST-3 AVE,6'] = '619'
		self.Remote2StopID['WOODLAWN ROAD,4'] = '401'
		self.Remote2StopID['MOSHOLU PARKWAY,4'] = '402'
		self.Remote2StopID['BEDFORD PARK BL,4'] = '405'
		self.Remote2StopID['KINGSBRIDGE RD,4'] = '406'
		self.Remote2StopID['FORDHAM ROAD,4'] = '407'
		self.Remote2StopID['183 ST,4'] = '408'
		self.Remote2StopID['BURNSIDE AVE,4'] = '409'
		self.Remote2StopID['176 ST,4'] = '410'
		self.Remote2StopID['MT EDEN AVE,4'] = '411'
		self.Remote2StopID['170 ST,4'] = '412'
		self.Remote2StopID['167 ST,4'] = '413'
		self.Remote2StopID['161 ST-YANKEE,BD4'] = '414'
		self.Remote2StopID['149 ST-GR CONC,245'] = '415'
		self.Remote2StopID['138 ST-GR CONC,45'] = '416'
		self.Remote2StopID['125 ST,456'] = '621'
		self.Remote2StopID['116 ST,6'] = '622'
		self.Remote2StopID['110 ST,6'] = '623'
		self.Remote2StopID['103 ST,6'] = '624'
		self.Remote2StopID['96 ST,6'] = '625'
		self.Remote2StopID['86 ST,456'] = '626'
		self.Remote2StopID['77 ST,6'] = '627'
		self.Remote2StopID['68ST-HUNTER COL,6'] = '628'
		self.Remote2StopID['59 ST,456NQR'] = '629'
		self.Remote2StopID['LEXINGTON AVE,456NQR'] = '629'
		self.Remote2StopID['51 ST,6'] = '630'
		self.Remote2StopID['42 ST-GRD CNTRL,4567S'] = '631'
		self.Remote2StopID['33 ST,6'] = '632'
		self.Remote2StopID['28 ST,6'] = '633'
		self.Remote2StopID['23 ST,6'] = '634'
		self.Remote2StopID['14 ST-UNION SQ,LNQR456'] = '635'
		self.Remote2StopID['ASTOR PLACE,6'] = '636'
		self.Remote2StopID['BLEECKER ST,6DF'] = '637'
		self.Remote2StopID['SPRING ST,6'] = '638'
		self.Remote2StopID['CANAL ST,JNQRZ6'] = '639'
		self.Remote2StopID['BROOKLYN BRIDGE,456JZ'] = '640'
		self.Remote2StopID['BROOKLYN BRIDGE,JZ456'] = '640'
		self.Remote2StopID['FULTON ST,ACJZ2345'] = '418'
		self.Remote2StopID['WALL ST,45'] = '419'
		self.Remote2StopID['BOWLING GREEN,45'] = '420'
		self.Remote2StopID['BOROUGH HALL/CT,2345R'] = '423'
		self.Remote2StopID['WAKEFIELD-241,2'] = '201'
		self.Remote2StopID['NEREID AVE,25'] = '204'
		self.Remote2StopID['233 ST,25'] = '205'
		self.Remote2StopID['225 ST,25'] = '206'
		self.Remote2StopID['219 ST,25'] = '207'
		self.Remote2StopID['GUN HILL ROAD,25'] = '208'
		self.Remote2StopID['BURKE AVE,25'] = '209'
		self.Remote2StopID['ALLERTON AVE,25'] = '210'
		self.Remote2StopID['PELLHAM PARKWAY,25'] = '211'
		self.Remote2StopID['BRONX PARK EAST,25'] = '212'
		self.Remote2StopID['E 180 ST,25'] = '213'
		self.Remote2StopID['E TREMONT AVE,25'] = '214'
		self.Remote2StopID['174 ST,25'] = '215'
		self.Remote2StopID['FREEMAN ST,25'] = '216'
		self.Remote2StopID['SIMPSON ST,25'] = '217'
		self.Remote2StopID['INTERVALE-163,25'] = '218'
		self.Remote2StopID['PROSPECT AVE,25'] = '219'
		self.Remote2StopID['JACKSON AVE,25'] = '220'
		self.Remote2StopID['149 ST-3 AVE,25'] = '221'
		self.Remote2StopID['149 ST-GR CONC,245'] = '222'
		self.Remote2StopID['148 ST-LENOX,3'] = '301'
		self.Remote2StopID['145 ST,3'] = '302'
		self.Remote2StopID['135 ST,23'] = '224'
		self.Remote2StopID['125 ST,23'] = '225'
		self.Remote2StopID['116 ST,23'] = '226'
		self.Remote2StopID['110 ST-CPN,23'] = '227'
		self.Remote2StopID['DYRE AVE,5'] = '501'
		self.Remote2StopID['BAYCHESTER AVE,5'] = '502'
		self.Remote2StopID['GUN HILL ROAD,5'] = '503'
		self.Remote2StopID['PELHAM PARKWAY,5'] = '504'
		self.Remote2StopID['PELHAM PARKWAY,25'] = '504'
		self.Remote2StopID['MORRIS PARK,5'] = '505'
		self.Remote2StopID['MAIN ST,7'] = '701'
		self.Remote2StopID['METS-WILLETS PT,7'] = '702'
		self.Remote2StopID['111 ST,7'] = '705'
		self.Remote2StopID['103 ST-CORONA,7'] = '706'
		self.Remote2StopID['JUNCTION BLVD,7'] = '707'
		self.Remote2StopID['90 ST-ELMHURST,7'] = '708'
		self.Remote2StopID['82 ST-JACKSON H,7'] = '709'
		self.Remote2StopID['74 ST-BROADWAY,EFMR7'] = '710'
		self.Remote2StopID['69 ST-FISK AVE,7'] = '711'
		self.Remote2StopID['61 ST/WOODSIDE,7'] = '712'
		self.Remote2StopID['52 ST-LINCOLN,7'] = '713'
		self.Remote2StopID['46 ST-BLISS ST,7'] = '714'
		self.Remote2StopID['40 ST-LOWERY ST,7'] = '715'
		self.Remote2StopID['33 ST/RAWSON ST,7'] = '716'
		self.Remote2StopID['QUEENSBORO PLZ,7NQ'] = '718'
		#self.Remote2StopID[''] = 'R09'
		self.Remote2StopID['COURT SQ,7'] = '719'
		self.Remote2StopID['HUNTERS PT AVE,7'] = '720'
		self.Remote2StopID['VERNON/JACKSON,7'] = '721'
		self.Remote2StopID['42 ST-GRD CNTRL,4567S'] = '723'
		self.Remote2StopID['5 AVE-BRYANT PK,7BDFM'] = '724'
		self.Remote2StopID['42 ST-TIMES SQ,1237ACENQRS'] = '725'

		self.Remote2StopID['ST. GEORGE,1'] = 'S31'
		self.Remote2StopID['TOMPKINSVILLE,1'] = 'S30'
		#self.Remote2StopID[''] = 'S29'
		#self.Remote2StopID[''] = 'S28'
		#self.Remote2StopID[''] = 'S27'
		#self.Remote2StopID[''] = 'S26'
		#self.Remote2StopID[''] = 'S25'
		#self.Remote2StopID[''] = 'S24'
		#self.Remote2StopID[''] = 'S23'
		#self.Remote2StopID[''] = 'S22'
		#self.Remote2StopID[''] = 'S21'
		#self.Remote2StopID[''] = 'S20'
		#self.Remote2StopID[''] = 'S19'
		self.Remote2StopID['ELTINGVILLE PK,Z'] = 'S18'
		#self.Remote2StopID[''] = 'S17'
		#self.Remote2StopID[''] = 'S16'
		#self.Remote2StopID[''] = 'S15'
		#self.Remote2StopID[''] = 'S14'
		#self.Remote2StopID[''] = 'S13'
		#self.Remote2StopID[''] = 'S09'
		#self.Remote2StopID[''] = 'S11'
		

		#self.Remote2StopID[''] = '476'
		#self.Remote2StopID[''] = '477'
		#self.Remote2StopID[''] = '902'
		#self.Remote2StopID[''] = '902'









































