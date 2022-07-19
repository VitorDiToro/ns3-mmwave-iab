#!/usr/bin/python
import os

N_EXECUTIONS = 1
SEEDS = [1,2,3]
RUNS = 50

def execute_simulation(n_relays:int, seed:int, run:int):
    os.system(f"python3 run.py -r {n_relays} -t {N_EXECUTIONS} -s {seed} -n {run}")



for n_relays in range(5):
    for seed in SEEDS:
        for run in range(1,RUNS+1):
            execute_simulation(n_relays, seed, run)