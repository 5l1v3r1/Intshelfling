import RPi.GPIO as GPIO
import time
import re
import sys
import urllib2
import requests
from hx711 import HX711
from numpy import median

class Line :
	def __init__(self,id,quan,weight,quan_max):
		self.id = id
		self.weight = weight
		self.quan = quan
		self.quan_max=quan_max

def cleanAndExit():
	print "Cleaning..."
	GPIO.cleanup()
	print "Bye!"
	sys.exit()

contents = urllib2.urlopen("http://intshelf.azurewebsites.net/api/info").read()
contents= contents.translate(None, '"')
values = contents.split('},')

for i,itr in enumerate(values):
	print(itr)
	val=itr.split(',')
	vals=[]
	for index,v in enumerate(val):
		vals.append(v.split(":")[1])

	lines=[]
	for idx in range(6):
		lines.append(Line(vals[1],vals[2],vals[3],vals[4]))

	for idx in range(6):
		lines[idx]=(Line(vals[1],vals[2],vals[3],vals[4]))
	
for obj in lines:
	print(obj.id)
	print(obj.weight)
