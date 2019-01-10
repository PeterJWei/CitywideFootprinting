#!/bin/bash

# x=/Users/peterwei/Desktop/testData/part-00001
# y=/Users/peterwei/Desktop/CitywideFootprinting/static/data/${x}.csv
# echo $y
baseDir=/Users/peterwei/Desktop/cuebiqData/
rm $baseDir*.gz
dest="/Users/peterwei/Desktop/CitywideFootprinting/static/data/"
echo $dest
for filename in $baseDir*; do
	b=`basename $filename`
	tmpName="$dest$b.csv";
	echo $tmpName;
	mv $filename $tmpName;
done



# mmv /Users/peterwei/Desktop/testData/* /Users/peterwei/Desktop/CitywideFootprinting/static/data/#1.csv