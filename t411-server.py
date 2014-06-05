#!/usr/bin/env python2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from ConfigParser import SafeConfigParser
import urllib, logger, re
import bencoded
config = SafeConfigParser()
config.read('config.ini')

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global config
        try:
            params = self.path.split("?")[1]
            url = "%s?%s" % ( config.get('account','tracker') ,params )
            url = re.sub("downloaded=\d+",'downloaded=0',url)

            response = urllib.urlopen(url)
            content = response.read()

            self.send_response( response.getcode())
            self.end_headers()
            self.wfile.write( content )

            self.processLogging(url)
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def processLogging(self,url):
        event = re.search('event=(\w+)&', url)
        if event:
            logger.print_info("event %s" % event.group(1))
        else:
            logger.print_info(url)
            


def main():
    try:
        server = HTTPServer(('', 16992), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

