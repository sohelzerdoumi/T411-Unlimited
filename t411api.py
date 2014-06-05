import json,urllib,urllib2
import logger 
from ConfigParser import SafeConfigParser


config = SafeConfigParser()
config.read('config.ini')

class T411API:
	URL      = "https://api.t411.me/"
	USERNAME = config.get('account','username')
	PASSWORD = config.get('account','password')
	CATEGORY = {
		'video'		:'210',
		'music'		:'623',
		'game'		:'246',
		'software' 	:'391'
	}

	token = None

	def search(self,keywords,category=210):
		if category in self.CATEGORY:
			catid = self.CATEGORY[ category ]
		else:
			catid = 210
		
		response = []
		logger.print_info("Recherche en cours ...",eol='')
		json_response = json.loads(self.__call("torrents/search/%s&cid=%s" % (keywords,catid), {'offset':'0', 'limit':'200'}))
		logger.print_ok()

		for torrent in json_response['torrents']:
			item 		= type('Torrent', (object,), { "id": None, "name": None, "seeders":None,"size":None })
			item.id 	= torrent['id']
			item.title 	= torrent['name']
			item.seeders = torrent['seeders']
			item.size 	= torrent['size']
			response.append(item)

		return response

	def download(self,tid):
		return self.__call("torrents/download/%s" % tid)

	def details(self,tid):
		return json.loads(self.__call("torrents/details/%s" % tid))

	def __init__(self):
		if self.token == None:
			self.loadToken()

	def loadToken(self):
		logger.print_info("Authentification ... ",eol='')
		json_decode = json.loads(self.__call('auth',{'username':self.USERNAME,'password':self.PASSWORD}))
		self.token = json_decode['token']
		logger.print_ok()
	def __call(self,action,datas={}):
		params 		= urllib.urlencode(datas)
		req 		= urllib2.Request(self.URL+action, params, headers={'Authorization': self.token})
		response 	= urllib2.urlopen(req)
		return response.read()