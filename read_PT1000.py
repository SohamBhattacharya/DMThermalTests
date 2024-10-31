#! /usr/bin/python

import serial
import sys
import time
import logging

from optparse import OptionParser

sys.path.append("/home/cptlab1/Documents/BTL/TXP3510P/")
from TXP3510PWrapper import TXP3510P

parser = OptionParser()
parser.add_option("-d","--dev")
parser.add_option("-l","--log")
(options,args)=parser.parse_args()

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',filename=options.log,level=logging.DEBUG)

port = options.dev

try:
    ser = serial.Serial(port, 115200)
    ser.timeout = 0.1
except serial.serialutil.SerialException:
    #no serial connection
    logging.warning('not possible to establish connection with '+str(port))
    self.ser = None
else:
    print('Starting connection with '+str(port))
    #logging.info('Starting connection with '+str(port))

command = '1'

mykey = TXP3510P("/dev/ttyACM2")

while True:
    # ser.write(('1\r\n').encode())
    time.sleep(0.5)
    # print(ser.readline())
    # print('reading...')

    current = mykey.getCurrent()
    voltage = mykey.getVoltage()

    data = ser.readline()[:-2] #the last bit gets rid of the new-line chars
    #if data:
    # 	print(data)

    x = ser.write(('1\r\n').encode())
    out = ''
    # let's wait one second before reading output (let's give device time to answer)
    time.sleep(1)

    line = ser.readline()   # read a byte string
    # print(line)
    if line:
        line = line.decode()  # convert the byte string to a unicode string
        # string = string[:-1]
        # out += string
        # print(line)
        out = " ".join(line.strip().split(",") + [str(current), str(voltage)])
    
    # print(out)
    #while ser.inWaiting() > 0:
    #    out += str(ser.read(1))
        
    if out:
        print(out)
        # logging.info(out.rstrip().lstrip(' '))
        logging.info(out.rstrip().lstrip(' '))

ser.close()
