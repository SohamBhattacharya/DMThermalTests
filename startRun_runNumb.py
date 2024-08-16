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

# file that contains last run number
last_run_number_file = '/home/cmsdaq/DAQ/DMThermalTests/lastRunNumber.txt'
log_dir = '/data1/DMQAQC/PRODUCTION/'
script_dir = '/home/cmsdaq/DAQ/DMThermalTests/'

# get last number from the txt and overwrite
def get_next_run_number():
    run_number = 1
    if os.path.exists(last_run_number_file):
        with open(last_run_number_file, 'r') as file:
            try:
                run_number = int(file.read().strip())
            except ValueError:
                pass    
    new_run_number = run_number + 1
    with open(last_run_number_file, 'w') as file:
        file.write(str(new_run_number))
    return new_run_number

new_run_number = get_next_run_number()

print("Now logging into ", log_dir, "run%04d.log"%int(new_run_number))

mykey = TXP3510P('/dev/TTi-3')
mykey_state = 0

proc = Popen(['python3','{}/read_PT1000.py'.format(script_dir),'--dev','/dev/ttyACM0','--log','%s/run%04d.log'%(log_dir,int(new_run_number))])
pid = proc.pid
print(pid)

timestamp_init = datetime.now() 

time.sleep(3)

while True:
    try:
        os.system('tail -n 1 %s/run%04d.log'%(log_dir,int(new_run_number)))
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
