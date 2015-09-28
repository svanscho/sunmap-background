#!/usr/bin/env python

from appscript import app
from  datetime import datetime
import urllib2
import os
import uuid
import sh
import datetime

def removeOldPicture():
	try:
		sh.rm(sh.glob('/tmp/background-*.jpg'))
		#os.remove("/tmp/background.jpg")
	except:
		pass

def getCurrentUTCtime():
	now = datetime.utcnow()
	return now.strftime("%Y%m%dT%H%M")

def downloadImage(url,datestring):
	url=url+datestring
	response = urllib2.urlopen(url)
	filename = "/tmp/background-"+str(uuid.uuid4())+".jpg"
	f = open(filename,'wb')
	f.write(response.read())
	f.close()
	return filename

def shiftImageToLeft(filename,pixels):
	os.system(" ".join(["/usr/local/bin/convert	",filename,"-roll","-"+str(pixels),filename]))

try:
	removeOldPicture()
	
	#example url 1 (dynamic): http://www.timeanddate.com/scripts/sunmap.php?iso=20140929T0700
	#url = "http://www.timeanddate.com/scripts/sunmap.php?iso="
	#datestring = getCurrentUTCtime()
	
	#example urls (static): 
	url = "http://static.die.net/earth/mercator/1600.jpg"
	#url = "http://static.die.net/earth/mollweide/1600.jpg"
	#url = "http://static.die.net/earth/peters/1600.jpg"
	
	datestring = ""
	
	filename=downloadImage(url,datestring)
	
	#Australia centric map
	shiftImageToLeft(filename,650)

	se = app('System Events')
	desktops = se.desktops.display_name.get()
	for d in desktops:
		desk = se.desktops[d]
		desk.picture.set(filename)
		
except Exception as e:
	pass
