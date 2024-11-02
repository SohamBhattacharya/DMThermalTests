#!/usr/bin/env python3

import argparse
import os
import sys
import time
import subprocess
from subprocess import Popen, PIPE 
from optparse import OptionParser
from datetime import datetime 

sys.path.append(os.path.abspath("../TXP3510P/"))
from TXP3510PWrapper import TXP3510P

parser = argparse.ArgumentParser(
    description = "DM thermal test run",
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--dmid",
    required = True,
    type = str,
    help = "DM ID (barcode)"
)
args = parser.parse_args()


# file that contains last run number
log_dir = "/data/QAQC_DM"
last_run_number_file = f"{log_dir}/lastRunNumber.txt"
#script_dir = ("/home/cptlab1/Documents/BTL/DMThermalTests")
script_dir = os.getcwd()

os.system(f"mkdir -p {log_dir}")

# get last number from the txt and overwrite
def get_next_run_number():
    run_number = 0
    if os.path.exists(last_run_number_file):
        with open(last_run_number_file, "r") as file:
            try:
                run_number = int(file.read().strip())
            except ValueError:
                pass    
    new_run_number = run_number + 1
    with open(last_run_number_file, "w") as file:
        file.write(str(new_run_number))
    return new_run_number

new_run_number = get_next_run_number()

logfile = f"{log_dir}/run-{new_run_number:04d}_DM-{args.dmid}.log"

print(f"Starting to log: {logfile}")

mykey = TXP3510P("/dev/ttyACM2")
mykey_state = 0

proc = Popen([
    "python3",
    f"{script_dir}/read_PT1000.py",
    "--dev",
    "/dev/ttyACM0",
    "--log",
    logfile
])
pid = proc.pid
print(pid)

timestamp_init = datetime.now() 

time.sleep(3)

while True:
    try:
        command = "powershell -Command \"Get-Content -Path \'{0}\\run{1:04d}.log\' -Tail 1\""\
          .format(log_dir, int(new_run_number))
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

print("killing process %d"%pid)
os.system("kill -9 %d"%pid) 

mykey.setVoltage(0)
mykey.powerOff()

print(f"Finished logging: {logfile}")
