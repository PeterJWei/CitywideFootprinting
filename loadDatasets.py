# >>> import csv
# >>> with open('eggs.csv', 'rb') as csvfile:
# ...     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
# ...     for row in spamreader:
# ...         print ', '.join(row)

import csv
with open('datasets/PLUTO_Manhattan.csv', 'rb') as csvfile:
	dataReader = csv.reader(csvfile, delimiter=',')
	for row in dataReader:
		for i in range(len(row)):
			print(str(i) + "," + row[i])
		break