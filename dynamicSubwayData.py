import web
from subwayStream import subwayStream

urls = ("/", "dynamicSubway")

class dynamicSubway:
	def __init__(self, borough=1):
		self.init(borough)
		self.borough = borough

	def init(self, borough=1):
		self.MTAstream = subwayStream()
		