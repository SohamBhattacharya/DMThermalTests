#!/usr/bin/env python3

import os


nruns = 27

d_args = {}
d_args["logdir"] = "../data/QAQC_DM"

#d_args["plotdir"] = "../data/QAQC_DM/plots_w-offset"
#d_args["offset"] = ""

d_args["plotdir"] = "../data/QAQC_DM/plots_wo-offset"

d_info = {}
d_info["32110040004201"] = list(range(1, nruns+1))

for dm in d_info :

    l_runs = d_info[dm]

    for run in l_runs :
        
        str_args = " ".join([f"--{_key} {_val}" for _key, _val in d_args.items()])
        cmd = f"./plotTemp_PT1000.py --run {run} --dmid {dm} --batch {str_args}"
        print(cmd)
        os.system(cmd)
