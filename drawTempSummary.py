#! /usr/bin/env python3

import glob
import numpy
import os
import re
import ROOT
#import tdrstyle

ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.SetBatch(False)


def expand_range(rng):
    numbers = []
    for item in rng:
        if '-' in item:
            start, end = map(int, item.split('-'))   
            numbers.extend(range(start, end + 1))
        else:
            numbers.append(int(item))
    return sorted(numbers)



data_path = '../data/QAQC_DM/plots_w-offset/'
#data_path = '../data/QAQC_DM/plots_wo-offset/'

plotDir = f'{data_path}/summary_plots/'
os.system(f"mkdir -p {plotDir}")

#runs = ['7-9','11-19','21-23','25-28','33','40-46','49','51-52','54-56', '58-61','65-66', '68-73', '75-78','80-83','85-89', '104-105','110-111', '113-117', '124-125']

#run_list = expand_range(runs)
print('Plot dir: ', plotDir)
#print('Runs:', run_list)


hDeltaTMean = ROOT.TH1F('hDeltaTMean','hDeltaTMean', 500, -25, -15)
hDeltaTRMS  = ROOT.TH1F('hDeltaTRMS','hDeltaTRMS', 100, 0, 2)
hDeltaTTopLRatio = ROOT.TH1F('hDeltaTTopLRatio','hDeltaTTopLRatio', 100, 0, 5)  
hDeltaTTopRRatio = ROOT.TH1F('hDeltaTTopRRatio','hDeltaTTopRRatio', 100, 0, 5)  
hDeltaTBottomLRatio = ROOT.TH1F('hDeltaTBottomLRatio','hDeltaTBottomLRatio', 100, 0, 5)  
hDeltaTBottomRRatio = ROOT.TH1F('hDeltaTBOttomRRatio','hDeltaTBottomRRatio', 100, 0, 5)  
hDeltaTRMS_after2min  = ROOT.TH1F('hDeltaTRMS_after2min','hDeltaTRMS_after2min', 100, 0, 2)
hDeltaTRMS_after4min  = ROOT.TH1F('hDeltaTRMS_after4min','hDeltaTRMS_after4min', 100, 0, 2)
hDeltaTRMS_ratio  = ROOT.TH1F('hDeltaTRMS_ratio','hDeltaTRMS_ratio', 50, 0, 2)

time1 = 2.
time2 = 4. 

def parse_string_regex(
    s,
    regexp
) :
    
    rgx = re.compile(regexp)
    result = [m.groupdict() for m in rgx.finditer(s)][0]
    
    return result

for fname in glob.glob(data_path+'/*.root'):
    
    print(fname)
    #if  (  int(fname.split('_')[1].replace('run','')) not in run_list):
    #    continue
    #dm = fname.split('_')[3].replace('.root','')
    #print(dm, "  in run ",  int(fname.split('_')[1].replace('run','')))
    
    rgx_result = parse_string_regex(s = fname, regexp = "run-(?P<run>\d+)_DM-(?P<dmid>\d+)")
    run = rgx_result["run"]
    dm = rgx_result["dmid"]
    
    f = ROOT.TFile.Open(fname, "READ")
    gDeltaTTopL = f.Get('g_DeltaTTopL_module_{}'.format(dm))
    gDeltaTTopR = f.Get('g_DeltaTTopR_module_{}'.format(dm))
    gDeltaTBottomL = f.Get('g_DeltaTBottomL_module_{}'.format(dm))
    gDeltaTBottomR = f.Get('g_DeltaTBottomR_module_{}'.format(dm))
    
    htemp = ROOT.TH1F('htemp','htemp', 200, -30, -10)
    for g in [gDeltaTTopL, gDeltaTTopR, gDeltaTBottomL, gDeltaTBottomR]:
        #print(g.GetName(), numpy.array(g.GetY()))
        gmin = min(g.GetY())
        #print(g.GetName(), gmin)
        htemp.Fill(gmin)
    deltaTempMean = htemp.GetMean()
    deltaTempRMS  = htemp.GetRMS()
    hDeltaTMean.Fill(deltaTempMean)
    #print(deltaTempMean)
    hDeltaTRMS.Fill(deltaTempRMS)
    hDeltaTTopLRatio.Fill(gDeltaTTopL.Eval(time2)/gDeltaTTopL.Eval(time1))
    hDeltaTTopRRatio.Fill(gDeltaTTopR.Eval(time2)/gDeltaTTopR.Eval(time1))
    hDeltaTBottomLRatio.Fill(gDeltaTBottomL.Eval(time2)/gDeltaTBottomL.Eval(time1))
    hDeltaTBottomRRatio.Fill(gDeltaTBottomR.Eval(time2)/gDeltaTBottomR.Eval(time1))
    htemp1 = ROOT.TH1F('htemp1','htemp1', 100, -30, 0)
    htemp2 = ROOT.TH1F('htemp2','htemp2', 100, -30, 0)
    for g in [gDeltaTTopL, gDeltaTTopR, gDeltaTBottomL, gDeltaTBottomR]:
        htemp1.Fill( g.Eval(time1) )
        htemp2.Fill( g.Eval(time2) )
    hDeltaTRMS_after2min.Fill(htemp1.GetRMS())
    hDeltaTRMS_after4min.Fill(htemp2.GetRMS())
    hDeltaTRMS_ratio.Fill( (htemp2.GetRMS()/htemp2.GetMean())/(htemp1.GetRMS()/htemp1.GetMean()))
    #print(htemp1.GetRMS(), htemp2.GetRMS(), htemp.GetRMS() )

ROOT.gStyle.SetOptStat(1110) 

c = ROOT.TCanvas('c_DeltaTMean','', 800, 700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
hDeltaTMean.SetTitle('; <#Delta T> [C]; entries')
hDeltaTMean.SetFillStyle(3001)
hDeltaTMean.SetFillColor(ROOT.kRed)
hDeltaTMean.SetLineColor(ROOT.kRed)
hDeltaTMean.Draw()
c.Print(plotDir+'DeltaTMean.png')


c = ROOT.TCanvas('c_DeltaTRMS','', 800, 700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
hDeltaTRMS.SetTitle('; RMS(#DeltaT) [^{o}C];entries')
hDeltaTRMS.SetFillStyle(3001)
hDeltaTRMS.SetFillColor(ROOT.kRed)
hDeltaTRMS.SetLineColor(ROOT.kRed)
hDeltaTRMS.Draw()
c.Print(plotDir+'DeltaTRMS.png')


c = ROOT.TCanvas('c_DeltaTRMS_after2min','', 800, 700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
hDeltaTRMS_after2min.SetTitle('; RMS(#DeltaT) after 2 min [^{o}C];entries')
hDeltaTRMS_after2min.SetFillStyle(3001)
hDeltaTRMS_after2min.SetFillColor(ROOT.kRed)
hDeltaTRMS_after2min.SetLineColor(ROOT.kRed)
hDeltaTRMS_after2min.Draw()
c.Print(plotDir+'DeltaTRMS_after2min.png')

c = ROOT.TCanvas('c_DeltaTRMS_after4min','', 800, 700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
hDeltaTRMS_after4min.SetTitle('; RMS(#DeltaT) after 4 min [^{o}C];entries')
hDeltaTRMS_after4min.SetFillStyle(3001)
hDeltaTRMS_after4min.SetFillColor(ROOT.kRed)
hDeltaTRMS_after4min.SetLineColor(ROOT.kRed)
hDeltaTRMS_after4min.Draw()
c.Print(plotDir+'DeltaTRMS_after4min.png')


c = ROOT.TCanvas('c_DeltaTRMS_ratio','', 800, 700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
hDeltaTRMS_ratio.SetTitle('; RMS(4 min)/RMS(2 min);entries')
hDeltaTRMS_ratio.SetFillStyle(3001)
hDeltaTRMS_ratio.SetFillColor(ROOT.kRed)
hDeltaTRMS_ratio.SetLineColor(ROOT.kRed)
hDeltaTRMS_ratio.Draw()
c.Print(plotDir+'DeltaTRMS_ratio.png')


c = ROOT.TCanvas('c_DeltaTTopLRatio','', 800, 700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
hDeltaTTopLRatio.SetTitle('; #DeltaT_{4min}/#DeltaT_{2min};entries')
hDeltaTTopLRatio.SetFillStyle(3001)
hDeltaTTopLRatio.SetFillColor(ROOT.kRed)
hDeltaTTopLRatio.SetLineColor(ROOT.kRed)
hDeltaTTopLRatio.Draw()
c.Print(plotDir+'DeltaTTopLRatio.png')


c = ROOT.TCanvas('c_DeltaTTopRRatio','', 800, 700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
hDeltaTTopRRatio.SetTitle('; #DeltaT_{4min}/#DeltaT_{2min};entries')
hDeltaTTopRRatio.SetFillStyle(3001)
hDeltaTTopRRatio.SetFillColor(ROOT.kRed)
hDeltaTTopRRatio.SetLineColor(ROOT.kRed)
hDeltaTTopRRatio.Draw()
c.Print(plotDir+'DeltaTTopRRatio.png')


c = ROOT.TCanvas('c_DeltaTBottomLRatio','', 800, 700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
hDeltaTBottomLRatio.SetTitle('; #DeltaT_{4min}/#DeltaT_{2min};entries')
hDeltaTBottomLRatio.SetFillStyle(3001)
hDeltaTBottomLRatio.SetFillColor(ROOT.kRed)
hDeltaTBottomLRatio.SetLineColor(ROOT.kRed)
hDeltaTBottomLRatio.Draw()
c.Print(plotDir+'DeltaTBottomLRatio.png')


c = ROOT.TCanvas('c_DeltaTBottomRRatio','', 800, 700)
ROOT.gPad.SetGridx()
ROOT.gPad.SetGridy()
hDeltaTBottomRRatio.SetTitle('; #DeltaT_{4min}/#DeltaT_{2min};entries')
hDeltaTBottomRRatio.SetFillStyle(3001)
hDeltaTBottomRRatio.SetFillColor(ROOT.kRed)
hDeltaTBottomRRatio.SetLineColor(ROOT.kRed)
hDeltaTBottomRRatio.Draw()
c.Print(plotDir+'DeltaTBottomRRatio.png')
