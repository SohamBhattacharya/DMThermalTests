#! /usr/bin/python3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from time import sleep, strftime, time
from datetime import datetime
import sys
import argparse
import os

# define dm
file=sys.argv[1]

nPointsOffset = 5


plt.ion()

mytime = []
mysecs = []
TCopperR= []
TCopperL= []
TTopL= []
TTopR= []
TBottomL= []
TBottomR= []
DeltaTTopL= []
DeltaTTopR= []
DeltaTBottomL= []
DeltaTBottomR= []



# draw function ---
def graph():
    plt.clf()
    axes = plt.gca()
    plt.subplot(211)
    plt.plot(mysecs,TCopperL,color='black',linestyle='dotted',label='copper left')
    plt.plot(mysecs,TCopperR,color='black',linestyle='dashed',label='copper right')
    plt.plot(mysecs,TTopL,color='red',label='top left')
    plt.plot(mysecs,TTopR,color='orange',label='top right')
    plt.plot(mysecs,TBottomL,color='blue',label='bottom left')
    plt.plot(mysecs,TBottomR,color='green',label='bottom right')
    plt.xlabel("time elapsed [min.]")
    plt.ylabel("temperature [C]")
    plt.grid()
    plt.ylim([15.,50.])
    plt.legend()
    plt.subplot(212)
    plt.plot(mysecs,DeltaTTopL,color='red',label='top left')
    plt.plot(mysecs,DeltaTTopR,color='orange',label='top right')
    plt.plot(mysecs,DeltaTBottomL,color='blue',label='bottom left')
    plt.plot(mysecs,DeltaTBottomR,color='green',label='bottom right')
    plt.xlabel("time elapsed [min.]")
    plt.ylabel("Delta T [C]")
    plt.grid()
    plt.ylim([-30.,3.])
    plt.legend()
    plt.text(0.15,-10,'max. $\Delta$T = %.2f C'%DeltaTTopLMin, color='red')
    plt.text(0.15,-11,'max. $\Delta$T = %.2f C'%DeltaTTopRMin, color='orange')
    plt.text(0.15,-12,'max. $\Delta$T = %.2f C'%DeltaTBottomLMin, color='blue')
    plt.text(0.15,-13,'max. $\Delta$T = %.2f C'%DeltaTBottomRMin, color='green')
    plt.show()



TCopperROffset = 0.
TCopperLOffset = 0.
TTopLOffset = 0.
TTopROffset = 0.
TBottomLOffset = 0.
TBottomROffset = 0.

DeltaTTopLMin = 999.
DeltaTTopRMin = 999.
DeltaTBottomLMin = 999.
DeltaTBottomRMin = 999.

# reading log file
it = 0
with open(str(file), 'r') as fin:
    #for line in fin.readlines() [-200]:
    for line in fin.readlines():
        readings = line.strip().split()
        if len(readings) != 8:
            continue;
        
        mytime.append(datetime.strptime(readings[0]+" "+readings[1], "%Y-%m-%d %H:%M:%S"))
        if len(mysecs) == 0:
            mysecs.append(0)
        else:
            mysecs.append((mytime[-1]-mytime[0]).total_seconds()/60.)        
        
        TCopperR.append(float(readings[2]))
        TCopperL.append(float(readings[3]))
        TTopL.append(float(readings[4]))
        TTopR.append(float(readings[5]))
        TBottomL.append(float(readings[6]))
        TBottomR.append(float(readings[7]))

        # calibration points        
        if it < nPointsOffset:
            TCopperROffset += TCopperR[-1]
            TCopperLOffset += TCopperL[-1]
            TTopLOffset += TTopL[-1]
            TTopROffset += TTopR[-1]
            TBottomLOffset += TBottomL[-1]
            TBottomROffset += TBottomR[-1]
            
        elif it == nPointsOffset:
            TCopperROffset /= nPointsOffset
            TCopperLOffset /= nPointsOffset
            TTopLOffset /= nPointsOffset
            TTopROffset /= nPointsOffset
            TBottomLOffset /= nPointsOffset
            TBottomROffset /= nPointsOffset
        
        offset = 0.
        

        # correcting temperatures for T offset
        if it >= nPointsOffset:
            offset = TTopLOffset - TCopperLOffset
            #offset = 0.
        DeltaTTopL.append( TTopL[-1]-TCopperL[-1]-offset )
        if (TTopL[-1]-TCopperL[-1]-offset) < DeltaTTopLMin:
            DeltaTTopLMin = (TTopL[-1]-TCopperL[-1]-offset)
        
        if it >= nPointsOffset:
            offset = TTopROffset - TCopperROffset
            #offset = 0.
        DeltaTTopR.append( TTopR[-1]-TCopperR[-1]-offset )
        if (TTopR[-1]-TCopperR[-1]-offset) < DeltaTTopRMin:
            DeltaTTopRMin = (TTopR[-1]-TCopperR[-1]-offset)
        
        if it >= nPointsOffset:
            offset = TBottomLOffset - TCopperLOffset
            #offset = 0.
        DeltaTBottomL.append( TBottomL[-1]-TCopperL[-1]-offset )
        if (TBottomL[-1]-TCopperL[-1]-offset) < DeltaTBottomLMin:
            DeltaTBottomLMin = (TBottomL[-1]-TCopperL[-1]-offset)
        
        if it >= nPointsOffset:
            offset = TBottomROffset - TCopperROffset
            #offset = 0.
        DeltaTBottomR.append( TBottomR[-1]-TCopperR[-1]-offset )
        if (TBottomR[-1]-TCopperR[-1]-offset) < DeltaTBottomRMin:
            DeltaTBottomRMin = (TBottomR[-1]-TCopperR[-1]-offset)
        
        print(str(readings[1])+" "+str(readings[2])+" "+str(readings[3])+" "+str(readings[4])+" "+str(readings[5])+" "+str(readings[6])+" "+str(readings[7]))
        
        it += 1

graph()
input('ok?')
