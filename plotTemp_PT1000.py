#!/usr/bin/env python3

import matplotlib.pyplot as plt
from datetime import datetime
import argparse
import numpy
import os
import re
import ROOT
import numpy as np


class Formatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawTextHelpFormatter
): pass

parser = argparse.ArgumentParser(
    description = "DM thermal test plot",
    formatter_class = Formatter
)

parser.add_argument(
    "--run",
    required = False,
    type = int,
    help = "Run number"
)

parser.add_argument(
    "--dmid",
    required = False,
    type = str,
    help = "DM ID (barcode)"
)

parser.add_argument(
    "--logdir",
    required = False,
    type = str,
    default = "/data/QAQC_DM",
    help = "Directory with the temperature logs"
)

parser.add_argument(
    "--logfile",
    required = False,
    type = str,
    help = "Log file; if provided, will ignore run, dmid and logdir"
)

parser.add_argument(
    "--regexp",
    help = (
        "Keyed regular expression to extract run and DM barcode from the log file name.\n"
        "Generally the file path has the form run-[RUN]_DM-[BARCODE]"
        "\n   "
    ),
    type = str,
    required = False,
    default = "run-(?P<run>\d+)_DM-(?P<dmid>\d+)"
)

parser.add_argument(
    "--batch",
    required = False,
    action = "store_true",
    help = "Batch mode; will not display interactive plots"
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

def str_to_float(s) :
    
    f = None
    
    try :
        
        f = float(s)
    
    except ValueError :
        
        print(f"Could not convert {s} to float")
        pass
    
    return f

def parse_string_regex(
    s,
    regexp
) :
    
    rgx = re.compile(regexp)
    result = [m.groupdict() for m in rgx.finditer(s)][0]
    
    return result

plot_dir = args.plotdir
fname_noext = None

if (args.logfile) :
    
    file = args.logfile
    
    rgx_result = parse_string_regex(file, args.regexp)
    args.run = rgx_result["run"]
    args.dmid = rgx_result["dmid"]

else :
    log_dir = args.logdir
    file = f"{log_dir}/run-{args.run:04d}_DM-{args.dmid}.log"


fname_noext = os.path.splitext(os.path.basename(file))[0]
plot_file = f"{plot_dir}/{fname_noext}.png"
graph_file = f"{plot_dir}/{fname_noext}.root"

os.system(f"mkdir -p {plot_dir}")

nPointsOffset = 5

if (not args.batch) :
    
    plt.ion()

mytime = []
mysecs = []
TCopperR = []
TCopperL = []
TTopL = []
TTopR = []
TBottomL = []
TBottomR = []
DeltaTTopL = []
DeltaTTopR = []
DeltaTBottomL = []
DeltaTBottomR = []
currents = []
voltages = []
powers = []


# draw function ---file
def graph():
    # plt.clf()
    # axes = plt.gca()
    
    n = len(mysecs)
    output_file = ROOT.TFile.Open(graph_file, "RECREATE")
    gDeltaTTopL = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTTopL))
    gDeltaTTopR = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTTopR))
    gDeltaTBottomL = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTBottomL))
    gDeltaTBottomR = ROOT.TGraph(n, np.array(mysecs), np.array(DeltaTBottomR))
    
    title = f"DM {args.dmid}"
    
    l_drawn_objects = []
    
    fig = plt.figure(figsize = (10, 10))
    
    fontdict = {"weight": "bold"}
    
    ax_upr_l = fig.add_subplot(2, 1, 1)
    l_drawn_objects.extend(ax_upr_l.plot(mysecs, TCopperL, color = "black", linestyle = "dotted", label = "Left PT1000"))
    l_drawn_objects.extend(ax_upr_l.plot(mysecs, TCopperR, color = "black", linestyle = "dashed", label = "Right PT1000"))
    l_drawn_objects.extend(ax_upr_l.plot(mysecs, TTopL, color = "red", label = "Top left RTD"))
    l_drawn_objects.extend(ax_upr_l.plot(mysecs, TTopR, color = "orange", label = "Top right RTD"))
    l_drawn_objects.extend(ax_upr_l.plot(mysecs, TBottomL, color = "blue", label = "Bottom left RTD"))
    l_drawn_objects.extend(ax_upr_l.plot(mysecs, TBottomR, color = "green", label = "Bottom right RTD"))

    
    ax_upr_l.set_xlabel("Time elapsed [min]", fontdict = fontdict)
    ax_upr_l.set_ylabel("Temperature [°C]", fontdict = fontdict)
    ax_upr_l.grid()
    ax_upr_l.set_ylim([5, 50])
    ax_upr_l.legend(loc = "upper left", fontsize = "medium", shadow = False, title = title, title_fontproperties = fontdict)
    
    ax_upr_r = ax_upr_l.twinx()
    l_drawn_objects.extend(ax_upr_r.plot(mysecs, powers, color = "gray", linestyle = "dashdot", label = "Power drawn"))
    ax_upr_r.set_ylabel("Power [W]", fontdict = fontdict)
    #ax_upr_r.grid()
    ax_upr_r.set_ylim([0, 10])
    ax_upr_r.legend(loc = "upper right", fontsize = "medium", shadow = False)
    
    #ax_upr_l.legend(
    #    handles = l_drawn_objects,
    #    labels = [_obj.get_label() for _obj in l_drawn_objects],
    #    loc = "upper left",
    #    fontsize = "medium",
    #    shadow = False,
    #    title = title
    #)
    
    ax_lwr = fig.add_subplot(2, 1, 2)
    ax_lwr.plot(mysecs, DeltaTTopL, color = "red", label = "Top left RTD")
    ax_lwr.plot(mysecs, DeltaTTopR, color = "orange", label = "Top right RTD")
    ax_lwr.plot(mysecs, DeltaTBottomL, color = "blue", label = "Bottom left RTD")
    ax_lwr.plot(mysecs, DeltaTBottomR, color = "green", label = "Bottom right RTD")
    ax_lwr.plot(mysecs, np.average([DeltaTTopL, DeltaTTopR, DeltaTBottomL, DeltaTBottomR], axis = 0), color = "magenta", label = "Average")
    ax_lwr.set_xlabel("Time elapsed [min]", fontdict = fontdict)
    ax_lwr.set_ylabel("ΔT [°C]", fontdict = fontdict)
    ax_lwr.grid()
    ax_lwr.set_ylim([-35, 5])
    ax_lwr.legend(loc = "upper right", fontsize = "medium", shadow = False, title = title, title_fontproperties = {"weight": "bold"})
    ax_lwr.text(0, -22, f"max ΔT [°C] = {DeltaTTopLMin:.2f}, {DeltaTTopLMin-DeltaTAvg:.2f} wrt avg", color = "red")
    ax_lwr.text(0, -24, f"max ΔT [°C] = {DeltaTTopRMin:.2f}, {DeltaTTopRMin-DeltaTAvg:.2f} wrt avg", color = "orange")
    ax_lwr.text(0, -26, f"max ΔT [°C] = {DeltaTBottomLMin:.2f}, {DeltaTBottomLMin-DeltaTAvg:.2f} wrt avg", color = "blue")
    ax_lwr.text(0, -28, f"max ΔT [°C] = {DeltaTBottomRMin:.2f}, {DeltaTBottomRMin-DeltaTAvg:.2f} wrt avg", color = "green")

    evaltime = 4.0
    arr_deltaT_attime = numpy.array([gDeltaTTopL.Eval(evaltime), gDeltaTTopR.Eval(evaltime), gDeltaTBottomL.Eval(evaltime), gDeltaTBottomR.Eval(evaltime)])
    mean_attime = numpy.mean(arr_deltaT_attime)
    std_attime = numpy.std(arr_deltaT_attime)
    
    ax_lwr.text(0, -30, f"μ(max ΔT), σ(max ΔT) [°C] = {DeltaTAvg:.2f}, {DeltaTStd:.2f}", color = "magenta")
    ax_lwr.text(0, -32, f"μ(ΔT), σ(ΔT) at {evaltime} min [°C] = {mean_attime:.2f}, {std_attime:.2f}", color = "magenta")
    ax_lwr.text(0, -34, f"max power [W] = {np.max(powers):.2f}", color = "black")
    
    
    fig.tight_layout()
    fig.savefig(plot_file)
    
    print()
    print(f"Produced plot: {plot_file}")
    
    #save TGraphs 
    gDeltaTTopL.Write(f"g_DeltaTTopL_module_{args.dmid}")
    gDeltaTTopR.Write(f"g_DeltaTTopR_module_{args.dmid}")
    gDeltaTBottomL.Write(f"g_DeltaTBottomL_module_{args.dmid}")
    gDeltaTBottomR.Write(f"g_DeltaTBottomR_module_{args.dmid}")
    output_file.Close()
    print(f"Produced ROOT file: {graph_file}")


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
        readings = line.strip().replace(", ", " ").split()
        if len(readings) != 10:
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

        # the first two entries are date and time, hence +2
        TCopperL.append(float(readings[0+2]))
        TCopperR.append(float(readings[1+2]))
        TTopL.append(float(readings[5+2]))
        TTopR.append(float(readings[4+2]))
        TBottomL.append(float(readings[3+2]))
        TBottomR.append(float(readings[2+2]))
        
        # Exclude the unit 'A' end character
        current = str_to_float(readings[-2][:-1])
        current = current if (current and current > 0) else 0
        
        # Exclude the unit 'V' end character
        voltage = str_to_float(readings[-1][:-1])
        voltage = voltage if (voltage and voltage > 0) else 0
        
        power = current*voltage
        
        currents.append(current)
        voltages.append(voltages)
        powers.append(power)
        
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
        
        print(str(readings[1])+" "+str(readings[2])+" "+str(readings[3])+" "+str(readings[4])+" "+str(readings[5])+" "+str(readings[6])+" "+str(readings[7]))
        
        it += 1
    
    #arr_DeltaT = np.array([DeltaTTopLMin, DeltaTTopRMin, DeltaTBottomLMin, DeltaTBottomRMin])
    DeltaTMin = [min(DeltaTTopL), min(DeltaTTopR), min(DeltaTBottomL), min(DeltaTBottomR)]
    DeltaTAvg = np.mean(DeltaTMin)
    DeltaTStd = np.std(DeltaTMin)

graph()
# input("ok?")
