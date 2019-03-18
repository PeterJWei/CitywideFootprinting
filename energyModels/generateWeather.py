import csv
from datetime import datetime
from datetime import date, timedelta
import time

class weather:
	def __init__(self, file):
		print("Loading weather data")
		start = time.time()
		self.weatherList = {}
		self.loadWeather(file)
		#self.saveDaily('daily.py')
		self.testDaily()
		end = time.time()
		print("Finished: " + str(end-start) + " s")
		print("Compiled weather data")

	def loadWeather(self, file):
		doRH = False
		cyear = None
		cmonth = None
		cday = None
		DPmax = None
		DPmin = None
		DPavg = 0
		DBmax = None
		DBmin = None
		DBavg = 0
		if doRH: RHmax = None
		if doRH: RHmin = None
		if doRH: RHavg = 0
		samples = 0
		with open(file, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			first = True
			for row in reader:
				# for i,label in enumerate(row):
				# 	print((i, label))
				if first:
					first = not first
					continue
				f = "%Y-%m-%dT%H:%M:%S"
				dt = datetime.strptime(row[1], f)
				if cyear is not None and cday != dt.day:
					self.weatherList[(cyear, cmonth, cday)] = (DPmax, DPmin, DPavg, 
						DBmax, DBmin, DBavg, samples)
					#self.weatherList.append([cyear, cmonth, cday, DPmax, DPmin, DPavg/samples, 
						#DBmax, DBmin, DBavg/samples])#, RHmax, RHmin, RHavg/samples])
				if cyear is None or cday != dt.day:
					DPmax = None
					DPmin = None
					DPavg = 0
					DBmax = None
					DBmin = None
					DBavg = 0
					if doRH: RHmax = None
					if doRH: RHmin = None
					if doRH: RHavg = 0
					samples = 0
					cyear = dt.year
					cmonth = dt.month
					cday = dt.day

				try:
					DP = float(row[42])
					DB = float(row[43])
					#RH = float(row[44])
				except ValueError:
					#print((row[42], row[43], DP, DB))
					continue
				DPmax = DP if (DPmax is None or DPmax < DP) else DPmax
				DPmin = DP if (DPmin is None or DPmin > DP) else DPmin
				DPavg += DP
				DBmax = DB if (DBmax is None or DBmax < DB) else DBmax
				DBmin = DB if (DBmin is None or DBmin > DB) else DBmin
				DBavg += DB
				if doRH: RHmax = RH if (RHmax is None or RHmax < RH) else RHmax
				if doRH: RHmin = RH if (RHmin is None or RHmin > RH) else RHmin
				if doRH: RHavg += RH
				samples += 1
				#print((dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second))
				#self.weatherList.append((dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, DPTemp, DBTemp, RH))

	def testDaily(self):
		startDate = date(2010, 1, 1)
		endDate = date(2019, 3, 3)
		delta = endDate - startDate
		for i in range(delta.days + 1):
			newDate = startDate + timedelta(i)
			if (newDate.year, newDate.month, newDate.day) not in self.weatherList:
				print((newDate.year, newDate.month, newDate.day))

	def saveDaily(self, file):
		with open(file, mode='w') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in self.weatherList:
				writer.writerow(row)
			#writer.writerow()

