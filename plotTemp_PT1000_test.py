#! /usr/bin/python3
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive plotting
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from time import sleep, strftime, time
from datetime import datetime
import sys
import argparse
import os
import ROOT
import numpy as np
# data and plot paths
log_dir = '/data1/DMQAQC/PRODUCTION/'
plot_dir = '/data1/html/'+log_dir


# parser
parser = argparse.ArgumentParser(description='DM Thermal Tests: plotting')
parser.add_argument("-r",  "--runLog",   required=True, type=int, help="run number")
parser.add_argument("-m",  "--detectorModule",       required=True, type=int, help="detector module barcode")
args = parser.parse_args()

# define dm
#file=sys.argv[1]
file = '{}/run{:04d}.log'.format(log_dir,args.runLog)
dm = '{:05d}'.format(args.detectorModule)
dm = '321100400'+dm

print("dm ", dm)
print("file ", file)

# create plot folder
plot_dir = plot_dir+'/run{:04d}_module_{}'.format(args.runLog,dm)
plot_name = '{}/run{:04d}_module_{}_thermal_test.png'.format(plot_dir, args.runLog,dm)  
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)
else:
    print("plot dir already exists. check either run number or dm")
    #sys.exit()

print("plot dir ", plot_dir)
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
    plt.figure(figsize=(10, 10)) 
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
    plt.ylim([10.,50.])
    plt.legend(loc='upper right', fontsize='small', shadow=True)
    plt.subplot(212)
    plt.plot(mysecs,DeltaTTopL,color='red',label='top left')
    plt.plot(mysecs,DeltaTTopR,color='orange',label='top right')
    plt.plot(mysecs,DeltaTBottomL,color='blue',label='bottom left')
    plt.plot(mysecs,DeltaTBottomR,color='green',label='bottom right')
    plt.xlabel("time elapsed [min.]")
    plt.ylabel("Delta T [C]")
    plt.grid()
    plt.ylim([-30.,3.])
    plt.legend(loc='upper right', fontsize='small', shadow=True)
    plt.text(0.15,-22,'max. DeltaT = %.2f C'%DeltaTTopLMin, color='red')
    plt.text(0.15,-24,'max. DeltaT = %.2f C'%DeltaTTopRMin, color='orange')
    plt.text(0.15,-26,'max. DeltaT = %.2f C'%DeltaTBottomLMin, color='blue')
    plt.text(0.15,-28,'max. DeltaT = %.2f C'%DeltaTBottomRMin, color='green')

    plt.tight_layout()

    plt.savefig(plot_name)
    plt.close()
    
    #save TGraphs 
    n = len(mysecs)
    gDeltaTTopL = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTTopL))
    gDeltaTTopR = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTTopR))
    gDeltaTBottomL = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTBottomL))
    gDeltaTBottomR = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTBottomR))
    output_file = ROOT.TFile(log_dir+'/temperatures_run{:04d}_module_{}.root'.format(args.runLog,dm), 'RECREATE')
    gDeltaTTopL.Write('g_DeltaTTopL_module_{}'.format(dm))
    gDeltaTTopR.Write('g_DeltaTTopR_module_{}'.format(dm))
    gDeltaTBottomL.Write('g_DeltaTBottomL_module_{}'.format(dm))
    gDeltaTBottomR.Write('g_DeltaTBottomR_module_{}'.format(dm))
    output_file.Close()
    #plt.show()



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
#input('ok?')
