import bencoded

def write_into_file(filename,datas):
	f = open(filename, "w")
	f.write( datas  )
	f.close()

def torrent_replace_announce(torrent_datas,new_tracker):
	torrent_decoded = bencoded.decode(torrent_datas)
	torrent_decoded['announce'] = new_tracker
	return bencoded.encode(torrent_decoded)

def sizeof_fmt(num):
	num = int(num)
	for x in ['bytes','KB','MB','GB','TB']:
		if num < 1024.0:
			return "%3.1f %s" % (num, x)
		num /= 1024.0