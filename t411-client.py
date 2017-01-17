#!/usr/bin/env python2
from optparse import *
from t411api import *
from ConfigParser import *
import tempfile, bencoded,os,logger
import transmissionrpc,base64,sys,time
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

		group_search = OptionGroup(parser, "* Search torrents","Search torrent by keywords and category")
		group_search.add_option("-s", dest="search",help="Expected keywords")
		group_search.add_option('-c', dest="category", type='choice', 
				choices=['video', 'music', 'game', 'software'],help="video, music, game, software")
		parser.add_option_group(group_search)

		group_download = OptionGroup(parser, "* Download Torrent","Download torrent locally")
		group_download.add_option("-d", dest="download",help="Torrent id")
		group_download.add_option("-m", dest='mode', type='choice', default="local",
				choices=['local','transmission'],help="local, transmission")
		parser.add_option_group(group_download)

		(self.options, args) = parser.parse_args()

	def run(self):
		if self.options.search:
			self.processSearch()
		elif self.options.download:
			self.processDownload()

	def processSearch(self):
		tclient = T411API(self.config.get('account','username'),self.config.get('account','password'))
		torrents = tclient.search(self.options.search, self.options.category) 
		print "%8s %18s %70s %8s   %4s" % ("Id","Categorie","Title","Seeders","Size")
		print "-"*120
		for torrent in torrents:
			print "%8s %18s %70s %8s   %4s" % (torrent.tid,torrent.categoryname,torrent.name[:70],torrent.seeders, sizeof_fmt( torrent.size) )

	def processDownload(self):
		tclient = T411API(self.config.get('account','username'),self.config.get('account','password'))
		torrent_datas = tclient.download( self.options.download ) 

		if self.options.mode == 'local':
			self.processDownloadLocal(torrent_datas)
		elif self.options.mode == 'transmission':
			self.processDownloadTransmission(torrent_datas)


	def processDownloadLocal(self,torrent_datas):
		torrent_datas = torrent_replace_announce( torrent_datas, self.config.get('tracker','url') )

		tmp_filename = "%s/%s.torrent" % ( tempfile.gettempdir(),self.options.download )
		write_into_file( tmp_filename, torrent_datas )
		
		cmd =  self.config.get('global','torrent-client') % tmp_filename 
		logger.print_info("Lancement du torrent [ %s ] " % cmd)
		os.system(cmd)

	def processDownloadTransmission(self,torrent_datas):
		torrent_datas = torrent_replace_announce( torrent_datas, self.config.get('transmission','tracker') )

		logger.print_info('Connexion au server transmission ... ', eol='')
		tc = transmissionrpc.Client( self.config.get('transmission','host') ,
		 	port=self.config.get('transmission','port') ,
		 	user=self.config.get('transmission','username'),
		 	password=self.config.get('transmission','password'))
		logger.print_ok()

		logger.print_info("Upload du torrent ... ",eol='')
		torrent = tc.add_torrent(base64.b64encode(torrent_datas))
		logger.print_ok()

		torrent = tc.get_torrent(torrent.id)
		while torrent.progress < 100:
			sys.stdout.write('\r %.2f%% [%-100s] ' % ( torrent.progress, "="*int(torrent.progress)+">" ))
			sys.stdout.flush()
			torrent = tc.get_torrent(torrent.id)
			time.sleep(1)
		print '\r 100%% [%s]   '%('='*100)
		logger.print_success( 'Download complet' )
		tc.stop_torrent(torrent)

try:
	app = MainApp()
	app.run()
except NoSectionError,e:
	logger.print_error( "Invalid config.ini ( %s )" % e )
