#! /usr/bin/python

import os
import re
import sys
import argparse
from datetime import datetime


def get_parameters():
    # Create the parser
    parser = argparse.ArgumentParser(prog='mv-results',
                                     description='List arguments options',
                                     fromfile_prefix_chars='@')

    # Add the arguments
    parser.add_argument('-r',
                        metavar='Relays',
                        type=int,
                        action='store',
                        required=True,
                        help='Number of relays to use in simulation')
   
    parser.add_argument('-i',
                        metavar='Inter Packet Interval',
                        type=int,
                        action='store',
                        required=True,
                        help='interPacketInterval in us')
   
    parser.add_argument('-s',
                        metavar='Seed',
                        type=int,
                        action='store',
                        required=False,
                        default=1,
                        help='Random seed (Default: 1)') 
      
    parser.add_argument('-c',
                        metavar='Schedule: RR/PF',
                        type=str,
                        action='store',
                        required=False,
                        choices=["RR", "rr", "PF", "pf"],
                        default="PF",
                        help='Type of schedule used on simulation. RR(Round Robin) or PF(Proportional Fair)')
                            
    parser.add_argument('-n',
                        metavar='Execution number',
                        type=int,
                        action='store',
                        required=False,
                        default=0,
                        help='Define execution RUN on RngSeedManager (Default: 0)') 

    args = parser.parse_args()
    current_dir_path = sys.argv[0].replace(sys.argv[0].split("/")[-1], '')
    
    n_relays = args.r
    seed = args.s
    schedule = args.c
    run_turn = args.n
    interPacketInterval = args.i

    return [n_relays, interPacketInterval, seed, schedule, run_turn, current_dir_path]


def create_base_path(current_dir: str, n_relays: int, inter_packet_interval: int, seed: int, run: int, schedule_type: str):

    path = f"{current_dir}results/{schedule_type.upper()}/"
    
    path += f"{n_relays}-"
    if n_relays in [0,1]:
        path += "relay/"
    else:
        path += "relays/"
        
    path += f"{inter_packet_interval}us/"
    path += f"seed-{seed}/"
    path += f"run-{run}/"
    path += datetime.now().strftime("%Y.%m.%d-%H.%M.%S")

    if not os.path.exists(path):
        os.makedirs(path)

    return path


def move_results(base_path: str, execution_number: int = 0):
    files_list = ["DataRadioBearerCreatedTrace.txt",
                  "ENB-UE.txt",
                  "RlcAmBufferSize.txt",
                  "RxPacketTrace.txt",
                  "StateTransitionTrace.txt",
                  "UdpServerRx.txt",
                  "buildings.txt",
                  "enbs.txt",
                  "ues.txt",
                  "terminal.log"]

    folder_path = f"{base_path}/execution-{execution_number}/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for file in files_list:
        print(f"Moved {file}, To {folder_path}")
        #shutil.move(file, folder_path)
        os.system(f"mv {file} {folder_path}")


if __name__ == '__main__':
    n_relays, inter_packet_interval, seed, schedule_type, run_number, current_dir = get_parameters()
    
    output_base_path = create_base_path(current_dir, n_relays, inter_packet_interval, seed, run_number, schedule_type)
    
    move_results(output_base_path) #, execution)