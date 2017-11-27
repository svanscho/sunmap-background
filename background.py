#!/usr/bin/env python

from appscript import app
from  datetime import datetime
import urllib2
import os
import uuid
import sh
import datetime
from pytz import timezone
import pytz
from datetime import datetime, timedelta
import time

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
	#url=url+datestring
	response = urllib2.urlopen(url)
	filename = "/tmp/background-"+str(uuid.uuid4())+".jpg"
	f = open(filename,'wb')
	f.write(response.read())
	f.close()
	return filename

def shiftImageToLeft(filename,pixels):
	os.system(" ".join(["/usr/local/bin/convert	",filename,"-roll","-"+str(pixels),filename]))

def annotateImageWithTimestamps(filename):
	utc = timezone('UTC')
	pst = timezone('US/Pacific-New')
	europe = timezone('Europe/Amsterdam')
	sydney = timezone('Australia/Sydney')
	fmt = '%d-%m-%Y %H:%M'
	now = utc.localize(datetime.utcnow())
	pst_time = now.astimezone(pst).strftime(fmt)
	europe_time = now.astimezone(europe).strftime(fmt)
	sydney_time = now.astimezone(sydney).strftime(fmt)
	os.system(" ".join(["/usr/local/bin/convert     ",filename,"-undercolor '#00000080'","-fill white   -annotate +220+275 ","'"+pst_time+"'",filename]))
	os.system(" ".join(["/usr/local/bin/convert     ",filename,"-undercolor '#00000080'","-fill white   -annotate +780+225 ","'"+europe_time+"'",filename]))
	os.system(" ".join(["/usr/local/bin/convert     ",filename,"-undercolor '#00000080'","-fill white   -annotate +1350+575 ","'"+sydney_time+"'",filename]))

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
	annotateImageWithTimestamps(filename)
	
	#Australia centric map
	shiftImageToLeft(filename,650)

	se = app('System Events')
	desktops = se.desktops.display_name.get()
	for d in desktops:
		desk = se.desktops[d]
		desk.picture.set(filename)
		
except Exception as e:
	print e
