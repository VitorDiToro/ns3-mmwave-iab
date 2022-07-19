#!/usr/bin/python
import os

N_EXECUTIONS = 1
SEEDS = [1,2,3]
RUNS = 50
N_RELAYS = 0


#for n_relays in [0]:
for seed in SEEDS:
    for run in range(1,RUNS+1):
        os.system(f"python3 run.py -r {N_RELAYS} -t {N_EXECUTIONS} -s {seed} -n {run}")

