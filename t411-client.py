#!/usr/bin/env python2
from optparse import *
from t411api import *
from ConfigParser import SafeConfigParser
import tempfile, bencoded,os,logger
from utils import *

class MainApp:
	config = None
	options = None

	def __init__(self):
		self.config = SafeConfigParser()
		self.config.read('config.ini')
		self.setupOptions()

	def setupOptions(self):
		parser = OptionParser()

		group_search = OptionGroup(parser, "Search torrents","Search torrent by keywords and category")
		group_search.add_option("-s", dest="search",help="Expected keywords")
		group_search.add_option('-c', dest="category", type='choice', 
				choices=['video', 'music', 'game', 'software'],help="video, music, game, software")
		parser.add_option_group(group_search)

		group_download = OptionGroup(parser, "Download Torrent","Download torrent locally")
		group_download.add_option("-d", dest="download",help="Torrent id")
		parser.add_option_group(group_download)

		(self.options, args) = parser.parse_args()

	def run(self):
		if self.options.search:
			self.processSearch()
		elif self.options.download:
			self.processDownload()

	def processSearch(self):
		tclient = T411API()
		torrents = tclient.search(self.options.search, self.options.category) 
		print "%8s %70s %8s   %4s" % ("Id","Title","Seeders","Size")
		print "-"*100
		for torrent in torrents:
			print "%8s %70s %8s   %4s" % (torrent.id,torrent.title[:70],torrent.seeders, sizeof_fmt( torrent.size) )

	def processDownload(self):
		tclient = T411API()
		torrent_datas = tclient.download( self.options.download ) 
		torrent_datas = torrent_replace_announce( torrent_datas, self.config.get('tracker','url') )

		tmp_filename = "%s/%s.torrent" % ( tempfile.gettempdir(),self.options.download )
		write_into_file( tmp_filename, torrent_datas )
		
		logger.print_info("Lancement du torrent ... %s " % self.config.get('global','torrent-client'))
		os.system( self.config.get('global','torrent-client') % tmp_filename )

app = MainApp()
app.run()