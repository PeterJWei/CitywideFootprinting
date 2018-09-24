import urllib2
import time
for i in range(100,200):
	f = open('cameraTrainingStills/pic' + str(i) + '.jpg', 'wb')
	f.write(urllib2.urlopen('http://207.251.86.238/cctv303.jpg?math=0.29673863811952195').read())
	f.close()
	time.sleep(1)