import csv
import datetime

class subwayHistorical:
	def __init__(self):
		self.loadRemote2Station()
		self.loadStation2nta()
		return

	def loadStation2nta(self):
		self.station2nta = {"242 ST": ["BX22"],
							"238 ST": ["BX22","BX29"],
							"231 ST": ["BX28", "BX29"],
							"MARBLE HILL-225": ["MN01"],
							"215 ST": ["MN01"],
							"207 ST": ["MN01"],
							"DYCKMAN ST": ["MN01"],
							"191 ST": ["MN01"],
							"181 ST": ["MN01", "MN35"],
							"168 ST-BROADWAY": ["MN36"],
							"157 ST": ["MN04"],
							"145 ST": ["MN04", "MN06"],
							"137 ST-CITY COL": ["MN06"],
							"125 ST": ["MN06", "MN09"],
							"116 ST-COLUMBIA": ["MN09"],
							"110 ST": ["MN09"],
							"103 ST": ["MN12"],
							"96 ST": ["MN12"],
							"86 ST": ["MN12"],
							"79 ST": ["MN12"],
							"72 ST": ["MN14"],
							"66 ST-LINCOLN": ["MN14"],
							"59 ST-CLINTON": ["MN14", "MN15", "MN17"],
							"50 ST": ["MN17"],
							"42 ST-TIMES SQ": ["MN17"],
							"34 ST-PENN STA": ["MN17", "MN13"],
							"28 ST": ["MN13"],
							"23 ST": ["MN13"],
							"18 ST": ["MN13"],
							"14 ST": ["MN13", "MN23"],
							"CHRISTOPHER ST": ["MN23"],
							"HOUSTON ST": ["MN24"]}


	def loadRemote2Station(self):
		self.remote2station = {}
		filename = 'TurnstileData/Remote-Booth-Station-2.csv'
		with open (filename, 'rb') as csvfile:
			data = [row for row in csv.reader(csvfile.read().splitlines())]
			reader = data
			i = True
			for row in reader:
				if i:
					i = False
					continue
				else:
					remote = row[0]
					booth = row[1]
					station = row[2]
					if booth not in self.remote2station:
						self.remote2station[booth] = station

	def loadTurnstile(self, turnstileFile):
		ntaDictionary = {}
		timeSeriesDataEntries = {}
		timeSeriesDataExits = {}
		boothNTAs = {}
		with open (turnstileFile, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			i = True
			for row in reader: 
				if i: #skip the first line
					i = False
					continue
				else:
					booth = row[0]
					unit = row[1]
					stationName = row[3]
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
					index = diff.seconds / 3600 / 4
					entries = row[9]
					exits = row[10]
					if booth not in self.remote2station:
						continue
					station = self.remote2station[booth]
					if station not in self.station2nta:
						continue
					nta = self.station2nta[station]

					if booth not in timeSeriesDataEntries:
						timeSeriesDataEntries[booth] = [0] * 42
						timeSeriesDataExits[booth] = [0] * 42
						boothNTAs[booth] = nta
					timeSeriesDataEntries[booth][index] = int(entries)
					timeSeriesDataExits[booth][index] = int(exits)

		for booth in timeSeriesDataEntries:
			nta = boothNTAs[booth]
			for n in nta:
				if n not in ntaDictionary:
					ntaDictionary[n] = [0] * 41
				for i in range(len(timeSeriesDataEntries[booth])-1):
					ntaDictionary[n][i] += (int(timeSeriesDataEntries[booth][i+1]) - int(timeSeriesDataEntries[booth][i]))/len(nta)
					ntaDictionary[n][i] -= (int(timeSeriesDataExits[booth][i+1]) - int(timeSeriesDataExits[booth][i]))/len(nta)
		return ntaDictionary



S = subwayHistorical()
#S.loadTurnstile('TurnstileData/turnstile_180811.csv')