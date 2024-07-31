#! /usr/bin/python

import serial
import time
import logging

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-d","--dev")
parser.add_option("-l","--log")
(options,args)=parser.parse_args()

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S',filename=options.log,level=logging.DEBUG)

port = options.dev

try:
    ser = serial.Serial(port, 115200)
    ser.timeout = 5
except serial.serialutil.SerialException:
    #no serial connection
    logging.warning('not possible to establish connection with '+str(port))
    self.ser = None
else:
    print('Starting connection with '+str(port))
    #logging.info('Starting connection with '+str(port))

command = '1'

while True:
    time.sleep(0.5)
    
    #print('reading...')

    data = ser.readline()[:-2] #the last bit gets rid of the new-line chars
    #if data:
    # 	print(data)

    x = ser.write(('1\r\n').encode())
    out = ''
    # let's wait one second before reading output (let's give device time to answer)
    time.sleep(1)

    line = ser.readline()   # read a byte string
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        string = string[:-1]
        out += string
    
    #while ser.inWaiting() > 0:
    #    out += str(ser.read(1))
        
    if out != '':
        logging.info(out.rstrip().lstrip(' '))

ser.close()
