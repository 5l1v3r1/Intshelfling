import RPi.GPIO as GPIO
import time
import re
import sys
import urllib2
import requests
import json
from hx711 import HX711
from numpy import median

def cleanAndExit():
	print "Cleaning..."
	GPIO.cleanup()
	print "Bye!"
	sys.exit()
	
class Line :
    
    def __init__(self,a_id,a_weight,a_quan,a_quan_max):
        self.id = a_id
        self.weight = a_weight
        self.quan = a_quan
        self.quan_max = a_quan_max

contents = urllib2.urlopen("http://intshelf.azurewebsites.net/api/info").read()

lines=[]

jvar=json.loads(contents)

for i in range(6):
    lines.append(Line(i+1,jvar[i]['Weight'],jvar[i]['Quantity'],jvar[i]['MaxQuantity']))


def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()
    
    
hx_tab=[None]*7

hx_tab[1]=HX711(5, 6)
hx_tab[2]=HX711(13,19)

hx = HX711(5, 6)
hx1 = HX711(13,19)

hx.set_reading_format("LSB", "MSB")
hx1.set_reading_format("LSB", "MSB")
hx.set_reference_unit(20)
hx1.set_reference_unit(20)

hx.reset()
hx.tare()
hx1.reset()
hx1.tare()

j_initialize=json.loads(urllib2.urlopen("http://intshelf.azurewebsites.net/api/info").read())


initial_weights=[]*6

for i in range(len(initial_weights)):
    initial_weights[i]=j_initialize[i]['Quantity']

w_1=j_initialize[0]['Quantity']


while True:
    try:
        contents = urllib2.urlopen("http://intshelf.azurewebsites.net/api/info").read()

        lines=[]
        
        valz=[None]*6

        jvar=json.loads(contents)

        for i in range(6):
            lines.append(Line(i+1,jvar[i]['Weight'],jvar[i]['Quantity'],jvar[i]['MaxQuantity']))
            
        for i in range(len(valz)):
            valz[i]=hx_tab[i].get_weight(5)
            valz[i]=abs(valz[i])
        
        val = hx.get_weight(5)
        val=abs(val)
        prt = "1. " + str(val)
        print (prt)
        
        print("Debugging: ")
        print(val/lines[0].weight)
        print(val)
        print(lines[0].weight)
        
        x1=round(val/lines[0].weight)
        
        x1=int(x1)
        
        print("Simple bedubging:")
        print(x1)
        
        for i in range(len(lines)):
            
        
        if x1>lines[0].quan:
            print("Sending up signal on line 1.")
            requests.get("http://intshelf.azurewebsites.net/api/up/1")
            ++w_1
        
        elif x1<lines[0].quan:
            print("Sending down signal on line 1.")
            requests.get("http://intshelf.azurewebsites.net/api/down/1")
            --w_1
        
        
        
        val = hx1.get_weight(5)
        prt = "2. " + str(val)
        print (prt)
        
        
        

        hx.power_down()
        hx1.power_down()
        hx.power_up()
        hx1.power_up()
        
        for i_hx in hx_tab:
            i_hx.power_down()
            i_hx.power_up()
        
        time.sleep(0.8)
            


        
        
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


    






