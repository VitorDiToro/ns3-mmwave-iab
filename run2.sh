#!/bin/bash

N_EXECUTIONS=1
RUNS=50
N_RELAYS=0


for seed in {1..3}
do
    for run in $(seq 1 $RUNS)
    do
        python3 run.py -r $N_RELAYS -t $N_EXECUTIONS -s $seed -n $run
    done
done

