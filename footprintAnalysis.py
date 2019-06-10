import DBMgr
import argparse
import datetime
import calendar
import csv

db = DBMgr.DBMgr()

csvFilePath = "exampleFootprints/footprint1.csv"

def main():
	args = parser.parse_args()
	days = args.days
	user = args.user
	if days > 0:
		print("Days: " + str(days))
		days = 100
	end = calendar.timegm(datetime.datetime.now().utctimetuple())
	start = end - datetime.timedelta(days=days)
	print("Querying database for footprint...")
	D = db.getFootprintData(user, start, end)
	print("Received footprint data")

	footprints = D["footprint"]
	timestamps = D["timestamps"]
	energies = D["energy"]

	with open(csvFilePath, mode='w') as csvFile:
		csvWriter = csv.writer(csvFile, delimiter=',')
		assert(len(footprints) == len(timestamps))
		assert(len(timestamps) == len(energies))
		for i in range(len(footprints)):
			csvWriter.writerow([timestamps[i], energies[i], footprints[i]])
	print("Script complete")


if __name__ == "main":
	parser = argparse.ArgumentParser(description='Pull footprint from database.')
	parser.add_argument('user', type=str, default="597C5E91-976D-48D9-8797-5004455EC7B5")
	parser.add_argument('days', type=int, default=10)
	main()