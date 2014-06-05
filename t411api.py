import json,urllib,urllib2
import logger 


class T411Exception(Exception):
	pass

class Torrent:
	"""
		Represent a torrent
	"""
	tid 			= 0
	name 			= ""
	categoryname 	= ""
	seeders 		= 0
	size 			= 0

	def __init__(self,json_datas):
		self.tid = json_datas['id']
		self.name = json_datas['name']
		self.categoryname = json_datas['categoryname']
		self.seeders = json_datas['seeders']
		self.size = json_datas['size']

class T411API:
	"""
		API to interact with api.t411.me

	"""
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

	def search(self,keywords,category='210'):
		"""
			@param string keywords   
			@param string category

			@return array of Torrent 
		"""
		if category in self.CATEGORY:
			catid = self.CATEGORY[ category ]
		else:
			catid = '210'
		
		response = []
		logger.print_info("Recherche en cours ...",eol='')
		json_response = self.__call_json("torrents/search/%s&cid=%s" % (keywords,catid), {'offset':'0', 'limit':'200'})
		logger.print_ok()

		for torrent in json_response['torrents']:
			response.append( Torrent(torrent) )

		return response

	def download(self,tid):
		"""
			@param int tid : id of the expected torrent
			@return torrent data
		"""
		logger.print_info("Download torrent ... ",eol='')
		torrent = self.__call("torrents/download/%s" % tid)
		logger.print_ok()
		return torrent

	def details(self,tid):
		"""
			Return information about the torrent
			@param int tid : id of the expected torrent
		"""
		return self.__call_json("torrents/details/%s" % tid)

	def __init__(self,username,password):
		"""
			Initialized and authentificate it
			@param string username
			@param string password
		"""
		self.USERNAME = username 
		self.PASSWORD = password 
		
		if self.token == None:
			self.loadToken()

	def loadToken(self):
		"""
			Process Authentification
		"""
		logger.print_info("Authentification ... ",eol='')
		json_decode = self.__call_json('auth',{'username':self.USERNAME,'password':self.PASSWORD})
		self.token = json_decode['token']
		logger.print_ok()

	def __call_json(self,action,datas={}):
		"""
			execute HTTP request to the API and expect a json answer
			@param string action
			@param dict datas

			@return answer as json
		""" 
		return json.loads( self.__call(action,datas) )

	def __call(self,action,datas={}):
		"""
			execute HTTP request to the API
			@param string action
			@param dict datas

			@return answer body
		"""
		params 		= urllib.urlencode(datas)
		req 		= urllib2.Request(self.URL+action, params, headers={'Authorization': self.token})
		response 	= urllib2.urlopen(req).read()
		if '{"error"' in response:
			logger.print_error( json.loads(response)['error'] )	
			exit()	
		return response