#! /usr/bin/python3

import os
import sys
import time
import subprocess
from subprocess import Popen, PIPE 
from optparse import OptionParser
from datetime import datetime 

sys.path.append("/home/cmsdaq/DAQ/TXP3510P/")
from TXP3510PWrapper import TXP3510P



parser = OptionParser()
parser.add_option("-r","--run")
(options,args)=parser.parse_args()

mykey = TXP3510P('/dev/TTi-3')
mykey_state = 0

proc = Popen(['python3','/home/cmsdaq/DAQ/DMThermalTests/read_PT1000.py','--dev','/dev/ttyACM5','--log','run%04d.log'%int(options.run)])
pid = proc.pid
print(pid)

timestamp_init = datetime.now() 

time.sleep(3)

while True:
    try:
        os.system('tail -n 1 run%04d.log'%int(options.run)) 
        time.sleep(2)
        
        timestamp_curr = datetime.now()
        time_elapsed = float((timestamp_curr - timestamp_init).total_seconds())
        if time_elapsed > 30. and time_elapsed < 270. and mykey_state == 0:
            mykey.setVoltage(20.)
            mykey.setCurrent(0.25)
            mykey.powerOn()
            mykey_state = 1
        
        if time_elapsed > 270.:
            if mykey_state != 0:
                mykey.setVoltage(0.)
                mykey.powerOff()
                mykey_state = 0
        
        if time_elapsed > 300.:
            break
    
    except KeyboardInterrupt:
        break

print('killing process %d'%pid)
os.system('kill -9 %d'%pid) 

mykey.setVoltage(0)
mykey.powerOff()
