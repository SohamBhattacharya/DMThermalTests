#!/usr/bin/env python3

import matplotlib
# matplotlib.use("Agg")  # Use the "Agg" backend for non-interactive plotting
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from time import sleep, strftime, time
from datetime import datetime
import sys
import argparse
import os
# import ROOT
import numpy as np


parser = argparse.ArgumentParser(
    description = "DM thermal test plot",
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--run",
    required = True,
    type = int,
    help = "Run number"
)
parser.add_argument(
    "--dmid",
    required = True,
    type = str,
    help = "DM ID (barcode)"
)
parser.add_argument(
    "--batch",
    required = False,
    action = "store_true",
    help = "Batch mode; will not display interactive plots"
)
parser.add_argument(
    "--logdir",
    required = False,
    type = str,
    default = "/data/QAQC_DM",
    help = "Directory with the temperature logs"
)
parser.add_argument(
    "--plotdir",
    required = False,
    type = str,
    default = "/data/QAQC_DM",
    help = "Directory to save plots in"
)
parser.add_argument(
    "--offset",
    required = False,
    action = "store_true",
    help = "Will do offset correction"
)



args = parser.parse_args()

log_dir = args.logdir
plot_dir = args.plotdir

file = f"run-{args.run:04d}_DM-{args.dmid}.log"
plot_file = f"{plot_dir}/{os.path.splitext(file)[0]}.png"

graph_file = f"{plot_dir}/{os.path.splitext(file)[0]}.root"

file = f"{log_dir}/{file}"

os.system(f"mkdir -p {plot_dir}")

nPointsOffset = 5

if (not args.batch) :
    
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


# draw function ---file
def graph():
    # plt.clf()
    # axes = plt.gca()
    
    title = f"DM {args.dmid}"
    
    plt.figure(figsize=(10, 10)) 
    plt.subplot(211)
    plt.plot(mysecs,TCopperL,color="black",linestyle="dotted",label="Copper left")
    plt.plot(mysecs,TCopperR,color="black",linestyle="dashed",label="Copper right") 
    plt.plot(mysecs,TTopL,color="red",label="Top left")
    plt.plot(mysecs,TTopR,color="orange",label="Top right")
    plt.plot(mysecs,TBottomL,color="blue",label="Bottom left")
    plt.plot(mysecs,TBottomR,color="green",label="Bottom right")
    plt.xlabel("Time elapsed [min]")
    plt.ylabel("Temperature [°C]")
    plt.grid()
    plt.ylim([5, 50])
    plt.legend(loc="upper left", fontsize="small", shadow=True, title = title)

    
    plt.subplot(212)
    plt.plot(mysecs,DeltaTTopL,color="red",label="Top left")
    plt.plot(mysecs,DeltaTTopR,color="orange",label="Top right")
    plt.plot(mysecs,DeltaTBottomL,color="blue",label="Bottom left")
    plt.plot(mysecs,DeltaTBottomR,color="green",label="Bottom right")
    plt.xlabel("Time elapsed [min]")
    plt.ylabel("ΔT [°C]")
    plt.grid()
    plt.ylim([-35, 5])
    plt.legend(loc="upper right", fontsize="small", shadow=True, title = title)
    plt.text(0,-22, f"max ΔT [°C] = {DeltaTTopLMin:.2f}, {DeltaTTopLMin-DeltaTAvg:.2f} wrt avg", color="red")
    plt.text(0,-24, f"max ΔT [°C] = {DeltaTTopRMin:.2f}, {DeltaTTopRMin-DeltaTAvg:.2f} wrt avg", color="orange")
    plt.text(0,-26, f"max ΔT [°C] = {DeltaTBottomLMin:.2f}, {DeltaTBottomLMin-DeltaTAvg:.2f} wrt avg", color="blue")
    plt.text(0,-28, f"max ΔT [°C] = {DeltaTBottomRMin:.2f}, {DeltaTBottomRMin-DeltaTAvg:.2f} wrt avg", color="green")
    plt.text(0,-30, f"avg(max ΔT) [°C] = {DeltaTAvg:.2f}", color="magenta")

    plt.tight_layout()
    # plt.show()
    
    plt.savefig(plot_file)
    #plt.close()
    
    print()
    print(f"Produced plot: {plot_file}")

    #save TGraphs 
    # n = len(mysecs)
    # output_file = ROOT.TFile(graph_file)
    # gDeltaTTopL = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTTopL))
    # gDeltaTTopR = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTTopR))
    # gDeltaTBottomL = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTBottomL))
    # gDeltaTBottomR = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTBottomR))
    # gDeltaTTopL.Write("g_DeltaTTopL_module_{}".format(dm))
    # gDeltaTTopR.Write("g_DeltaTTopR_module_{}".format(dm))
    # gDeltaTBottomL.Write("g_DeltaTBottomL_module_{}".format(dm))
    # gDeltaTBottomR.Write("g_DeltaTBottomR_module_{}".format(dm))
    # output_file.Close()


    if (not args.batch) :
        
        plt.show(block = True)



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
DeltaTAvg = 999.

# reading log file
it = 0
with open(str(file), "r") as fin:
    #for line in fin.readlines() [-200]:
    for line in fin.readlines():
        readings = line.strip().replace(",", " ").split()
        if len(readings) != 8:
            continue
        
        mytime.append(datetime.strptime(readings[0]+" "+readings[1], "%Y-%m-%d %H:%M:%S"))
        if len(mysecs) == 0:
            mysecs.append(0)
        else:
            mysecs.append((mytime[-1]-mytime[0]).total_seconds()/60.)        
        
        # TCopperR.append(float(readings[2]))
        # TCopperL.append(float(readings[3]))
        # TTopL.append(float(readings[4]))
        # TTopR.append(float(readings[5]))
        # TBottomL.append(float(readings[6]))
        # TBottomR.append(float(readings[7]))
        
        # TCopperR.append(float(readings[4+2]))
        # TCopperL.append(float(readings[5+2]))
        # TTopL.append(float(readings[1+2]))
        # TTopR.append(float(readings[2+2]))
        # TBottomL.append(float(readings[0+2]))
        # TBottomR.append(float(readings[3+2]))

        TCopperL.append(float(readings[4+2]))
        TCopperR.append(float(readings[5+2]))
        TTopL.append(float(readings[3+2]))
        TTopR.append(float(readings[0+2]))
        TBottomL.append(float(readings[2+2]))
        TBottomR.append(float(readings[1+2]))

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
        if it >= nPointsOffset and args.offset:
            offset = TTopLOffset - TCopperLOffset
            #print(offset)
            #offset = 0.
        DeltaTTopL.append( TTopL[-1]-TCopperL[-1]-offset )
        if (TTopL[-1]-TCopperL[-1]-offset) < DeltaTTopLMin:
            DeltaTTopLMin = (TTopL[-1]-TCopperL[-1]-offset)

        if it >= nPointsOffset and args.offset:
            offset = TTopROffset - TCopperROffset
            #print(offset)
            #offset = 0.
        DeltaTTopR.append( TTopR[-1]-TCopperR[-1]-offset )
        if (TTopR[-1]-TCopperR[-1]-offset) < DeltaTTopRMin:
            DeltaTTopRMin = (TTopR[-1]-TCopperR[-1]-offset)

        if it >= nPointsOffset and args.offset:
            offset = TBottomLOffset - TCopperLOffset
            #print(offset)
            #offset = 0.
        DeltaTBottomL.append( TBottomL[-1]-TCopperL[-1]-offset )
        if (TBottomL[-1]-TCopperL[-1]-offset) < DeltaTBottomLMin:
            DeltaTBottomLMin = (TBottomL[-1]-TCopperL[-1]-offset)

        if it >= nPointsOffset and args.offset:
            offset = TBottomROffset - TCopperROffset
            #print(offset)
            #offset = 0.
        DeltaTBottomR.append( TBottomR[-1]-TCopperR[-1]-offset )
        if (TBottomR[-1]-TCopperR[-1]-offset) < DeltaTBottomRMin:
            DeltaTBottomRMin = (TBottomR[-1]-TCopperR[-1]-offset)
        
        arr_DeltaT = np.array([DeltaTTopLMin, DeltaTTopRMin, DeltaTBottomLMin, DeltaTBottomRMin])
        DeltaTAvg = np.average(arr_DeltaT)
        

        print(str(readings[1])+" "+str(readings[2])+" "+str(readings[3])+" "+str(readings[4])+" "+str(readings[5])+" "+str(readings[6])+" "+str(readings[7]))
        
        it += 1

graph()
# input("ok?")
