import DBMgr
import argparse
import datetime
import calendar
import csv

db = DBMgr.DBMgr()

csvFilePath = "exampleBuildingFootprints/buildingFootprint1.csv"

def main():
	args = parser.parse_args()
	minutes = args.minutes
	user = args.user
	if minutes > 0:
		print("Minutes: " + str(minutes))
		minutes = 100
	start = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
	start = calendar.timegm(start.utctimetuple())
	end = calendar.timegm(datetime.datetime.now().utctimetuple())
	print("Querying database for footprint...")
	D = db.getBuildingFootprintData(start, end)
	print("Received footprint data")

	keys = D.keys()
	timestamps = D["timestamp"]
	if "timestamp" in keys:
		keys.remove("timestamp")
	else:
		print("No Timestamp!")

	with open(csvFilePath, mode='w') as csvFile:
		csvWriter = csv.writer(csvFile, delimiter=',')
		for i in range(len(timestamps)):
			row = []
			row.append(timestamps[i])
			for key in keys:
				row.append(D[key][i])
			csvWriter.writerow(row)
	print("Script complete")


if __name__ == "__main__":
	print("Running Main...")
	parser = argparse.ArgumentParser(description='Pull footprint from database.')
	parser.add_argument('--minutes', type=int, default=10)
	main()