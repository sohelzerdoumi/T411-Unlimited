import json,urllib,urllib2
import logger 
from ConfigParser import SafeConfigParser


class T411Exception(Exception):
	pass

class T411API:
	URL      = "https://api.t411.me/"
	USERNAME = None
	PASSWORD = None
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
		json_response = self.__call_json("torrents/search/%s&cid=%s" % (keywords,catid), {'offset':'0', 'limit':'200'})
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
		logger.print_info("Download torrent ... ")
		return self.__call("torrents/download/%s" % tid)

	def details(self,tid):
		return self.__call_json("torrents/details/%s" % tid)

	def __init__(self):
		global config
		config = SafeConfigParser()
		config.read('config.ini')

		self.USERNAME = config.get('account','username')
		self.PASSWORD = config.get('account','password')
		
		if self.token == None:
			self.loadToken()

	def loadToken(self):
		logger.print_info("Authentification ... ",eol='')
		json_decode = self.__call_json('auth',{'username':self.USERNAME,'password':self.PASSWORD})
		self.token = json_decode['token']
		logger.print_ok()

	def __call_json(self,action,datas={}):
		response_json = json.loads( self.__call(action,datas) )
		if 'error' in response_json:
			raise T411Exception( response_json['error'] )
		return response_json

	def __call(self,action,datas={}):
		params 		= urllib.urlencode(datas)
		req 		= urllib2.Request(self.URL+action, params, headers={'Authorization': self.token})
		response 	= urllib2.urlopen(req).read()
		if 'error' in response:
			logger.print_error( json.loads(response)['error'] )	
			exit()	
		return response