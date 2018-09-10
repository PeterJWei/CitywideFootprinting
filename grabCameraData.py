import urllib2
f = open('pic.jpg', 'wb')
f.write(urllib2.urlopen('http://207.251.86.238/cctv303.jpg?math=0.29673863811952195').read())
f.close()