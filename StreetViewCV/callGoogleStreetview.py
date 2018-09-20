import google_streetview.api
import google_streetview.helpers
import os
#'40.805816,-73.964647'
#'40.805721,-73.964426'#'40.805689,-73.964374'
locs = ['40.805269,-73.963270',
		'40.804993,-73.962609',
		'40.804684,-73.965822',
		'40.804440,-73.965221',
		'40.803985,-73.964121',
		'40.803961,-73.966218',
		'40.803717,-73.965521',
		'40.803278,-73.964411',
		'40.803371,-73.966664',
		'40.803160,-73.966031',
		'40.802583,-73.964819',
		'40.802778,-73.967142',
		'40.802421,-73.966321',
		'40.801995,-73.965270']

start = 1
cwd = os.getcwd()
for loc in locs:
	for heading,pitch in [('0','0'),('0','-90'),('0','90'),('90','0'),('180','0'),('270','0')]:

		params = [{
		'location':loc,
		'fov':'90',
		'heading':heading,
		'pitch':pitch,
		'key':'AIzaSyCGwNxMCXwsVRJNyy82x9G5MiXUGn_9Eb8'
		}]

		results = google_streetview.api.results(params)
		results.preview()
		results.download_links('streetviews')

		results.save_links('streetviews/links.txt')
		results.save_metadata('streetviews/metadata.json')

		os.rename(cwd+'/streetviews/gsv_0.jpg', cwd+'/streetviews/testImages_' + str(start) + '.jpg')
		start += 1